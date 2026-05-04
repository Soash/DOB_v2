import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from core.models import Carrier

def load_data():
    carriers = [
        {
            "title": "Bioinformatics Researcher",
            "employment_type": "Full-time",
            "location": "Dhaka Office",
            "vacancy": 1,
            "posted_date": date.today() - timedelta(days=10),
            "deadline": date.today() + timedelta(days=20),
            "short_description": "Lead complex genomic data analysis projects and develop novel algorithms for metabolic pathway modeling in specialized plant species.",
            "job_overview": "<p>Dawn of Bioinformatics Limited is seeking a visionary Bioinformatics Researcher to spearhead our genomic data analysis initiatives. In this role, you will lead complex projects focused on interpreting vast biological datasets to drive innovation in precision medicine. You will work at the intersection of high-performance computing and molecular biology, ensuring that our research maintains absolute precision and scientific integrity at every stage of the pipeline.</p>",
            "required_profile": "<ul><li>PhD in Bioinformatics, Computational Biology, or a related quantitative field.</li><li>Minimum 3 years of post-doctoral or industrial experience in genomic data analysis.</li><li>Expertise in Python and R, with a strong foundation in statistical modeling.</li><li>Extensive publication record in high-impact peer-reviewed journals.</li><li>Proficiency with cloud computing (AWS/GCP) and containerization (Docker).</li></ul>",
            "role_description": "<ul><li><strong>Project Leadership:</strong> Coordinate multidisciplinary teams to execute genomic research roadmaps.</li><li><strong>Algorithm Development:</strong> Design and implement novel computational methods for variant calling and annotation.</li><li><strong>Data Quality Control:</strong> Maintain rigorous QC standards for NGS pipelines and clinical datasets.</li><li><strong>Collaborative Research:</strong> Partner with laboratory teams to optimize wet-lab and dry-lab integration.</li></ul>",
            "salary_info": "<p>Competitive compensation package commensurate with academic standing and professional experience. Includes performance bonuses, comprehensive health insurance, and research stipends.</p>"
        },
        {
            "title": "Data Scientist (Genomics)",
            "employment_type": "Full-time",
            "location": "Chittagong",
            "vacancy": 1,
            "posted_date": date.today() - timedelta(days=15),
            "deadline": date.today() + timedelta(days=15),
            "short_description": "Apply machine learning techniques to large-scale biological datasets to identify biomarkers for early disease detection.",
            "job_overview": "<p>We are looking for a Data Scientist with a passion for genomics. You will apply advanced machine learning techniques to large-scale biological datasets, aiming to uncover hidden patterns and identify critical biomarkers.</p>",
            "required_profile": "<ul><li>Master's or PhD in Data Science, Computer Science, or Bioinformatics.</li><li>Strong background in Machine Learning algorithms (Random Forest, Deep Learning).</li><li>Experience working with omics data.</li></ul>",
            "role_description": "<ul><li><strong>Model Building:</strong> Develop predictive models for clinical outcomes based on genomic profiles.</li><li><strong>Data Integration:</strong> Merge diverse biological datasets for holistic analysis.</li></ul>",
            "salary_info": "<p>Industry-leading salary with equity options.</p>"
        },
        {
            "title": "Lab Technician",
            "employment_type": "Part-time",
            "location": "Dhaka Office",
            "vacancy": 2,
            "posted_date": date.today() - timedelta(days=5),
            "deadline": date.today() + timedelta(days=25),
            "short_description": "Maintain laboratory equipment and assist in the preparation of biological samples for high-throughput sequencing.",
            "job_overview": "<p>We need an organized and meticulous Lab Technician to support our core research facilities. You will be responsible for daily operations, ensuring that the lab runs efficiently and safely.</p>",
            "required_profile": "<ul><li>BSc in Biology, Chemistry, or related field.</li><li>Experience with pipetting and sample preparation.</li><li>Knowledge of lab safety protocols.</li></ul>",
            "role_description": "<ul><li><strong>Sample Prep:</strong> Prepare samples for NGS and other assays.</li><li><strong>Maintenance:</strong> Calibrate and clean instruments daily.</li><li><strong>Inventory Management:</strong> Track and order reagents.</li></ul>",
            "salary_info": "<p>Hourly wage with flexible scheduling options.</p>"
        },
        {
            "title": "Backend Systems Engineer",
            "employment_type": "Full-time",
            "location": "Remote",
            "vacancy": 1,
            "posted_date": date.today() - timedelta(days=2),
            "deadline": date.today() + timedelta(days=28),
            "short_description": "Architect and optimize cloud-native bioinformatics pipelines capable of processing terabytes of data daily with 99.9% reliability.",
            "job_overview": "<p>Join our engineering team to build scalable backends for our computational pipelines. You'll ensure our systems can handle terabytes of genomic data securely and rapidly.</p>",
            "required_profile": "<ul><li>BS/MS in Computer Science or equivalent.</li><li>Expertise in Python, Django, and PostgreSQL.</li><li>Experience with AWS, Docker, and Kubernetes.</li></ul>",
            "role_description": "<ul><li><strong>Architecture:</strong> Design robust microservices for bioinformatics tasks.</li><li><strong>Optimization:</strong> Improve pipeline throughput and reduce compute costs.</li></ul>",
            "salary_info": "<p>Competitive salary with performance bonuses.</p>"
        }
    ]
    
    Carrier.objects.all().delete()
    for c in carriers:
        Carrier.objects.create(**c)
    print("Successfully loaded Carrier demo data.")

if __name__ == '__main__':
    load_data()
