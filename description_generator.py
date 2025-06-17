import os
import re
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import html

load_dotenv()

force_elaboration = True

def clean_html_spacing(html):
    """
    Clean up HTML output by removing extra line breaks and spaces between <li> elements.
    Ensures tight spacing within <ul> lists while preserving spacing between sections.
    """
    cleaned_html = re.sub(r'</li>\s*<li>', '</li><li>', html)
    cleaned_html = re.sub(r'<ul>\s*', '<ul>', cleaned_html)
    cleaned_html = re.sub(r'\s*</ul>', '</ul>', cleaned_html)
    cleaned_html = re.sub(r'</ul>\s*<b>', '</ul><br><br><b>', cleaned_html)
    return cleaned_html

def generate_description(data):
    word_count = data.get("wordCount", 1000) or 1000
    company_type = data.get("companyType", "company")
    # Use the correct field name based on companyType
    post_type = (data.get("opportunityType", "") or "") if company_type == "company" else (data.get("postType", "") or "")
    company_name = (data.get("companyName", "") or "Individual").strip()
    title = html.escape(data.get("title", "") or "Untitled Role")
    skills = data.get("skills", []) or []
    keywords = data.get("keywords", []) or []
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",") if s.strip()]
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]

    # Combine important words for bolding (remove duplicates)
    important_words = list(set([company_name] + skills + keywords))
    important_words = [word for word in important_words if word]

    # Extract common fields
    location = data.get("location", "") or "Not specified"
    package = data.get("package", "") or "Competitive compensation"
    last_date = data.get("lastDate", "") or "Not specified"
    vacancy = data.get("vacancy", 1) if data.get("vacancy") and data.get("vacancy") > 0 else 1

    # Fields specific to "For My Company"
    work_duration = data.get("workDuration", "") or "Not specified"
    work_mode = data.get("workMode", "") or "Not specified"
    time_commitment = data.get("timeCommitment", "") or "Not specified"

    # Fields specific to "Individual"
    eligibility = data.get("eligibility", "") or "Not specified"

    # LLM setup
    llm = ChatGroq(
        temperature=0.7,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-70b-8192"
    )

    # Common prompt data
    prompt_data = {
        "companyName": company_name,
        "title": title,
        "postType": post_type or "Generic Role",
        "location": location,
        "package": package,
        "lastDate": last_date,
        "vacancy": vacancy,
        "skills": ", ".join(skills) if skills else "Not specified",
        "keywords": ", ".join(keywords) if keywords else "Not specified",
        "workDuration": work_duration,
        "workMode": work_mode,
        "timeCommitment": time_commitment,
        "eligibility": eligibility
    }

    # Define formats based on companyType and postType
    if company_type == "company":
        # "For My Company" formats
        if not post_type:
            intro_instruction = "Generate a generic job description for a role. The tone should be professional and adaptable to any job type."
            format_instruction = """
Format:
<b>Company:</b> {companyName}<br>
<b>Location:</b> {location}<br>
<b>Work Mode:</b> {workMode}<br>
<b>Role:</b> {title}<br>

<b>About the Opportunity:</b>  
[Brief intro to the role and company.]

<b>Responsibilities:</b>  
<ul>
    <li>[List of duties (if provided, otherwise generic duties).]</li>
</ul>

<b>Skills & Qualifications:</b>  
<ul>
    <li>[List of skills (if provided, otherwise generic skills).]</li>
</ul>
"""
        elif post_type == "Full time":
            intro_instruction = "Generate a professional full-time job description targeted at attracting qualified candidates. The tone should be formal, aspirational, and highlight long-term career growth, company culture, and stability."
            format_instruction = """
Format:
<b>Company:</b> {companyName}<br>  
<b>Location:</b> {location}<br>
<b>Work Mode:</b> {workMode}<br> 
<b>Job Type:</b> Full-Time <br><br> 

<b>About the Company:</b>  
[Brief intro to the company, culture, and mission.]

<b>Roles & Responsibilities:</b>  
<ul>
    <li>[List of job duties.]</li>
</ul>

<b>Required Skills & Qualifications:</b>  
<ul>
    <li>[List of skills and qualifications.]</li>
</ul>

<b>Benefits:</b>  
<ul>
    <li>[Perks like health insurance, paid leave, etc.]</li>
</ul>
"""
        elif post_type == "Part time":
            intro_instruction = "Generate a clear and professional part-time job description. Highlight flexible hours, key responsibilities, and the specific time commitment required. Keep the tone friendly yet informative."
            format_instruction = """
Format:
<b>Company:</b> {companyName}<br>  
<b>Location:</b> {location}<br> 
<b>Work Mode:</b> {workMode}<br> 
<b>Job Type:</b> Part-Time <br><br> 

<b>About the Role:</b>  
[Brief about the role and work hours.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties.]</li>
</ul>

<b>Qualifications & Skills:</b>  
<ul>
    <li>[List key skills.]</li>
</ul>

<b>Perks:</b>  
<ul>
    <li>[Highlight work-life balance, flexibility.]</li>
</ul>
"""
        elif post_type == "Internship (Stipend)":
            intro_instruction = "Create a paid internship post that is inviting to students or fresh graduates. Emphasize learning, mentorship, potential growth opportunities, and the stipend as a financial incentive. Keep the tone encouraging and professional."
            format_instruction = """
Format: 
<b>Company:</b> {companyName}<br>   
<b>Location:</b> {location}<br>   
<b>Work Mode:</b> {workMode}<br>   
<b>Internship Type:</b> Paid Internship  <br><br> 

<b>About the Company:</b>  
[Brief overview.]

<b>Internship Overview:</b>  
[What interns will work on.]

<b>Learning Opportunities:</b>  
<ul>
    <li>[List skills interns will develop.]</li>
</ul>

<b>Requirements:</b>  
<ul>
    <li>[Eligibility, background, or tools.]</li>
</ul>

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties.]</li>
</ul>

<b>Duration:</b> {workDuration}  
"""
        elif post_type == "Internship (Unpaid)":
            intro_instruction = "Create an unpaid internship post that is inviting to students or fresh graduates. Emphasize learning, mentorship, networking opportunities, and other non-monetary benefits to attract candidates. Keep the tone encouraging and professional."
            format_instruction = """
Format: 
<b>Company:</b> {companyName}<br>   
<b>Location:</b> {location}<br> 
<b>Work Mode:</b> {workMode}<br>   
<b>Internship Type:</b> Unpaid Internship  <br><br> 

<b>About the Company:</b>  
[Brief overview.]

<b>Internship Overview:</b>  
[What interns will work on.]

<b>Learning Opportunities:</b>  
<ul>
    <li>[List skills interns will develop.]</li>
</ul>

<b>Requirements:</b>  
<ul>
    <li>[Eligibility, background, or tools.]</li>
</ul>

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties.]</li>
</ul>

<b>Non-Monetary Benefits:</b>  
<ul>
    <li>[Highlight mentorship, networking, certificates, etc.]</li>
</ul>

<b>Duration:</b> {workDuration}  
"""
        elif post_type == "Contract":
            intro_instruction = "Generate a professional contract opportunity post. Focus on short-term project deliverables, duration, and payment. It is not a job. The tone should appeal to freelancers or short-term collaborators."
            format_instruction = """
Format:
<b>Contract Role:</b> {title}<br>   
<b>Location:</b> {location}<br> 
<b>Work Mode:</b> {workMode}<br>  
<b>Type:</b> Contract-Based ({workDuration})<br><br> 

<b>Overview:</b>  
[Short intro to project.]

<b>Responsibilities:</b>  
<ul>
    <li>[List of deliverables.]</li>
</ul>

<b>Requirements:</b>  
<ul>
    <li>[Tools, skills, experience needed.]</li>
</ul>

<b>Contract Duration:</b> {workDuration}  
"""
        elif post_type == "Project (freelancers)":
            intro_instruction = "Generate a project collaboration post for individual freelancers. This is not a job but an opportunity for freelancers to contribute to a specific project with clear goals and timelines. Focus on skillset needed, project objectives, and payment terms. Keep the tone flexible and appealing to independent professionals."
            format_instruction = """
Format:
<b>Company Name:</b> {companyName}<br>  
<b>Location:</b> {location}<br>   
<b>Work Mode:</b> {workMode}<br> br>   

<b>Project Overview:</b>  
[Summary of the project, its impact, and goals.]

<b>Who We're Looking For:</b>  
[Type of freelancers, e.g., independent professionals with specific skills.]

<b>Required Skills:</b>  
<ul>
    <li>[List of technical/non-technical skills.]</li>
</ul>

<b>Timeline:</b> {workDuration}  
"""
        elif post_type == "Project (Service companies)":
            intro_instruction = "Generate a project collaboration post for service companies. This is not a job but an opportunity for companies to collaborate on a specific project with clear goals and timelines. Focus on partnership potential, project scale, and required expertise. Keep the tone formal and professional."
            format_instruction = """
Format:
<b>Company Name:</b> {companyName}<br>  
<b>Location:</b> {location}<br>   
<b>Work Mode:</b> {workMode}<br><br>   

<b>Project Overview:</b>  
[Summary of the project, its impact, and goals.]

<b>Who We're Looking For:</b>  
[Type of service companies, e.g., agencies or firms with specific expertise.]

<b>Required Expertise:</b>  
<ul>
    <li>[List of technical/non-technical expertise required.]</li>
</ul>

<b>Collaboration Scope:</b>  
[Details on how the collaboration will work.]

<b>Timeline:</b> {workDuration}  
"""
        else:
            intro_instruction = "Generate a generic job description for a role. The tone should be professional and adaptable to any job type."
            format_instruction = """
Format:
<b>Company:</b> {companyName}<br>   
<b>Location:</b> {location}<br>  
<b>Work Mode:</b> {workMode}<br>   
<b>Role:</b> {title}<br><br> 

<b>About the Opportunity:</b>  
[Brief intro to the role and company.]

<b>Responsibilities:</b>  
<ul>
    <li>[List of duties (if provided, otherwise generic duties).]</li>
</ul>

<b>Skills & Qualifications:</b>  
<ul>
    <li>[List of skills (if provided, otherwise generic skills).]</li>
</ul>
"""
    else:
        # "Individual" formats for "Create New Opportunity"
        if not post_type:
            intro_instruction = "Generate a generic opportunity description for an individual seeking collaboration. The tone should be professional yet approachable, focusing on the individual's goals and the opportunity's purpose."
            format_instruction = """
Format:
<b>Posted By:</b> {companyName}<br>  
<b>Location:</b> {location}<br>    
<b>Opportunity:</b> {title}<br> 
<b>Application Deadline:</b> {lastDate}<br>   
<b>Vacancies:</b> {vacancy}<br><br> 

<b>About Me:</b>  
[Brief intro to the individual and their goals.]

<b>About the Role:</b>  
[Brief intro to the opportunity and its purpose.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties (if provided, otherwise generic duties).]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List of skills (if provided, otherwise generic skills).]</li>
</ul>

<b>Nice to Have:</b>  
<ul>
    <li>[List of optional skills or experiences.]</li>
</ul>

<b>Perks & Benefits:</b>  
<ul>
    <li>[Details about the package and any additional benefits.]</li>
</ul>

<b>Eligibility:</b>  
<ul>
    <li>[Details about eligibility criteria.]</li>
</ul>
"""
        elif post_type == "Full time":
            intro_instruction = "Generate a professional full-time opportunity description for an individual seeking a long-term collaborator. The tone should be approachable yet formal, emphasizing the individual's vision, the role's impact, and opportunities for growth."
            format_instruction = """
Format:
<b>Posted By:</b> {companyName}<br>   
<b>Location:</b> {location}<br>  
<b>Job Type:</b> Full-Time  
<b>Application Deadline:</b> {lastDate}<br>  
<b>Vacancies:</b> {vacancy}<br><br>  

<b>About Me:</b>  
[Brief intro to the individual, their vision, and passion for the project.]

<b>About the Role:</b>  
[Details about the role, its impact, and long-term potential.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of job duties relevant to a full-time role.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List of skills and qualifications.]</li>
</ul>

<b>Nice to Have:</b>  
<ul>
    <li>[List of optional skills or experiences, e.g., additional technical skills or domain knowledge.]</li>
</ul>

<b>Perks & Benefits:</b>  
<ul>
    <li>[Details about the package, e.g., salary, and any collaboration opportunities.]</li>
</ul>

<b>Eligibility:</b>  
<ul>
    <li>[Details about eligibility criteria.]</li>
</ul>
"""
        elif post_type == "Part time":
            intro_instruction = "Generate a clear and professional part-time opportunity description for an individual seeking a flexible collaborator. Highlight the role's flexibility, key responsibilities, and the individual's support, with a friendly yet professional tone."
            format_instruction = """
Format:
<b>Posted By:</b> {companyName}<br> 
<b>Location:</b> {location}<br>  
<b>Job Type:</b> Part-Time  
<b>Application Deadline:</b> {lastDate}<br>  
<b>Vacancies:</b> {vacancy}<br><br> 

<b>About Me:</b>  
[Brief intro to the individual and their goals.]

<b>About the Role:</b>  
[Brief about the role, its flexibility, and expected time commitment.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties tailored for a part-time role.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List key skills.]</li>
</ul>

<b>Nice to Have:</b>  
<ul>
    <li>[List of optional skills or experiences, e.g., prior experience in similar roles.]</li>
</ul>

<b>Perks & Benefits:</b>  
<ul>
    <li>[Details about the package, e.g., hourly rate, and benefits like flexible hours.]</li>
</ul>

<b>Eligibility:</b>  
<ul>
    <li>[Details about eligibility criteria.]</li>
</ul>
"""
        elif post_type == "Internship (Stipend)":
            intro_instruction = "Create a paid internship opportunity description for an individual seeking a learner. Emphasize the learning opportunities, mentorship, and stipend, with an encouraging and professional tone focused on growth and development."
            format_instruction = """
Format: 
<b>Posted By:</b> {companyName}<br> 
<b>Location:</b> {location}<br>   
<b>Internship Type:</b> Paid Internship <br>  
<b>Application Deadline:</b> {lastDate}<br>   
<b>Vacancies:</b> {vacancy}<br><br>   

<b>About Me:</b>  
[Brief overview of the individual and their commitment to mentoring.]

<b>About the Role:</b>  
[What interns will work on and learn.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties for the internship.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List of skills, e.g., basic knowledge of tools or technologies.]</li>
</ul>

<b>Nice to Have:</b>  
<ul>
    <li>[List of optional skills, e.g., familiarity with specific software.]</li>
</ul>

<b>Perks & Benefits:</b>  
<ul>
    <li>[Details about the stipend and learning opportunities.]</li>
</ul>

<b>Eligibility:</b>  
<ul>
    <li>[Details about eligibility criteria.]</li>
</ul>
"""
        elif post_type == "Internship (Unpaid)":
            intro_instruction = "Create an unpaid internship opportunity description for an individual seeking a learner. Emphasize the learning opportunities, networking benefits, and non-monetary perks, with an encouraging and professional tone focused on growth."
            format_instruction = """
Format: 
<b>Posted By:</b> {companyName}<br>   
<b>Location:</b> {location}<br> 
<b>Internship Type:</b> Unpaid Internship <br> 
<b>Application Deadline:</b> {lastDate}<br> 
<b>Vacancies:</b> {vacancy}<br><br> 

<b>About Me:</b>  
[Brief overview of the individual and their commitment to mentoring.]

<b>About the Role:</b>  
[What interns will work on and learn.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties for the internship.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List of skills, e.g., basic knowledge of tools or technologies.]</li>
</ul>

<b>Nice to Have:</b>  
<ul>
    <li>[List of optional skills, e.g., familiarity with specific software.]</li>
</ul>

<b>Perks & Benefits:</b>  
<ul>
    <li>[Highlight networking opportunities, certificates, mentorship, etc.]</li>
</ul>

<b>Eligibility:</b>  
<ul>
    <li>[Details about eligibility criteria.]</li>
</ul>
"""
        elif post_type == "Contract":
            intro_instruction = "Generate a professional contract opportunity description for an individual seeking a short-term collaborator. Focus on the project's deliverables, timeline, and compensation, with a professional tone appealing to freelancers."
            format_instruction = """
Format:
<b>Posted By:</b> {companyName}<br> 
<b>Location:</b> {location}<br>   
<b>Opportunity Type:</b> Contract-Based <br>  
<b>Application Deadline:</b> {lastDate}<br> 
<b>Vacancies:</b> {vacancy}<br><br> 

<b>About Me:</b>  
[Brief overview of the individual and their project.]

<b>About the Role:</b>  
[Short intro to the project and its goals.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of deliverables for the contract.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[Tools, skills, experience needed.]</li>
</ul>

<b>Nice to Have:</b>  
<ul>
    <li>[List of optional skills, e.g., prior contract work experience.]</li>
</ul>

<b>Perks & Benefits:</b>  
<ul>
    <li>[Details about the package and any additional benefits.]</li>
</ul>

<b>Eligibility:</b>  
<ul>
    <li>[Details about eligibility criteria.]</li>
</ul>
"""
        elif post_type == "Project (freelancers)":
            intro_instruction = "Generate a project collaboration opportunity description for an individual seeking freelancers. Focus on the project's goals, required skills, and appeal to independent professionals, with a flexible and approachable tone."
            format_instruction = """
Format:
<b>Posted By:</b> {companyName}<br>  
<b>Location:</b> {location}<br> 
<b>Opportunity Type:</b> Project for Freelancers <br>  
<b>Application Deadline:</b> {lastDate}<br> 
<b>Vacancies:</b> {vacancy}<br><br> 

<b>About Me:</b>  
[Brief overview of the individual and their vision.]

<b>About the Role:</b>  
[Summary of the project, its impact, and goals.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of tasks for the project.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List of technical/non-technical skills.]</li>
</ul>

<b>Nice to Have:</b>  
<ul>
    <li>[List of optional skills, e.g., experience with similar projects.]</li>
</ul>

<b>Perks & Benefits:</b>  
<ul>
    <li>[Details about the package and any additional benefits.]</li>
</ul>

<b>Eligibility:</b>  
<ul>
    <li>[Details about eligibility criteria.]</li>
</ul>
"""
        elif post_type == "Project (Service companies)":
            intro_instruction = "Generate a project collaboration opportunity description for an individual seeking service companies. Focus on the project's scale, partnership potential, and required expertise, with a formal and professional tone."
            format_instruction = """
Format:
<b>Posted By:</b> {companyName}<br>   
<b>Location:</b> {location}<br> 
<b>Opportunity Type:</b> Project for Service Companies <br> 
<b>Application Deadline:</b> {lastDate}<br>   
<b>Vacancies:</b> {vacancy}<br> 

<b>About Me:</b>  
[Brief overview of the individual and their vision.]

<b>About the Role:</b>  
[Summary of the project, its impact, and goals.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of responsibilities for the collaboration.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List of technical/non-technical expertise required.]</li>
</ul>

<b>Nice to Have:</b>  
<ul>
    <li>[List of optional expertise, e.g., experience in similar collaborations.]</li>
</ul>

<b>Perks & Benefits:</b>  
<ul>
    <li>[Details about the package and any additional benefits.]</li>
</ul>

<b>Eligibility:</b>  
<ul>
    <li>[Details about eligibility criteria.]</li>
</ul>
"""
        else:
            intro_instruction = "Generate a generic opportunity description for an individual seeking collaboration. The tone should be professional yet approachable, focusing on the individual's goals and the opportunity's purpose."
            format_instruction = """
Format:
<b>Posted By:</b> {companyName}<br>   
<b>Location:</b> {location}<br> 
<b>Opportunity:</b> {title}<br> 
<b>Application Deadline:</b> {lastDate}<br>  
<b>Vacancies:</b> {vacancy}<br> 

<b>About Me:</b>  
[Brief intro to the individual and their goals.]

<b>About the Role:</b>  
[Brief intro to the opportunity and its purpose.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties (if provided, otherwise generic duties).]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List of skills (if provided, otherwise generic skills).]</li>
</ul>

<b>Nice to Have:</b>  
<ul>
    <li>[List of optional skills or experiences.]</li>
</ul>

<b>Perks & Benefits:</b>  
<ul>
    <li>[Details about the package and any additional benefits.]</li>
</ul>

<b>Eligibility:</b>  
<ul>
    <li>[Details about eligibility criteria.]</li>
</ul>
"""

    # Full prompt with dynamic instructions
    prompt = ChatPromptTemplate.from_template(f"""
    {intro_instruction}

    Generate a professional and polished opportunity post using the following details:

    - Company Name: {{companyName}}
    - Post Type: {{postType}}
    - Location: {{location}}
    - Job Title: {{title}}
    - Package: {{package}}
    - Last Date: {{lastDate}}
    - Vacancy: {{vacancy}}
    - Skills: {{skills}}
    - Keywords: {{keywords}}
    - Work Duration: {{workDuration}}
    - Work Mode: {{workMode}}
    - Time Commitment: {{timeCommitment}}
    - Eligibility: {{eligibility}}

    Important words to bold: {', '.join(important_words) if important_words else 'None'}

    {format_instruction}

    Instructions:
    - Use only <b>, not ** for bold.
    - Your response should be suitable for direct copy-pasting into a web page or email client that supports HTML formatting. Use only valid HTML tags.
    - Use bullet points where appropriate.
    - For all <ul> lists, ensure there are NO extra line breaks or spaces between <li> elements.
    - Ensure exactly two <br> tags between sections for clean spacing.
    - Output should be ready to copy-paste into LinkedIn/email without editing.
    - Use the company name naturally — don’t include 'companyType'.
    - Strictly follow the format provided above. Do NOT add extra fields or sections.
    - Within paragraph sections, bold the important words listed above using <b> tags. Do NOT bold words within <ul> lists.
    - Ensure the response is at least {word_count} words. Expand each section thoughtfully with relevant details.
    - Make the tone fit the nature of the role (e.g., formal for full-time, friendly for internships).
    - If any field is missing or empty, use generic placeholders (e.g., 'Not specified' for location, 'Competitive compensation' for package).
    -DO NOT MENTION THIS IN DESCRIPTION "Note: The output is ready to copy-paste into a web page or email client that supports HTML formatting. I've followed the provided format and instructions, and the response is at least 1000 words".
    """)

    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(prompt_data)
    cleaned_response = clean_html_spacing(response)
    return cleaned_response

