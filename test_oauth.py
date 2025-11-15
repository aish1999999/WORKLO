#!/usr/bin/env python3
"""
Test OAuth setup for Automated Resume Tailor
"""

import os
import sys
from dotenv import load_dotenv

def test_oauth_setup():
    """Test OAuth environment variables and file setup."""
    print("🔍 Testing OAuth setup...")
    
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    required_vars = [
        'GOOGLE_AUTH_MODE',
        'GOOGLE_CLIENT_SECRETS_FILE', 
        'LLM_PROVIDER',
        'OPENAI_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ All required environment variables are set")
    
    # Check OAuth mode
    auth_mode = os.getenv('GOOGLE_AUTH_MODE')
    if auth_mode != 'oauth':
        print(f"⚠️  GOOGLE_AUTH_MODE is '{auth_mode}', expected 'oauth'")
    else:
        print("✅ OAuth mode is enabled")
    
    # Check client secrets file
    client_secrets_file = os.getenv('GOOGLE_CLIENT_SECRETS_FILE')
    if os.path.exists(client_secrets_file):
        print(f"✅ Client secrets file found: {client_secrets_file}")
    else:
        print(f"❌ Client secrets file not found: {client_secrets_file}")
        return False
    
    # Check LLM provider
    llm_provider = os.getenv('LLM_PROVIDER')
    if llm_provider in ['openai', 'anthropic']:
        print(f"✅ LLM provider set to: {llm_provider}")
    else:
        print(f"❌ Invalid LLM provider: {llm_provider}")
        return False
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key.startswith('sk-'):
        print("✅ OpenAI API key format looks correct")
    else:
        print("❌ OpenAI API key format is invalid")
        return False
    
    # Check Drive folder ID
    drive_folder = os.getenv('DRIVE_FOLDER_ID')
    if drive_folder:
        print(f"✅ Drive folder ID set: {drive_folder}")
    else:
        print("⚠️  Drive folder ID not set (optional)")
    
    return True

def test_script_import():
    """Test if the script can be imported with OAuth config."""
    print("\n🔍 Testing script import with OAuth...")
    
    try:
        from automated_resume_tailor import ResumeTailor
        print("✅ Script imported successfully")
        
        # Test dry run initialization
        tailor = ResumeTailor(dry_run=True)
        print("✅ ResumeTailor initialized in dry run mode")
        
        return True
    except Exception as e:
        print(f"❌ Script import failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Testing OAuth Setup for Automated Resume Tailor\n")
    
    # Test OAuth setup
    oauth_ok = test_oauth_setup()
    
    # Test script import
    import_ok = test_script_import()
    
    print("\n" + "="*50)
    if oauth_ok and import_ok:
        print("🎉 OAuth setup is ready! You can now run the resume tailor.")
        print("\nNext steps:")
        print("1. Create your base resume and master template as DOCX files")
        print("2. Set up your Google Sheet with JOB_TITLE and JOB_DESCRIPTION columns")
        print("3. Run: python automated_resume_tailor.py --help")
        print("\nNote: On first run, you'll be prompted to authorize the app in your browser.")
    else:
        print("❌ OAuth setup has issues. Please check the errors above.")
    
    return oauth_ok and import_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

