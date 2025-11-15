#!/usr/bin/env python3
"""
Test Google Sheets integration for cover letters
"""

import sys
import os
sys.path.append('.')

from automated_resume_tailor import ResumeTailor

def test_sheets_integration():
    """Test Google Sheets integration to see column structure"""

    print("=" * 80)
    print("TESTING GOOGLE SHEETS INTEGRATION")
    print("=" * 80)

    # Initialize resume tailor (this will also help us see sheet structure)
    print("🔧 Initializing ResumeTailor...")
    tailor = ResumeTailor(dry_run=False)

    try:
        print("📊 Processing job data to see column structure...")
        job_records = tailor.process_job_data(
            sheet_id='1dkxFBloNJQMnXtTfLG5CsGryK_EfmlYrdFFluWPBkgw',
            worksheet_name='Jobs',
            overwrite_keywords=False
        )

        if job_records:
            print(f"✅ Found {len(job_records)} job records")
            print("\n📋 Sample record structure:")
            sample_record = job_records[0]

            for key in sorted(sample_record.keys()):
                if key.startswith('__'):
                    print(f"  🔧 {key}: {sample_record[key]}")
                else:
                    value = sample_record[key]
                    if len(str(value)) > 50:
                        value = str(value)[:50] + "..."
                    print(f"  📄 {key}: {value}")

            print("\n🎯 Looking for cover letter column information:")
            cover_letter_col = sample_record.get('__COVER_LETTER_COL_INDEX')
            if cover_letter_col:
                print(f"✅ Cover letter column index found: {cover_letter_col}")
            else:
                print("⚠️  Cover letter column index not found")

                # Look for potential cover letter columns
                print("\n🔍 Searching for potential cover letter columns:")
                for key in sample_record.keys():
                    if 'COVER' in key.upper() or 'LETTER' in key.upper():
                        print(f"  📝 Found potential column: {key}")
        else:
            print("❌ No job records found")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_sheets_integration()