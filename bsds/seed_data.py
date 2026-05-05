import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from bsds.models import CampusCoordinator, Collaboration, Competition, ResearchTalk

def run():
    # 1. Campus Coordinators
    CampusCoordinator.objects.all().delete()
    CampusCoordinator.objects.create(
        year=2024,
        name="Sarah Rahman",
        role_label="Best Bioinformatics Campus Coordinator 2024",
        description="Sarah expanded the BSDS network to 3 new public universities, organizing 5 hands-on workshops and onboarding over 200 new students to foundational computational biology tools.",
        order=1
    )
    CampusCoordinator.objects.create(
        year=2023,
        name="Ahmed Hasan",
        role_label="Outstanding Hub Leader 2023",
        description="Ahmed spearheaded a regional bio-hackathon that brought together students from 10 different institutions, fostering a collaborative spirit that continues to thrive in his district.",
        order=2
    )
    print("Seeded Campus Coordinators")

    # 2. Collaboration
    Collaboration.objects.all().delete()
    universities = [
        ("University of Dhaka", "school"),
        ("BUET", "precision_manufacturing"),
        ("Rajshahi University", "science"),
        ("Jahangirnagar University", "biotech"),
        ("SUST", "computer"),
    ]
    for i, (name, icon) in enumerate(universities):
        Collaboration.objects.create(name=name, icon=icon, collab_type='university', order=i)

    clubs = [
        ("SUST Science Arena", "science"),
        ("DU IT Society", "computer"),
        ("RU Science Club", "biotech"),
        ("BUET Robotics Club", "precision_manufacturing"),
        ("JU Bioinformatics Hub", "school"),
    ]
    for i, (name, icon) in enumerate(clubs):
        Collaboration.objects.create(name=name, icon=icon, collab_type='club', order=i)
    
    print("Seeded Collaborations")

    # 3. Competition
    Competition.objects.all().delete()
    # Active
    Competition.objects.create(
        title="Bioinformatics Video Contest 2024",
        description="Communicate complex biological concepts through compelling visual narratives. Challenge yourself to bridge the gap between data and public understanding.",
        is_active=True,
        apply_url="https://google.com",
        order=1
    )
    Competition.objects.create(
        title="Bioinformatics Writing Contest 2024",
        description="Articulate groundbreaking research or ethical considerations in modern genomics. Submit your manuscript for review by our panel of distinguished scientists.",
        is_active=True,
        apply_url="https://google.com",
        order=2
    )
    # Past Winners
    Competition.objects.create(
        title="Bioinformatics Video Contest Winner",
        description="Communicate complex biological concepts through compelling visual narratives. Challenge yourself to bridge the gap between data and public understanding.",
        is_active=False,
        placement='1st',
        year=2023,
        order=1
    )
    Competition.objects.create(
        title="BioCompute Collective",
        description="The collective engineered a serverless pipeline capable of processing massive viral genome datasets, enabling real-time tracking of emerging pathogens across global networks.",
        is_active=False,
        placement='2nd',
        year=2023,
        order=2
    )
    Competition.objects.create(
        title="Genome Nexus",
        description="Genome Nexus authored a comprehensive study on soil microbiome diversity in industrial zones, leading to new bioremediation strategies for contaminated agricultural land.",
        is_active=False,
        placement='3rd',
        year=2023,
        order=3
    )
    print("Seeded Competitions")

    # 4. Research Talks
    ResearchTalk.objects.all().delete()
    talks = [
        ("Advanced Proteomics: Decoding Structural Complexity", "A comprehensive deep-dive into mass spectrometry data processing for protein identification and quantification.", "45:12"),
        ("Machine Learning in Variant Interpretation", "Exploring neural network architectures designed for predicting the functional impact of genetic mutations.", "38:05"),
        ("Next-Gen Sequencing Pipelines: Scalability & Speed", "Optimizing cloud-based architectures for rapid processing of multi-terabyte genomic datasets.", "52:40"),
        ("Transcriptomics: Understanding Gene Expression", "Techniques for RNA-Seq analysis and differential expression testing across varied biological conditions.", "29:15"),
        ("The Dawn-R Framework: Global Ethics in Bio-Data", "A keynote session discussing the ethical implications of large-scale genetic data sharing and privacy.", "1:04:22"),
        ("Microbiome Metagenomics: A New Frontier", "Analyzing the functional diversity of microbial communities through shotgun metagenomic sequencing.", "41:55"),
    ]
    for i, (title, desc, duration) in enumerate(talks):
        ResearchTalk.objects.create(
            title=title,
            description=desc,
            duration=duration,
            youtube_url="https://youtube.com",
            order=i
        )
    print("Seeded Research Talks")

if __name__ == "__main__":
    run()
