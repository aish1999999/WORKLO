#!/usr/bin/env python3
"""
Integrated Application Tailor

A comprehensive workflow that generates both tailored resumes and cover letters for job applications.
Coordinates between automated_resume_tailor.py and automated_cover_letter.py to provide complete automation.

USAGE:
python integrated_application_tailor.py --sheet-id 1dkxFBloNJQMnXtTfLG5CsGryK_EfmlYrdFFluWPBkgw --worksheet "Jobs"

This script will:
1. Process job data and extract keywords (using resume tailor)
2. Generate tailored resumes for each job (using resume tailor)
3. Generate tailored cover letters for each job (using cover letter tailor)
4. Upload both files to Google Drive
5. Update Google Sheet with both resume and cover letter links
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Import our tailoring systems
from automated_resume_tailor import ResumeTailor
from automated_cover_letter import CoverLetterTailor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('integrated_application_tailor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class IntegratedApplicationTailor:
    """Integrated system for generating both resumes and cover letters."""

    def __init__(self, dry_run: bool = False):
        """Initialize both resume and cover letter tailors."""
        self.dry_run = dry_run

        # Initialize both tailoring systems
        self.resume_tailor = ResumeTailor(dry_run=dry_run)
        self.cover_letter_tailor = CoverLetterTailor(dry_run=dry_run)

        logger.info(f"Integrated Application Tailor initialized - Dry run: {dry_run}")

    def process_applications(self, sheet_id: str, worksheet_name: str,
                           base_resume_path: str, master_resume_template_path: str,
                           base_cover_letter_path: str, master_cover_letter_template_path: str,
                           drive_folder_id: str, overwrite_keywords: bool = False) -> Dict[str, Any]:
        """
        Process complete job applications with both resume and cover letter generation.

        Returns:
            Dictionary with processing results and statistics
        """
        results = {
            'processed_jobs': 0,
            'resumes_generated': 0,
            'cover_letters_generated': 0,
            'errors': [],
            'successful_applications': []
        }

        try:
            # STEP 1: Process job data and extract keywords (using resume tailor)
            logger.info("Processing job data and extracting keywords...")
            job_records = self.resume_tailor.process_job_data(
                sheet_id, worksheet_name, overwrite_keywords
            )

            if not job_records:
                logger.warning("No job records to process")
                return results

            results['processed_jobs'] = len(job_records)
            logger.info(f"Found {len(job_records)} job records to process")

            # STEP 2: Generate applications for each job
            for record in job_records:
                job_title = record.get('JOB_TITLE', '')
                job_description = record.get('JOB_DESCRIPTION', '')
                company_name = record.get('COMPANY', '')
                keywords = record.get('KEYWORDS_RAW', [])

                if not job_title or not job_description:
                    logger.warning(f"Skipping job with missing title or description: {record}")
                    continue

                # Check if applications already exist (skip duplicates)
                existing_resume_link = record.get('RESUME_LINK', '').strip()
                existing_cover_letter_link = record.get('COVER_LETTER_VERSION', '').strip()

                if existing_resume_link and existing_cover_letter_link:
                    logger.info(f"Skipping '{job_title}' - Both resume and cover letter already exist")
                    continue

                logger.info(f"Generating application for: {job_title} at {company_name}")

                # Generate resume (if not exists)
                resume_path = ""
                if not existing_resume_link:
                    logger.info("Generating tailored resume...")
                    resume_path = self.resume_tailor.generate_resume(
                        base_resume_path,
                        master_resume_template_path,
                        job_title,
                        job_description,
                        keywords,
                        company_name
                    )

                    if resume_path:
                        results['resumes_generated'] += 1
                        logger.info(f"Resume generated: {resume_path}")
                    else:
                        error_msg = f"Failed to generate resume for {job_title}"
                        results['errors'].append(error_msg)
                        logger.error(error_msg)
                        continue
                else:
                    logger.info("Resume already exists, skipping resume generation")

                # Generate cover letter (if not exists)
                cover_letter_path = ""
                if not existing_cover_letter_link:
                    logger.info("Generating tailored cover letter...")
                    cover_letter_path = self.cover_letter_tailor.generate_cover_letter(
                        base_cover_letter_path,
                        master_cover_letter_template_path,
                        job_title,
                        job_description,
                        keywords,
                        company_name
                    )

                    if cover_letter_path:
                        results['cover_letters_generated'] += 1
                        logger.info(f"Cover letter generated: {cover_letter_path}")
                    else:
                        error_msg = f"Failed to generate cover letter for {job_title}"
                        results['errors'].append(error_msg)
                        logger.error(error_msg)
                        # Continue processing even if cover letter fails
                else:
                    logger.info("Cover letter already exists, skipping cover letter generation")

                # Upload files and update sheet
                application_success = True

                # Upload resume to Drive (if generated)
                if resume_path and not existing_resume_link:
                    logger.info("Uploading resume to Google Drive...")
                    resume_drive_link = self.resume_tailor.upload_to_drive(resume_path, drive_folder_id)

                    if resume_drive_link:
                        logger.info(f"Resume uploaded: {resume_drive_link}")

                        # Update Google Sheet with resume link
                        resume_update_success = self.resume_tailor.update_resume_link_in_sheet(record, resume_drive_link)
                        if resume_update_success:
                            logger.info("Google Sheet updated with resume link")
                        else:
                            application_success = False
                            logger.error("Failed to update Google Sheet with resume link")

                        # Clean up local resume file
                        try:
                            Path(resume_path).unlink()
                            logger.info(f"Local resume file cleaned up: {resume_path}")
                        except Exception as e:
                            logger.warning(f"Failed to clean up local resume file {resume_path}: {e}")
                    else:
                        application_success = False
                        logger.error("Failed to upload resume to Drive")

                # Upload cover letter to Drive (if generated)
                if cover_letter_path and not existing_cover_letter_link:
                    logger.info("Uploading cover letter to Google Drive...")
                    cover_letter_drive_link = self.cover_letter_tailor.upload_to_drive(cover_letter_path, drive_folder_id)

                    if cover_letter_drive_link:
                        logger.info(f"Cover letter uploaded: {cover_letter_drive_link}")

                        # Update Google Sheet with cover letter link
                        # Note: We need to add cover letter column index to the job record
                        if '__COVER_LETTER_COL_INDEX' not in record:
                            # Find the cover letter column (this should be handled in resume tailor's process_job_data)
                            logger.warning("Cover letter column index not found in job record")

                        cover_letter_update_success = self.cover_letter_tailor.update_cover_letter_link_in_sheet(record, cover_letter_drive_link)
                        if cover_letter_update_success:
                            logger.info("Google Sheet updated with cover letter link")
                        else:
                            logger.error("Failed to update Google Sheet with cover letter link")
                            # Don't mark as failure since resume might have succeeded

                        # Clean up local cover letter file
                        try:
                            Path(cover_letter_path).unlink()
                            logger.info(f"Local cover letter file cleaned up: {cover_letter_path}")
                        except Exception as e:
                            logger.warning(f"Failed to clean up local cover letter file {cover_letter_path}: {e}")
                    else:
                        logger.error("Failed to upload cover letter to Drive")
                        # Don't mark as complete failure since resume might have succeeded

                if application_success:
                    results['successful_applications'].append({
                        'job_title': job_title,
                        'company': company_name,
                        'resume_generated': bool(resume_path),
                        'cover_letter_generated': bool(cover_letter_path)
                    })

            # Log final results
            logger.info(f"Processing complete:")
            logger.info(f"  - Jobs processed: {results['processed_jobs']}")
            logger.info(f"  - Resumes generated: {results['resumes_generated']}")
            logger.info(f"  - Cover letters generated: {results['cover_letters_generated']}")
            logger.info(f"  - Successful applications: {len(results['successful_applications'])}")
            if results['errors']:
                logger.info(f"  - Errors encountered: {len(results['errors'])}")
                for error in results['errors']:
                    logger.info(f"    * {error}")

            return results

        except Exception as e:
            error_msg = f"Error in integrated application processing: {e}"
            results['errors'].append(error_msg)
            logger.error(error_msg)
            return results


def main():
    """Main CLI function for integrated application tailoring."""
    parser = argparse.ArgumentParser(description='Integrated Application Tailor - Generates both resumes and cover letters')

    # Use defaults from environment or hardcoded values
    default_sheet_id = os.getenv('GOOGLE_SHEET_ID', '1dkxFBloNJQMnXtTfLG5CsGryK_EfmlYrdFFluWPBkgw')
    default_worksheet = os.getenv('GOOGLE_WORKSHEET', 'Jobs')
    default_base_resume = os.getenv('BASE_RESUME_PATH', './base_resume.docx')
    default_master_resume_template = os.getenv('MASTER_TEMPLATE_PATH', './Master_template2.docx')
    default_base_cover_letter = os.getenv('BASE_COVER_LETTER_PATH', './base_cover_letter_new.docx')
    default_master_cover_letter_template = os.getenv('MASTER_COVER_LETTER_TEMPLATE_PATH', './master_cover_letter_template.docx')
    default_drive_folder = os.getenv('DRIVE_FOLDER_ID', '1PCBjveFtn07ljJyIhmVjwlwWwPZ7hoFr')

    parser.add_argument('--sheet-id', default=default_sheet_id, help=f'Google Sheets document ID (default: {default_sheet_id})')
    parser.add_argument('--worksheet', default=default_worksheet, help=f'Worksheet name (default: {default_worksheet})')
    parser.add_argument('--base-resume', default=default_base_resume, help=f'Path to base resume DOCX file (default: {default_base_resume})')
    parser.add_argument('--master-resume-template', default=default_master_resume_template, help=f'Path to master resume template DOCX file (default: {default_master_resume_template})')
    parser.add_argument('--base-cover-letter', default=default_base_cover_letter, help=f'Path to base cover letter DOCX file (default: {default_base_cover_letter})')
    parser.add_argument('--master-cover-letter-template', default=default_master_cover_letter_template, help=f'Path to master cover letter template DOCX file (default: {default_master_cover_letter_template})')
    parser.add_argument('--overwrite-keywords', action='store_true', help='Overwrite existing keywords')
    parser.add_argument('--dry-run', action='store_true', help='Run in dry-run mode')
    parser.add_argument('--drive-folder-id', default=default_drive_folder, help=f'Google Drive folder ID for uploads (default: {default_drive_folder})')

    args = parser.parse_args()

    # Initialize the integrated tailor
    tailor = IntegratedApplicationTailor(dry_run=args.dry_run)

    try:
        # Process complete applications
        results = tailor.process_applications(
            sheet_id=args.sheet_id,
            worksheet_name=args.worksheet,
            base_resume_path=args.base_resume,
            master_resume_template_path=args.master_resume_template,
            base_cover_letter_path=args.base_cover_letter,
            master_cover_letter_template_path=args.master_cover_letter_template,
            drive_folder_id=args.drive_folder_id,
            overwrite_keywords=args.overwrite_keywords
        )

        # Exit with appropriate code
        if results['errors']:
            logger.error("Processing completed with errors")
            sys.exit(1)
        else:
            logger.info("All applications processed successfully")
            sys.exit(0)

    except Exception as e:
        logger.error(f"Fatal error in main process: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()