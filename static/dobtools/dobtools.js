/* =====================================================================
   DOBTools — shared behaviour (no dependencies)
   - Mobile menu toggle
   - "Copy citation" buttons
   - Screenshot viewer (click to enlarge)
   - Step showcase: the six steps cross-fading, with the 3D pose turning beside
   - DawnDock sidebar: collapsible on narrow screens + highlights the section in view
   - Download form: asks who is downloading, records it, starts the download

   The pages are styled with Tailwind, so this script never sets a style or a
   class to show state. It sets attributes, and the classes on the pages react
   to them:
     data-js            on the header, once the script runs (the menu folds away)
     data-open          on the menu while it is open
     data-step          on the download form: "form", then "done"
     data-ready         on the form once all three fields are filled
     data-bad           on the email field while what is in it is not an address
     data-active        on the showcase's current slide and caption
     data-auto          on the showcase while it advances by itself
     data-play          on the showcase: "running" while on screen and not held
     aria-selected,     on the showcase's tabs
     aria-expanded,     on the menu button
     aria-current       on the sidebar link of the section in view
   The lightbox below is the one piece of markup the script makes itself, so
   its Tailwind classes are written here; the stylesheet is built from this
   file as well as the pages.

   There used to be an English / বাংলা switch here for the manual. The manual
   is published in English only, so the switch and the pane it showed are gone;
   put both back together if a translation is ever made.
   ===================================================================== */