def generate_pass_opportunity_description(data):
    word_count = data.get("wordCount", 1000) or 1000
    company_type = data.get("companyType", "company")
    company_name = (data.get("companyName", "") or "Individual").strip()
    opportunity_title = html.escape(data.get("opportunityTitle", "") or "Untitled Opportunity")
    opportunity_type = data.get("opportunityType", "") or "Not specified"
    skills = data.get("skillsRequired", []) or []
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",") if s.strip()]

    # Combine important words for bolding (remove duplicates)
    important_words = list(set([company_name] + skills))
    important_words = [word for word in important_words if word]

    # Extract common fields
    location = data.get("location", "") or "Not specified"
    number_of_openings = data.get("numberOfOpenings", 1) if data.get("numberOfOpenings") and data.get("numberOfOpenings") > 0 else 1
    last_date = data.get("lastDate", "") or "Not specified"

    # Fields specific to "For My Company"
    work_mode = data.get("workMode", "") or "Not specified"
    time_commitment = data.get("timeCommitment", "") or "Not specified"

    # LLM setup
    llm = ChatGroq(
        temperature=0.7,
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-70b-8192"
    )

    # Common prompt data
    prompt_data = {
        "companyName": company_name,
        "opportunityTitle": opportunity_title,
        "opportunityType": opportunity_type,
        "location": location,
        "numberOfOpenings": number_of_openings,
        "lastDate": last_date,
        "skillsRequired": ", ".join(skills) if skills else "Not specified",
        "important_words": ", ".join(important_words) if important_words else "None",
        "workMode": work_mode,
        "timeCommitment": time_commitment
    }

    # Define formats based on companyType and opportunityType for "Pass an Opportunity"
    if company_type == "company":
        # "For My Company" formats
        if not opportunity_type:
            intro_instruction = "Generate a generic job description for an opportunity being passed to potential candidates. The tone should be professional and highlight why this opportunity is worth considering."
            format_instruction = """
Format:
<b>Company:</b> {companyName}<br>
<b>Location:</b> {location}<br>
<b>Work Mode:</b> {workMode}<br>  
<b>Opportunity:</b> {opportunityTitle}<br><br> 

<b>About the Opportunity:</b>  
[Brief intro to the opportunity and why it's unique.]

<b>Responsibilities:</b>  
<ul>
    <li>[List of duties.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List of skills.]</li>
</ul>
"""
        elif opportunity_type == "Full time":
            intro_instruction = "Generate a professional full-time job description for an opportunity being passed to potential candidates. The tone should be formal and emphasize the company's reputation and the role's impact."
            format_instruction = """
Format:
<b>Company:</b> {companyName}<br>  
<b>Location:</b> {location}<br>
<b>Work Mode:</b> {workMode}<br> 
<b>Job Type:</b> Full-Time <br><br>

<b>About the Company:</b>  
[Brief intro to the company and its reputation.]

<b>About the Role:</b>  
[Details about the role and its impact.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of job duties.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List of skills.]</li>
</ul>

<b>Benefits:</b>  
<ul>
    <li>[Perks like health insurance, professional development.]</li>
</ul>
"""
        elif opportunity_type == "Part time":
            intro_instruction = "Generate a clear and professional part-time job description for an opportunity being passed to potential candidates. Highlight the role's flexibility and the company's support for work-life balance."
            format_instruction = """
Format:
<b>Company:</b> {companyName}<br>
<b>Location:</b> {location}<br>
<b>Work Mode:</b> {workMode}<br>
<b>Job Type:</b> Part-Time <br><br>

<b>About the Role:</b>  
[Brief about the role and its flexibility.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List key skills.]</li>
</ul>

<b>Perks:</b>  
<ul>
    <li>[Highlight flexibility, work-life balance.]</li>
</ul>
"""
        elif opportunity_type == "Internship (Stipend)":
            intro_instruction = "Create a paid internship opportunity for passing to potential candidates. Emphasize the learning experience, mentorship, and the stipend, with a tone that is encouraging and professional."
            format_instruction = """
Format: 
<b>Company:</b> {companyName}<br>
<b>Location:</b> {location}<br>
<b>Work Mode:</b> {workMode}<br>
<b>Internship Type:</b> Paid Internship <br><br>

<b>About the Company:</b>  
[Brief overview.]

<b>Internship Opportunity:</b>  
[What interns will work on.]

<b>Learning Benefits:</b>  
<ul>
    <li>[List skills interns will gain.]</li>
</ul>

<b>Requirements:</b>  
<ul>
    <li>[Eligibility, background, or tools.]</li>
</ul>

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties.]</li>
</ul>
"""
        elif opportunity_type == "Internship (Unpaid)":
            intro_instruction = "Create an unpaid internship opportunity for passing to potential candidates. Emphasize the learning experience, networking opportunities, and non-monetary benefits, with a tone that is encouraging and professional."
            format_instruction = """
Format: 
<b>Company:</b> {companyName}<br>
<b>Location:</b> {location}<br>
<b>Work Mode:</b> {workMode}<br>
<b>Internship Type:</b> Unpaid Internship <br><br> 

<b>About the Company:</b>  
[Brief overview.]

<b>Internship Opportunity:</b>  
[What interns will work on.]

<b>Learning Benefits:</b>  
<ul>
    <li>[List skills interns will gain.]</li>
</ul>

<b>Requirements:</b>  
<ul>
    <li>[Eligibility, background, or tools.]</li>
</ul>

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties.]</li>
</ul>

<b>Non-Monetary Benefits:</b>  
<ul>
    <li>[Highlight mentorship, networking, etc.]</li>
</ul>
"""
        elif opportunity_type == "Contract":
            intro_instruction = "Generate a professional contract opportunity for passing to potential candidates. Focus on the project's deliverables and why it's a valuable opportunity for short-term collaborators."
            format_instruction = """
Format:
<b>Contract Opportunity:</b> {opportunityTitle}<br>  
<b>Location:</b> {location}<br>
<b>Work Mode:</b> {workMode}<br>
<b>Type:</b> Contract-Based <br><br>

<b>Overview:</b>  
[Short intro to the project.]

<b>Responsibilities:</b>  
<ul>
    <li>[List of deliverables.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[Tools, skills, experience needed.]</li>
</ul>
"""
        elif opportunity_type == "Project (freelancers)":
            intro_instruction = "Generate a project collaboration opportunity for freelancers to be passed to potential candidates. Focus on the project's goals, required skills, and why it's a great opportunity for independent professionals."
            format_instruction = """
Format:
<b>Company Name:</b> {companyName}<br> 
<b>Location:</b> {location}<br>
<b>Work Mode:</b> {workMode}<br><br> 

<b>Project Opportunity:</b>  
[Summary of the project and its goals.]

<b>Who We're Looking For:</b>  
[Type of freelancers with specific skills.]

<b>Required Skills:</b>  
<ul>
    <li>[List of technical/non-technical skills.]</li>
</ul>
"""
        elif opportunity_type == "Project (Service companies)":
            intro_instruction = "Generate a project collaboration opportunity for service companies to be passed to potential candidates. Focus on the project's scale, partnership potential, and required expertise, with a formal and professional tone."
            format_instruction = """
Format:
<b>Company Name:</b> {companyName}<br>  
<b>Location:</b> {location}<br>
<b>Work Mode:</b> {workMode}<br><br>

<b>Project Opportunity:</b>  
[Summary of the project and its goals.]

<b>Who We're Looking For:</b>  
[Type of service companies with specific expertise.]

<b>Required Expertise:</b>  
<ul>
    <li>[List of technical/non-technical expertise.]</li>
</ul>

<b>Collaboration Scope:</b>  
[Details on the collaboration.]
"""
        else:
            intro_instruction = "Generate a generic job description for an opportunity being passed to potential candidates. The tone should be professional and highlight why this opportunity is worth considering."
            format_instruction = """
Format:
<b>Company:</b> {companyName}<br>  
<b>Location:</b> {location}<br>  
<b>Work Mode:</b> {workMode}<br> 
<b>Opportunity:</b> {opportunityTitle}<br><br>

<b>About the Opportunity:</b>  
[Brief intro to the opportunity and why it's unique.]

<b>Responsibilities:</b>  
<ul>
    <li>[List of duties.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List of skills.]</li>
</ul>
"""
    else:
        # "Individual" formats
        if not opportunity_type:
            intro_instruction = "Generate a generic opportunity description for passing by an individual. The tone should be professional yet approachable, highlighting the opportunity's value."
            format_instruction = """
Format:
<b>Posted By:</b> {companyName}<br>  
<b>Location:</b> {location}<br>
<b>Opportunity:</b> {opportunityTitle}<br> 

<b>About the Opportunity:</b>  
[Brief intro to the opportunity and why it's unique.]

<b>Responsibilities:</b>  
<ul>
    <li>[List of duties.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List of skills.]</li>
</ul>
"""
        elif opportunity_type == "Full time":
            intro_instruction = "Generate a full-time opportunity description for passing by an individual. The tone should be approachable yet professional, emphasizing the individual's passion and the role's potential."
            format_instruction = """
Format:
<b>Posted By:</b> {companyName}<br>  
<b>Location:</b> {location}<br>
<b>Job Type:</b> Full-Time <br><br> 

<b>About Me:</b>  
[Brief intro to the individual and their passion.]

<b>About the Role:</b>  
[Details about the role and its potential.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of job duties.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List of skills.]</li>
</ul>

<b>Benefits:</b>  
<ul>
    <li>[Perks like collaboration opportunities.]</li>
</ul>
"""
        elif opportunity_type == "Part time":
            intro_instruction = "Generate a part-time opportunity description for passing by an individual. Highlight the role's flexibility and the individual's support, with a friendly yet professional tone."
            format_instruction = """
Format:
<b>Posted By:</b> {companyName}<br>  
<b>Location:</b> {location}<br>
<b>Job Type:</b> Part-Time <br><br>

<b>About the Role:</b>  
[Brief about the role and its flexibility.]

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List key skills.]</li>
</ul>

<b>Perks:</b>  
<ul>
    <li>[Highlight flexibility, collaboration opportunities.]</li>
</ul>
"""
        elif opportunity_type == "Internship (Stipend)":
            intro_instruction = "Create a paid internship opportunity for passing by an individual. Emphasize learning opportunities and the stipend, with an encouraging and professional tone."
            format_instruction = """
Format: 
<b>Posted By:</b> {companyName}<br>  
<b>Location:</b> {location}<br>
<b>Internship Type:</b> Paid Internship <br><br>

<b>About Me:</b>  
[Brief overview of the individual.]

<b>Internship Opportunity:</b>  
[What interns will work on.]

<b>Learning Benefits:</b>  
<ul>
    <li>[List skills interns will gain.]</li>
</ul>

<b>Requirements:</b>  
<ul>
    <li>[Eligibility, background, or tools.]</li>
</ul>

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties.]</li>
</ul>
"""
        elif opportunity_type == "Internship (Unpaid)":
            intro_instruction = "Create an unpaid internship opportunity for passing by an individual. Emphasize learning opportunities and non-monetary benefits, with an encouraging and professional tone."
            format_instruction = """
Format: 
<b>Posted By:</b> {companyName}<br>  
<b>Location:</b> {location}<br> 
<b>Internship Type:</b> Unpaid Internship <br><br>

<b>About Me:</b>  
[Brief overview of the individual.]

<b>Internship Opportunity:</b>  
[What interns will work on.]

<b>Learning Benefits:</b>  
<ul>
    <li>[List skills interns will gain.]</li>
</ul>

<b>Requirements:</b>  
<ul>
    <li>[Eligibility, background, or tools.]</li>
</ul>

<b>Key Responsibilities:</b>  
<ul>
    <li>[List of duties.]</li>
</ul>

<b>Non-Monetary Benefits:</b>  
<ul>
    <li>[Highlight networking, certificates, etc.]</li>
</ul>
"""
        elif opportunity_type == "Contract":
            intro_instruction = "Generate a contract opportunity for passing by an individual. Focus on the project's deliverables and value for short-term collaborators, with a professional tone."
            format_instruction = """
Format:
<b>Contract Opportunity:</b> {opportunityTitle}<br> 
<b>Location:</b> {location}<br>
<b>Type:</b> Contract-Based <br><br>

<b>Overview:</b>  
[Short intro to the project.]

<b>Responsibilities:</b>  
<ul>
    <li>[List of deliverables.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[Tools, skills, experience needed.]</li>
</ul>
"""
        elif opportunity_type == "Project (freelancers)":
            intro_instruction = "Generate a project collaboration opportunity for freelancers to be passed by an individual. Focus on the project's goals, required skills, and appeal to independent professionals."
            format_instruction = """
Format:
<b>Posted By:</b> {companyName}<br> 
<b>Location:</b> {location}<br>

<b>Project Opportunity:</b>  
[Summary of the project and its goals.]

<b>Who I'm Looking For:</b>  
[Type of freelancers with specific skills.]

<b>Required Skills:</b>  
<ul>
    <li>[List of technical/non-technical skills.]</li>
</ul>
"""
        elif opportunity_type == "Project (Service companies)":
            intro_instruction = "Generate a project collaboration opportunity for service companies to be passed by an individual. Focus on the project's scale, partnership potential, and required expertise, with a formal tone."
            format_instruction = """
Format:
<b>Posted By:</b> {companyName}<br>  
<b>Location:</b> {location}<br><br> 

<b>Project Opportunity:</b>  
[Summary of the project and its goals.]

<b>Who I'm Looking For:</b>  
[Type of service companies with specific expertise.]

<b>Required Expertise:</b>  
<ul>
    <li>[List of technical/non-technical expertise.]</li>
</ul>

<b>Collaboration Scope:</b>  
[Details on the collaboration.]
"""
        else:
            intro_instruction = "Generate a generic opportunity description for passing by an individual. The tone should be professional yet approachable, highlighting the opportunity's value."
            format_instruction = """
Format:
<b>Posted By:</b> {companyName}<br>  
<b>Location:</b> {location}<br>  
<b>Opportunity:</b> {opportunityTitle}<br><br> 

<b>About the Opportunity:</b>  
[Brief intro to the opportunity and why it's unique.]

<b>Responsibilities:</b>  
<ul>
    <li>[List of duties.]</li>
</ul>

<b>Required Skills:</b>  
<ul>
    <li>[List of skills.]</li>
</ul>
"""

    # Full prompt with dynamic instructions
    prompt = ChatPromptTemplate.from_template(f"""
    {intro_instruction}

    Generate a professional opportunity description for passing to potential candidates using the following details:

    - Company Name: {{companyName}}
    - Opportunity Title: {{opportunityTitle}}
    - Opportunity Type: {{opportunityType}}
    - Location: {{location}}
    - Work Mode: {{workMode}}
    - Number of Openings: {{numberOfOpenings}}
    - Last Date: {{lastDate}}
    - Skills Required: {{skillsRequired}}
    - Time Commitment: {{timeCommitment}}

    Important words to bold: {{important_words}}

    {format_instruction}

    Instructions:
    - Use only <b>, not ** for bold.
    - Your response should be suitable for direct copy-pasting into a web page or email client that supports HTML formatting. Use only valid HTML tags.
    - Use bullet points where appropriate.
    - For all <ul> lists, ensure there are NO extra line breaks or spaces between <li> elements.
    - Ensure exactly two <br> tags between sections for clean spacing.
    - Output should be ready to copy-paste into LinkedIn/email without editing.
    - Use the company name naturally — don’t include 'companyType'.
    - Strictly follow the format provided above. Do NOT add extra fields or sections.
    - Within paragraph sections, bold the important words listed above using <b> tags. Do NOT bold words within <ul> lists.
    - Ensure the response is at least {word_count} words. Expand each section thoughtfully with relevant details.
    - Make the tone fit the nature of the opportunity (e.g., formal for full-time, friendly for internships).
    - If any field is missing or empty, use generic placeholders (e.g., 'Not specified' for location).
    """)

    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(prompt_data)
    cleaned_response = clean_html_spacing(response)
    return cleaned_response