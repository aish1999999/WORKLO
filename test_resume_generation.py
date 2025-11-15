#!/usr/bin/env python3
"""Quick test script to verify resume generation works"""

import sys
import logging
from automated_resume_tailor import ResumeTailor

logging.basicConfig(level=logging.INFO)

# Initialize
tailor = ResumeTailor(dry_run=False)

# Process jobs
print("\n=== Testing Resume Generation ===\n")

job_records = tailor.process_job_data(
    sheet_id="1dkxFBloNJQMnXtTfLG5CsGryK_EfmlYrdFFluWPBkgw",
    worksheet_name="Jobs",
    overwrite_keywords=False
)

print(f"\nFound {len(job_records)} job records")

for i, record in enumerate(job_records, 1):
    job_title = record.get('JOB_TITLE', 'Unknown')
    resume_link = record.get('RESUME_LINK', '').strip()
    print(f"{i}. {job_title}")
    print(f"   Resume exists: {'YES' if resume_link else 'NO'}")

    if not resume_link:
        print(f"   → Will generate resume for this job")