(function () {
  'use strict';

  /* ---------- Mobile menu ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-dobt-menu]'), function (btn) {
    var nav = document.getElementById(btn.getAttribute('aria-controls'));
    var header = btn.closest('[data-dobt-header]');
    if (!nav || !header) return;
    header.setAttribute('data-js', '');

    function isOpen() { return nav.hasAttribute('data-open'); }
    function setOpen(open) {
      btn.setAttribute('aria-expanded', String(open));
      btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (open) nav.setAttribute('data-open', ''); else nav.removeAttribute('data-open');
    }
    btn.addEventListener('click', function () { setOpen(!isOpen()); });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isOpen()) { setOpen(false); btn.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (isOpen() && !header.contains(e.target)) setOpen(false);
    });
  });

  /* ---------- Copy citation ---------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.top = '-1000px';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy') ? resolve() : reject(new Error('copy failed')); }
      catch (err) { reject(err); }
      finally { document.body.removeChild(ta); }
    });
  }

  function selectText(el) {
    try {
      var range = document.createRange();
      range.selectNodeContents(el);
      var sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
    } catch (e) { /* ignore */ }
  }

  Array.prototype.forEach.call(document.querySelectorAll('[data-dobt-copy]'), function (btn) {
    var source = document.getElementById(btn.getAttribute('data-dobt-copy'));
    var label = btn.querySelector('[data-dobt-copy-label]') || btn;
    if (!source) return;
    var original = label.textContent;
    var timer;
    btn.addEventListener('click', function () {
      copyText(source.textContent.replace(/\s+/g, ' ').trim()).then(function () {
        label.textContent = 'Copied';
      }, function () {
        selectText(source);
        label.textContent = 'Press Ctrl+C to copy';
      });
      clearTimeout(timer);
      timer = setTimeout(function () { label.textContent = original; }, 2400);
    });
  });

  /* ---------- Screenshot viewer (click to enlarge) ----------
     Without JS (or <dialog> support) the link simply opens the image. */
  var zoomLinks = document.querySelectorAll('[data-dobt-lightbox]');
  if (zoomLinks.length && typeof window.HTMLDialogElement === 'function') {
    var dialog = document.createElement('dialog');
    dialog.className = 'm-0 size-full max-h-none max-w-none border-0 bg-transparent p-0 font-sans backdrop:bg-[rgb(10_20_33/.9)]';
    dialog.setAttribute('aria-label', 'Screenshot, full size');
    dialog.innerHTML =
      '<button type="button" class="fixed top-4 right-4 z-[2] grid size-[42px] cursor-pointer place-items-center rounded-full border border-white/30 bg-black/45 text-white hover:bg-black/70" data-dobt-lightbox-close aria-label="Close">' +
        '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12"/><path d="M18 6L6 18"/></svg>' +
      '</button>' +
      '<a class="fixed bottom-[18px] left-1/2 -translate-x-1/2 text-[13.5px] text-white underline underline-offset-[3px]" data-dobt-lightbox-raw target="_blank" rel="noopener">Open image in new tab</a>' +
      '<div class="grid size-full place-items-center p-[4vmin]" data-dobt-lightbox-inner>' +
        '<img class="max-h-[92vh] max-w-full rounded-lg shadow-[0_30px_80px_rgb(0_0_0/.5)]" alt="">' +
      '</div>';
    document.body.appendChild(dialog);

    var bigImg = dialog.querySelector('img');
    var rawLink = dialog.querySelector('[data-dobt-lightbox-raw]');
    var inner = dialog.querySelector('[data-dobt-lightbox-inner]');
    var lastTrigger = null;
    var isOpen = false;

    // Undo the scroll lock and return focus. Safe to call more than once.
    var cleanup = function () {
      if (!isOpen) return;
      isOpen = false;
      document.documentElement.style.overflow = '';
      if (lastTrigger) lastTrigger.focus();
    };
    var closeViewer = function () {
      if (dialog.open) dialog.close();
      cleanup();
    };

    dialog.querySelector('[data-dobt-lightbox-close]').addEventListener('click', closeViewer);
    dialog.addEventListener('click', function (e) {
      if (e.target === dialog || e.target === inner) closeViewer();
    });
    dialog.addEventListener('cancel', cleanup); // Esc key
    dialog.addEventListener('close', cleanup);

    Array.prototype.forEach.call(zoomLinks, function (link) {
      link.addEventListener('click', function (e) {
        if (e.ctrlKey || e.metaKey || e.shiftKey || e.button === 1) return; // let "open in new tab" through
        e.preventDefault();
        var thumb = link.querySelector('img');
        bigImg.src = link.getAttribute('href');
        bigImg.alt = thumb ? thumb.alt : '';
        rawLink.href = link.getAttribute('href');
        lastTrigger = link;
        isOpen = true;
        document.documentElement.style.overflow = 'hidden';
        dialog.showModal();
      });
    });
  }

  /* ---------- Step showcase ("What DawnDock does") ----------
     The fill animation on the current step's bar is the clock: when it ends, the
     show moves on. Pausing that animation (pointer over the show, keyboard focus
     inside it, or the show scrolled off screen) therefore pauses the show, and
     there is no separate timer to drift out of step with what is drawn. */
  Array.prototype.forEach.call(document.querySelectorAll('[data-dobt-show]'), function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[data-dobt-show-tab]'));
    var slides = Array.prototype.slice.call(root.querySelectorAll('[data-dobt-show-slide]'));
    var caps = Array.prototype.slice.call(root.querySelectorAll('[data-dobt-show-cap]'));
    var panel = root.querySelector('[role="tabpanel"]');
    var card = root.querySelector('[data-dobt-show-pose]');
    var video = card ? card.querySelector('video') : null;
    var reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    var current = 0;
    if (!tabs.length || tabs.length !== slides.length) return;

    function mark(list, i, extra) {
      list.forEach(function (el, k) {
        var on = k === i;
        if (on) {
          el.setAttribute('data-active', '');
          el.removeAttribute('aria-hidden');
        } else {
          el.removeAttribute('data-active');
          el.setAttribute('aria-hidden', 'true');
        }
        if (extra) extra(el, on);
      });
    }

    function show(i, focus) {
      i = (i + tabs.length) % tabs.length;
      if (i !== current) {
        tabs.forEach(function (t, k) {
          t.setAttribute('aria-selected', String(k === i));
          t.tabIndex = k === i ? 0 : -1;
        });
        mark(slides, i, function (el, on) {
          if (on) el.removeAttribute('tabindex'); else el.tabIndex = -1;
        });
        mark(caps, i);
        if (panel) panel.setAttribute('aria-labelledby', tabs[i].id);
        current = i;
      }
      if (focus) tabs[i].focus();
    }

    // The bar fills (and so the show advances) only while the show is on screen
    // and nobody is holding it, with the pointer or with the keyboard.
    var visible = false, hovered = false, focused = false;
    function syncPlay() {
      root.setAttribute('data-play', visible && !hovered && !focused ? 'running' : 'paused');
    }

    // Someone who picks a step wants to look at it, so the show stops there.
    function stopAuto() { root.removeAttribute('data-auto'); }

    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { stopAuto(); show(k, false); });
      t.addEventListener('keydown', function (e) {
        var to = null;
        if (e.key === 'ArrowRight') to = current + 1;
        else if (e.key === 'ArrowLeft') to = current - 1;
        else if (e.key === 'Home') to = 0;
        else if (e.key === 'End') to = tabs.length - 1;
        if (to === null) return;
        e.preventDefault();
        stopAuto();
        show(to, true);
      });
      var bar = t.querySelector('[data-dobt-show-fill]');
      if (bar) bar.addEventListener('animationend', function () {
        if (root.hasAttribute('data-auto') && k === current) show(current + 1, false);
      });
    });

    root.addEventListener('mouseenter', function () { hovered = true; syncPlay(); });
    root.addEventListener('mouseleave', function () { hovered = false; syncPlay(); });
    root.addEventListener('focusin', function () { focused = true; syncPlay(); });
    root.addEventListener('focusout', function (e) {
      if (!root.contains(e.relatedTarget)) { focused = false; syncPlay(); }
    });

    // The steps fade from one to the next for everyone: a fade moves nothing on
    // screen, which is why it is the usual stand-in when a reader asks for less
    // motion. Only the movement (the zoom, the floating card, the spinning pose)
    // is held back for them, by the motion-reduce classes and just below.
    syncPlay();
    root.setAttribute('data-auto', '');

    function playVideo() {
      if (!video || video.offsetParent === null) return;   // hidden on phones
      if (!video.getAttribute('src')) video.setAttribute('src', video.getAttribute('data-src'));
      var p = video.play();
      if (p && p.catch) p.catch(function () { /* autoplay refused: the poster stays */ });
    }

    // Under reduced motion the pose turns only while the pointer is on it: motion
    // the reader starts themselves is not the motion the setting asks to avoid.
    if (video && reduce) {
      card.addEventListener('mouseenter', playVideo);
      card.addEventListener('mouseleave', function () { video.pause(); });
    }

    // Run only while the show is on screen. The 3D clip is fetched the first
    // time it is needed, and never where the card is hidden (phones).
    function onScreen(isVisible) {
      visible = isVisible;
      syncPlay();
      if (!video) return;
      if (isVisible && !reduce) playVideo();
      else if (!isVisible) video.pause();
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { onScreen(en.isIntersecting); });
      }, { threshold: 0.35 }).observe(root);
    } else {
      onScreen(true);
    }
  });

  /* ---------- DawnDock sidebar ---------- */
  var toc = document.querySelector('[data-dobt-toc]');
  if (toc) {
    // 1024 px is Tailwind's `lg`, where the page's classes put the sidebar
    // beside the content instead of above it.
    var desktop = window.matchMedia('(min-width: 1024px)');
    var syncToc = function () { toc.open = desktop.matches; };
    syncToc();
    if (desktop.addEventListener) desktop.addEventListener('change', syncToc);
    else if (desktop.addListener) desktop.addListener(syncToc);

    toc.addEventListener('click', function (e) {
      if (e.target.closest('a') && !desktop.matches) toc.open = false;
    });

    // Highlight the link of the section currently in view
    var spyLinks = Array.prototype.slice.call(toc.querySelectorAll('a[data-dobt-spy]'));
    var targets = spyLinks.map(function (a) {
      return { link: a, el: document.getElementById(a.getAttribute('href').slice(1)) };
    }).filter(function (t) { return t.el; });

    var ticking = false;
    var updateSpy = function () {
      ticking = false;
      if (!targets.length) return;
      var line = 140;
      var current = targets[0];
      targets.forEach(function (t) {
        if (t.el.getBoundingClientRect().top <= line) current = t;
      });
      var doc = document.documentElement;
      if (window.innerHeight + window.scrollY >= doc.scrollHeight - 4) {
        current = targets[targets.length - 1];
      }
      targets.forEach(function (t) {
        if (t === current) t.link.setAttribute('aria-current', 'location');
        else t.link.removeAttribute('aria-current');
      });
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(updateSpy); }
    }, { passive: true });
    window.addEventListener('resize', updateSpy);
    updateSpy();
  }

  /* ---------- Download form ----------
     The Download button opens a form that asks who is downloading. The form
     carries the installer's address (data-dobt-file) and its own button, which
     stays disabled until a name, an institute and an email address are in.
     Pressing it does three things: remembers the details in this browser, so a
     returning visitor does not type them twice; records the download, with one
     POST to data-dobt-collect; and starts the download.

     The record is sent with sendBeacon, which the browser delivers even while
     it is busy starting a 298 MB download, and which needs no answer: the
     download never waits on it, and never fails because of it. While
     data-dobt-collect is empty nothing is sent at all.

     This asks people who they are; it does not lock the file. The installer is
     still an ordinary file on the site, and the same release is on GitHub and
     Zenodo, so the list is of those who came through this page. */
  Array.prototype.forEach.call(document.querySelectorAll('[data-dobt-gate]'), function (gate) {
    var form = gate.querySelector('form');
    var go = form ? form.querySelector('[type="submit"]') : null;
    var file = gate.getAttribute('data-dobt-file');
    if (!form || !go || !file) return;

    var who = ['name', 'institute', 'email'].map(function (n) { return form.elements[n]; });
    var mailField = who[2].closest('[data-dobt-gate-field]');
    var again = gate.querySelector('[data-dobt-gate-again]');
    var doneTitle = gate.querySelector('[data-dobt-gate-done]');
    var KEY = 'dobt-downloader';
    var lastTrigger = null;
    var locked = false;

    function text(el) { return el.value.replace(/\s+/g, ' ').trim(); }
    function isEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); }
    function ready() {
      return text(who[0]).length >= 2 && text(who[1]).length >= 2 && isEmail(text(who[2]));
    }
    function sync() {
      var ok = ready();
      go.disabled = !ok;
      if (ok) form.setAttribute('data-ready', ''); else form.removeAttribute('data-ready');
      if (mailField && isEmail(text(who[2]))) mailField.removeAttribute('data-bad');
    }

    who.forEach(function (el) { el.addEventListener('input', sync); });
    // Say the address looks wrong only once they have left the field: nobody's
    // address looks right while they are half way through typing it.
    who[2].addEventListener('blur', function () {
      if (!mailField) return;
      var v = text(who[2]);
      if (v && !isEmail(v)) mailField.setAttribute('data-bad', ''); else mailField.removeAttribute('data-bad');
    });

    function remember(details) {
      try { window.localStorage.setItem(KEY, JSON.stringify(details)); } catch (e) { /* private window */ }
    }
    function recall() {
      try {
        var saved = JSON.parse(window.localStorage.getItem(KEY) || 'null');
        if (saved) who.forEach(function (el) { if (!el.value && saved[el.name]) el.value = saved[el.name]; });
      } catch (e) { /* nothing saved, or not readable */ }
    }

    function record(details) {
      var url = gate.getAttribute('data-dobt-collect');
      if (!url) return;
      var body = new URLSearchParams();
      body.set('name', details.name);
      body.set('institute', details.institute);
      body.set('email', details.email);
      body.set('version', gate.getAttribute('data-dobt-version') || '');
      body.set('file', file.split('/').pop());
      body.set('page', window.location.origin + window.location.pathname);
      body.set('hp_check', form.elements.hp_check ? form.elements.hp_check.value : '');
      try {
        if (navigator.sendBeacon && navigator.sendBeacon(url, body)) return;
      } catch (e) { /* fall through to fetch */ }
      try {
        window.fetch(url, { method: 'POST', mode: 'no-cors', body: body, keepalive: true });
      } catch (e) { /* the download goes ahead regardless */ }
    }

    function start() {
      var a = document.createElement('a');
      a.href = file;
      a.setAttribute('download', '');
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!ready()) return;
      var details = { name: text(who[0]), institute: text(who[1]), email: text(who[2]) };
      remember(details);
      record(details);
      start();
      if (again) again.href = file;
      gate.setAttribute('data-step', 'done');
      if (doneTitle) doneTitle.focus();
    });

    function unlock() {
      if (!locked) return;
      locked = false;
      document.documentElement.style.overflow = '';
      if (lastTrigger) lastTrigger.focus();
    }
    function shut() {
      if (gate.open && typeof gate.close === 'function') gate.close();
      else gate.removeAttribute('open');
      unlock();
    }
    function open(trigger) {
      lastTrigger = trigger || null;
      gate.setAttribute('data-step', 'form');
      recall();
      sync();
      if (typeof gate.showModal === 'function') { if (!gate.open) gate.showModal(); }
      else gate.setAttribute('open', '');           // a browser without <dialog>: shown in the page
      locked = true;
      document.documentElement.style.overflow = 'hidden';
      var empty = who.filter(function (el) { return !text(el); })[0];
      (empty || go).focus();
    }

    gate.addEventListener('click', function (e) {
      if (e.target === gate || e.target.closest('[data-dobt-gate-close]')) shut();   // the backdrop, or a close control
    });
    gate.addEventListener('cancel', unlock);   // Esc key
    gate.addEventListener('close', unlock);

    Array.prototype.forEach.call(document.querySelectorAll('[data-dobt-get="' + gate.id + '"]'), function (btn) {
      btn.addEventListener('click', function () { open(btn); });
    });
  });
})();
