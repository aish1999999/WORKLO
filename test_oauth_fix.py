#!/usr/bin/env python3
"""
Quick test script to verify OAuth authentication fix for Google Sheets
"""
import os
import sys
import logging
from pathlib import Path
import gspread

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def test_google_sheets_oauth():
    """Test Google Sheets OAuth authentication."""

    client_secrets = os.getenv('GOOGLE_CLIENT_SECRETS_FILE', './client_secret.json')
    token_file = os.getenv('GOOGLE_OAUTH_TOKEN_FILE', './token.json')

    logger.info(f"Using client secrets: {client_secrets}")
    logger.info(f"Token file: {token_file}")
    logger.info(f"Token file exists: {Path(token_file).exists()}")

    try:
        logger.info("Attempting Google Sheets OAuth authentication...")
        gc = gspread.oauth(
            credentials_filename=client_secrets,
            authorized_user_filename=token_file,
        )
        logger.info("✓ Google Sheets OAuth authentication SUCCESSFUL!")

        # Try to list spreadsheets to verify it works
        logger.info("Testing API access by listing spreadsheets...")
        spreadsheets = gc.openall()
        logger.info(f"✓ Successfully accessed {len(spreadsheets)} spreadsheet(s)")

        if spreadsheets:
            logger.info("Sample spreadsheet titles:")
            for i, sheet in enumerate(spreadsheets[:5], 1):
                logger.info(f"  {i}. {sheet.title}")

        return True

    except Exception as e:
        logger.error(f"✗ OAuth authentication FAILED: {e}")

        # Check if token file is corrupted
        if Path(token_file).exists():
            logger.warning(f"Token file exists but may be corrupted. Deleting: {token_file}")
            Path(token_file).unlink()
            logger.info("Please run this script again to reauthenticate.")

        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Google Sheets OAuth Authentication Test")
    print("=" * 60)

    success = test_google_sheets_oauth()

    print("=" * 60)
    if success:
        print("✓ TEST PASSED: OAuth authentication working correctly")
        sys.exit(0)
    else:
        print("✗ TEST FAILED: OAuth authentication needs attention")
        sys.exit(1)
