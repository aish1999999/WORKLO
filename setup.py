#!/usr/bin/env python3
"""
Setup script for Automated Resume Tailor
"""

import os
import json
from pathlib import Path

def create_env_file():
    """Create .env file with user's credentials."""
    env_content = """# OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key

# LLM Provider (openai or anthropic)
LLM_PROVIDER=openai

# Google Drive Folder ID (optional)
DRIVE_FOLDER_ID=your_drive_folder_id

# Google Service Account Credentials (path to JSON file)
GOOGLE_CREDENTIALS_PATH=./google_credentials.json

# Optional: OAuth mode configuration
# GOOGLE_AUTH_MODE=oauth
# GOOGLE_CLIENT_SECRETS_FILE=./client_secret.json
# GOOGLE_OAUTH_TOKEN_FILE=./token.json

# Dry run mode (set to true to test without API calls)
# DRY_RUN=false
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with your credentials")

def create_google_credentials():
    """Create Google service account credentials file."""
    credentials = {
        "type": "service_account",
        "project_id": "key-prism-470108-f7",
        "private_key_id": "YOUR_PRIVATE_KEY_ID",
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
        "client_email": "YOUR_SERVICE_ACCOUNT@key-prism-470108-f7.iam.gserviceaccount.com",
        "client_id": "116112274808-3qjd0jglcdrqfc2j9bcigs4o6dsku0b4.apps.googleusercontent.com",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs/YOUR_SERVICE_ACCOUNT%40key-prism-470108-f7.iam.gserviceaccount.com"
    }
    
    with open('google_credentials.json', 'w') as f:
        json.dump(credentials, f, indent=2)
    
    print("✅ Created google_credentials.json template")
    print("⚠️  You need to replace the placeholder values with your actual service account credentials")

def create_sample_files():
    """Create sample resume and template files."""
    # Create sample base resume
    base_resume_content = """John Doe
Senior Software Engineer
john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years developing scalable applications using Python, JavaScript, and cloud technologies. Proven track record of leading development teams and delivering high-quality software solutions.

CORE SKILLS
• Python, JavaScript, TypeScript
• React, Node.js, Express
• AWS, Docker, Kubernetes
• PostgreSQL, MongoDB
• Git, CI/CD, Agile

EXPERIENCE
Software Engineer | Tech Corp | 2020-2023
• Developed microservices architecture serving 100K+ users
• Led team of 3 developers on critical projects
• Implemented automated testing reducing bugs by 40%

Junior Developer | StartupXYZ | 2018-2020
• Built responsive web applications using React
• Collaborated with design team on user experience
• Optimized database queries improving performance by 30%

PROJECTS
E-commerce Platform
• Full-stack application with React frontend and Node.js backend
• Integrated payment processing and inventory management
• Deployed on AWS with Docker containers

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2018
"""
    
    with open('sample_base_resume.txt', 'w') as f:
        f.write(base_resume_content)
    
    print("✅ Created sample_base_resume.txt")
    print("⚠️  Convert this to DOCX format for use with the script")

def main():
    """Main setup function."""
    print("🚀 Setting up Automated Resume Tailor...")
    
    # Create .env file
    create_env_file()
    
    # Create Google credentials template
    create_google_credentials()
    
    # Create sample files
    create_sample_files()
    
    print("\n📋 Next Steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Update google_credentials.json with your actual service account credentials")
    print("3. Create your base resume and master template as DOCX files")
    print("4. Set up your Google Sheet with JOB_TITLE and JOB_DESCRIPTION columns")
    print("5. Run the script: python automated_resume_tailor.py --help")
    
    print("\n🔧 Google Service Account Setup:")
    print("1. Go to Google Cloud Console")
    print("2. Create/select project → Enable Google Sheets API & Google Drive API")
    print("3. Create Service Account → Download JSON key file")
    print("4. Replace the content in google_credentials.json with your downloaded file")
    print("5. Share your Google Sheet with the service account email")

if __name__ == "__main__":
    main()

