#!/usr/bin/env python3
"""
Test script to generate a cover letter for a single job - demonstrates the new format
"""

import sys
import os
sys.path.append('.')

from automated_cover_letter import CoverLetterTailor

def test_single_cover_letter():
    """Test resume-aware cover letter generation for a single Manufacturing Controls Engineer role"""

    print("=" * 80)
    print("TESTING RESUME-AWARE COVER LETTER GENERATION")
    print("=" * 80)

    # Sample job data (similar to what comes from your Google Sheet)
    job_data = {
        'JOB_TITLE': 'Manufacturing Controls Development Engineer',
        'COMPANY': 'Tesla',
        'JOB_DESCRIPTION': '''
Tesla is seeking a Manufacturing Controls Development Engineer to join our Megapack production team.
This role will focus on developing and implementing advanced control systems for automated manufacturing processes.

Key Responsibilities:
- Design and develop PLC programs using Siemens TIA Portal and Allen-Bradley Studio 5000
- Implement SCADA systems using Ignition platform for real-time monitoring
- Integrate industrial robots (Fanuc, KUKA) into production workflows
- Develop HMI interfaces for operator interaction and process visualization
- Troubleshoot complex electro-mechanical systems and automation equipment
- Ensure compliance with Tesla's strict quality and safety standards
- Collaborate with cross-functional teams on continuous process improvement
- Support factory acceptance testing and commissioning activities

Required Qualifications:
- Bachelor's degree in Electrical, Mechanical, or Industrial Engineering
- 3+ years experience in manufacturing controls and industrial automation
- Proficiency in PLC programming (ladder logic, structured text, function block)
- Experience with SCADA platforms (Ignition preferred, WinCC acceptable)
- Knowledge of industrial communication protocols (PROFINET, EtherCAT, Ethernet/IP)
- Familiarity with robotics programming and machine vision systems
- Understanding of lean manufacturing principles and Industry 4.0 concepts
        ''',
        'KEYWORDS_RAW': [
            {'term': 'plc programming', 'rank': 1},
            {'term': 'scada systems', 'rank': 2},
            {'term': 'industrial automation', 'rank': 3},
            {'term': 'manufacturing controls', 'rank': 4},
            {'term': 'robotics integration', 'rank': 5},
            {'term': 'hmi development', 'rank': 6},
            {'term': 'process optimization', 'rank': 7},
            {'term': 'quality systems', 'rank': 8}
        ]
    }

    print(f"🎯 Target Job: {job_data['JOB_TITLE']}")
    print(f"🏢 Company: {job_data['COMPANY']}")
    print(f"🔑 Keywords: {[kw['term'] for kw in job_data['KEYWORDS_RAW']]}")
    print()

    # Initialize the cover letter tailor
    print("🔧 Initializing CoverLetterTailor...")
    tailor = CoverLetterTailor(dry_run=False)  # Set to False for real generation

    try:
        print("✍️  Generating resume-aware tailored cover letter...")
        print("   (This may take 30-60 seconds for AI processing)")

        # Extract actual resume content for evidence-based generation
        resume_content = """
        Aishwaryeshwar Manickavel
        ayeshwarm@gmail.com | 832-775-2886 | www.linkedin.com/in/aishwarnick

        EDUCATION
        University of Houston | Master of Science in Industrial Engineering | Houston, TX, USA | December 2025
        PSG College of Technology | Bachelor of Engineering in Metallurgical Engineering | TN, India | July 2023

        PROFESSIONAL EXPERIENCE
        University of Houston | Operations Lead | Houston, TX | USA | May 2024 – Feb 2025
        • Optimized workforce scheduling algorithms using demand forecasting and resource allocation strategies, improving staff utilization by 20% while maintaining service quality standards.
        • Reduced operational downtime by 15% through implementation of preventive maintenance protocols and real-time equipment tracking systems, saving $8,000+ in potential revenue loss.
        • Managed end-to-end event logistics for 25+ campus events per semester, ensuring 100% safety compliance and coordinating cross-functional teams of 15+ staff members.

        Centre for Automotive Energy Materials at IIT Madras | Industrial Manufacturing Controls Engineer | Chennai, TN | India | January 2023 -- December 2023
        • Developed next-generation control systems integrating PLC logic with modern software stacks, enhancing equipment efficiency by 30% during initial mass production phases.
        • Led supplier design reviews and factory acceptance testing for new manufacturing equipment, ensuring successful project delivery and reducing time-to-market by 25%.
        • Collaborated with cross-functional teams to troubleshoot and optimize electro-mechanical devices, achieving a 20% reduction in operational failures during production ramp-up.
        • Designed electrical schematics using ePLAN, streamlining the equipment setup process and improving compliance with Tesla's hardware and software standards by 15%.

        A. V.C Pvt Ltd. | Industrial Manufacturing Controls Engineer | TN, India | January 2021 -- May 2022
        • Implemented programming solutions for industrial robots (Fanuc, KUKA) that improved automation efficiency by 40%, significantly reducing manual labor costs.
        • Managed the commissioning of full-scale production equipment, achieving a 95% success rate in initial testing and minimizing downtime during ramp-up phases.
        • Optimized troubleshooting processes for electro-mechanical devices, resulting in a 30% decrease in repair time and enhancing overall production reliability.
        • Executed comprehensive training programs for staff on using diagnostic tools and hand tools, leading to a 50% improvement in maintenance response times.

        TECHNICAL SKILLS
        Control Systems Development: PLC Programming (Siemens, Allen-Bradley), Ladder Logic, Structured Text
        Robotics Programming: Industrial Robots (Fanuc, KUKA), Automation Solutions
        Electrical Design: ePLAN, AutoCAD, Electrical Schematic Design
        Manufacturing Processes: Mass Production, Equipment Commissioning, Preventive Maintenance
        Troubleshooting: Electro-Mechanical Devices, Diagnostic Tools, Multimeters
        Project Management: Supplier Coordination, Cross-Functional Collaboration, Factory Acceptance Testing
        """

        # Generate the cover letter with resume content
        cover_letter_path = tailor.generate_cover_letter(
            base_cover_letter_path='./base_cover_letter_new.docx',
            master_cover_letter_template_path='./master_cover_letter_template_fixed.docx',
            job_title=job_data['JOB_TITLE'],
            job_description=job_data['JOB_DESCRIPTION'],
            keywords=job_data['KEYWORDS_RAW'],
            company_name=job_data['COMPANY'],
            extra_prompt_instructions='Focus on evidence-based achievements and natural voice. Avoid buzzwords.',
            resume_content=resume_content
        )

        if cover_letter_path:
            print(f"✅ SUCCESS! Cover letter generated: {cover_letter_path}")

            # Upload to Google Drive
            drive_folder_id = '1PCBjveFtn07ljJyIhmVjwlwWwPZ7hoFr'  # Your specified folder
            print(f"📤 Uploading to Google Drive folder: {drive_folder_id}")

            cover_letter_drive_link = tailor.upload_to_drive(cover_letter_path, drive_folder_id)
            if cover_letter_drive_link:
                print(f"✅ Cover letter uploaded to Drive: {cover_letter_drive_link}")
            else:
                print("❌ Failed to upload cover letter to Drive")

            # Try to show a preview of the generated content
            try:
                from docx import Document
                doc = Document(cover_letter_path)

                print("\n📄 GENERATED COVER LETTER PREVIEW:")
                print("-" * 50)

                preview_lines = 0
                for paragraph in doc.paragraphs:
                    if paragraph.text.strip():
                        text = paragraph.text.strip()
                        if preview_lines < 15:  # Show first 15 non-empty lines
                            print(f"{text}")
                            preview_lines += 1
                        elif preview_lines == 15:
                            print("\n[... content continues ...]")
                            break

                print("-" * 50)
                print(f"📁 Full file saved as: {cover_letter_path}")

            except Exception as e:
                print(f"⚠️  Could not preview file content: {e}")
                print(f"But the file was created successfully: {cover_letter_path}")

        else:
            print("❌ Failed to generate cover letter")

    except Exception as e:
        print(f"❌ Error during generation: {e}")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_single_cover_letter()