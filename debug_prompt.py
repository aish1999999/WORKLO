#!/usr/bin/env python3
"""
Debug script to test the OpenAI prompt and see if content is being modified
"""
import os
from openai import OpenAI
from resume_txt_converter import ResumeTextConverter
from dotenv import load_dotenv

load_dotenv()

def test_prompt():
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Convert master template
    converter = ResumeTextConverter()
    master_txt = converter.docx_to_structured_txt('./Master_template2.docx')
    
    # Test job details
    job_title = "Supply Chain Manager, PCB"
    job_description = """We are seeking a Supply Chain Manager to oversee PCB procurement and manufacturing operations. Key responsibilities include vendor management, inventory optimization, demand planning, quality control, and cost reduction initiatives. The ideal candidate will have experience with electronics manufacturing, supplier relationship management, and supply chain analytics."""
    keywords = "supply chain management; pcb manufacturing; vendor management; inventory optimization; demand planning; quality control; cost reduction; electronics manufacturing"
    
    # Use our updated prompt
    system_prompt = """You are an expert resume writer and ATS optimization specialist.
You will receive a structured resume in TXT format with section markers (===SECTION===).

⸻

🔒 Critical Formatting Rules
    •    Keep the EXACT same structure with identical ===SECTION=== markers.
    •    Do not add or delete sections. If a section is missing, output the marker and leave it empty.
    •    Only rewrite the content inside each section.
    •    Do not include a ===SUMMARY=== section.
    •    Ensure the final resume fits neatly on one page (approx. 500–550 words, fully filled without wasted white space).

⸻

📑 Section Order (MUST follow exactly)
    1.    HEADER
    2.    EDUCATION
    3.    PROFESSIONAL EXPERIENCE
    4.    PROJECTS
    5.    SKILLS

⸻

✍️ Rewrite Instructions
    •    Rewrite all bullet points, descriptions, and achievements to align with the target job description and requirements.
    •    Keep company names, universities, and school names unchanged.
    •    Update the job title in the HEADER to the role most aligned with the target job description.
    •    Integrate job description keywords naturally (avoid copy-paste).
    •    Use strong action verbs, quantified achievements, and concise language.
    •    Maintain professional tone and ATS readability.

⸻

📌 Professional Experience & Projects Requirements
    •    From the master resume template (2 pages), select enough roles/projects (3–4 minimum, more if needed) to ensure the total bullet point count is greater than 12.
    •    Always keep HEADER, EDUCATION, and SKILLS sections.
    •    Discard non-relevant roles/projects to enforce a strict one-page limit.
    •    For each job role or project:
    •    Write exactly 3 bullet points (if possible). If fewer than 3 are realistic, use the strongest 2, but ensure the total bullet count across the resume remains >12.
    •    Bullets must follow this story sequence:
    1.    What I did (the task or responsibility)
    2.    How I did it (methods, tools, systems, or collaborations used)
    3.    Measurable outcome (numbers, %, cost savings, time reduction, efficiency gains, quality improvements)
    •    Bullets must be concise (max 2 lines each).
    •    Use industry-relevant terminology for ATS alignment.
    •    Example structure for one role:
• Implemented lean manufacturing workflow across 2 assembly lines
• Applied VSM and Kanban to streamline material flow and reduce idle time
• Achieved 18% cycle time reduction and $240K annual savings

⸻

📌 Education Requirements
    •    Keep all institution names unchanged.
    •    Highlight coursework, honors, or projects only if directly relevant to the job description.
    •    Keep concise (no longer than 2–3 bullets if needed).

⸻

📌 Skills Requirements
    •    Skills section must match the target job description keywords while staying relevant to the candidate's profile.
    •    Avoid generic filler.
    •    Present skills as a clear list (comma-separated or line-based, not paragraphs)."""
    
    user_prompt = f"""### Job Title:
{job_title}

### Job Description:
{job_description}

### Target Keywords (ranked most→least important):
{keywords}

### Master Resume in Structured Format:
{master_txt}

**Return ONLY the complete structured resume text with the same ===SECTION=== markers, following the system instructions above.**"""
    
    print("=== SENDING REQUEST TO OPENAI ===")
    print("System Prompt Length:", len(system_prompt))
    print("User Prompt Length:", len(user_prompt))
    print("\n=== MAKING API CALL ===")
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=4000
    )
    
    tailored_content = response.choices[0].message.content
    
    print("\n=== ORIGINAL MASTER TEMPLATE ===")
    print(master_txt)
    
    print("\n=== TAILORED CONTENT FROM AI ===")
    print(tailored_content)
    
    print("\n=== COMPARISON CHECK ===")
    if master_txt.strip() == tailored_content.strip():
        print("❌ PROBLEM: Content is identical - AI did not modify the resume!")
    else:
        print("✅ SUCCESS: Content was modified by AI")
        
    return tailored_content

if __name__ == "__main__":
    test_prompt()