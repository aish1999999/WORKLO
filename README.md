🎯 Automated Resume Tailor
A Python-powered command-line tool that automatically tailors resumes to specific job descriptions using AI, Google Sheets, and Google Drive.

📋 Table of Contents
Overview
Features
Prerequisites
Installation
Google Cloud Setup
Configuration
Usage
Troubleshooting
🔍 Overview
This tool automates the tedious process of tailoring your resume for each job application. It:

Reads job postings from a Google Sheet
Extracts relevant keywords using AI (OpenAI or Anthropic)
Generates custom resumes aligned with each job description
Uploads tailored resumes to Google Drive
Updates the Google Sheet with Drive links
No web server or database required - just Python, Google Sheets, and AI APIs!

✨ Features
📊 Google Sheets as Database - Manage all job postings in a spreadsheet
🤖 AI-Powered Keyword Extraction - OpenAI (GPT-4o-mini) or Anthropic (Claude) API
📝 Smart Resume Generation - Tailors content to match job requirements
☁️ Auto Google Drive Upload - Organized storage with shareable links
🔄 Duplicate Detection - Skips jobs that already have resumes
📐 Perfect Formatting - Preserves master template styling
🎯 ATS-Optimized - Industry-standard format with keyword integration
📦 Prerequisites
Before you begin, ensure you have:

Software Requirements
Python 3.9 or higher - Download
pip (Python package manager - comes with Python)
Git (optional) - Download
API Keys & Accounts
You'll need accounts for:

OpenAI (platform.openai.com) OR Anthropic (console.anthropic.com)
Google Cloud (for Sheets & Drive APIs) - console.cloud.google.com
Required Files
base_resume.docx - Your actual resume with factual experience
Master_template2.docx - Resume template with desired formatting/styling
🔧 Installation
Step 1: Download or Clone the Project
# If using Git
git clone <repository-url>
cd workload

# OR download ZIP and extract, then navigate to folder
cd path/to/workload
Step 2: Install Python Packages
Important: Install these exact packages in this order:

# Core packages for resume generation
pip install gspread==5.12.4
pip install oauth2client==4.1.3
pip install openai==1.3.7
pip install anthropic==0.7.8
pip install python-docx==1.1.0
pip install PyDrive2==1.16.0
pip install tenacity==8.2.3
pip install python-dotenv==1.0.0
pip install google-auth-oauthlib==1.2.0
OR install all at once using requirements.txt:

pip install -r requirements.txt
Note: If you encounter errors with pydantic-core on Python 3.13, use Python 3.11 or 3.12 instead.

Step 3: Verify Installation
python3 -c "import gspread, openai, anthropic, docx; print('All packages installed successfully!')"
If you see the success message, you're ready to proceed!

🔑 Google Cloud Setup
1. Create Google Cloud Project
Go to Google Cloud Console
Click "Select a Project" → "New Project"
Name it (e.g., "Resume Tailor")
Click "Create"
2. Enable Required APIs
In the Cloud Console, go to "APIs & Services" → "Library"
Search and enable:
Google Sheets API
Google Drive API
3. Set Up OAuth Credentials
Step A: Configure Consent Screen
Go to "APIs & Services" → "OAuth consent screen"
Select "External" → Click "Create"
Fill in required fields:
App name: Resume Tailor
User support email: Your email
Developer contact: Your email
Click "Save and Continue"
Skip "Scopes" → Click "Save and Continue"
Add yourself as a test user:
Click "Add Users"
Enter your email
Click "Save and Continue"
Step B: Create OAuth Client ID
Go to "APIs & Services" → "Credentials"
Click "+ Create Credentials" → "OAuth client ID"
Application type: "Desktop app"
Name: Resume Tailor Desktop
Click "Create"
Click "Download JSON"
Save the downloaded file as client_secret.json in your project folder
4. Create Google Drive Folder
Open Google Drive
Create a new folder: "Tailored Resumes"
Open the folder and copy the Folder ID from the URL:
https://drive.google.com/drive/folders/[THIS_IS_THE_FOLDER_ID]
Save this ID - you'll need it for configuration
5. Create Google Sheet
Create a new Google Sheet

Name it: "Job Applications"

Add these column headers in Row 1:

A	B	C	D	E	F	G	H	I	J	K	L	M	N
Job ID	Job Title	Company name	Location	Experience Level	Sponsorship	Posting URL	Posted Date	Job Description (raw)	Keywords extracted	Resume version [link]	Cover letter version	Tailoring status	Priority score
Copy the Sheet ID from the URL:

https://docs.google.com/spreadsheets/d/[THIS_IS_THE_SHEET_ID]/edit
⚙️ Configuration
1. Get Your API Keys
OpenAI (Recommended)
Go to OpenAI Platform
Sign in or create account
Click "+ Create new secret key"
Copy the key (starts with sk-proj-... or sk-...)
Anthropic (Alternative)
Go to Anthropic Console
Sign in or create account
Go to API Keys → "Create Key"
Copy the key
2. Create Environment File
Create a file named .env in your project folder with this content:

# LLM Provider (choose one)
LLM_PROVIDER=openai

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE

# Anthropic Configuration (if using Anthropic)
ANTHROPIC_API_KEY=sk-ant-YOUR_ACTUAL_KEY_HERE

# Google Authentication Mode
GOOGLE_AUTH_MODE=oauth

# Google OAuth Configuration
GOOGLE_CLIENT_SECRETS_FILE=./client_secret.json
GOOGLE_OAUTH_TOKEN_FILE=./token.json

# Google Drive folder ID for uploads
DRIVE_FOLDER_ID=YOUR_DRIVE_FOLDER_ID_HERE

# Google Sheets Configuration
GOOGLE_SHEET_ID=YOUR_GOOGLE_SHEET_ID_HERE
GOOGLE_WORKSHEET=Jobs

# Dry Run Mode (set to false for actual processing)
DRY_RUN=false
Replace the following:

YOUR_ACTUAL_KEY_HERE → Your OpenAI or Anthropic API key
YOUR_DRIVE_FOLDER_ID_HERE → Google Drive folder ID from earlier
YOUR_GOOGLE_SHEET_ID_HERE → Google Sheets ID from earlier
3. Prepare Resume Files
Ensure these files exist in your project folder:

base_resume.docx - Your actual resume with real experience
Master_template2.docx - Template with desired formatting
🚀 Usage
Basic Command
python3 automated_resume_tailor.py --sheet-id YOUR_SHEET_ID --worksheet "Jobs" --base-resume ./base_resume.docx --master-template ./Master_template2.docx
Using Environment Variables (Recommended)
If you set GOOGLE_SHEET_ID and GOOGLE_WORKSHEET in .env, you can simply run:

python3 automated_resume_tailor.py --base-resume ./base_resume.docx --master-template ./Master_template2.docx
First Run - OAuth Authentication
When you run the script for the first time, it will:

Open your browser automatically
Ask you to sign in to Google
Show a warning: "Google hasn't verified this app"
Click "Advanced" → "Go to Resume Tailor (unsafe)"
This is normal for personal OAuth apps
Click "Allow" to grant permissions
The script will continue and save credentials to token.json
Subsequent runs will use the saved token (no browser needed).

Command-Line Options
# Overwrite existing keywords (re-extract even if keywords exist)
python3 automated_resume_tailor.py --overwrite-keywords

# Dry run mode (test without making API calls)
python3 automated_resume_tailor.py --dry-run

# Specify custom Drive folder
python3 automated_resume_tailor.py --drive-folder-id YOUR_FOLDER_ID

# Full example with all options
python3 automated_resume_tailor.py \
  --sheet-id 1dkxFBloNJQMnXtTfLG5CsGryK_EfmlYrdFFluWPBkgw \
  --worksheet "Jobs" \
  --base-resume ./base_resume.docx \
  --master-template ./Master_template2.docx \
  --overwrite-keywords \
  --drive-folder-id 157tAEUFoynamUs5ahZr-0GWC0NvsNxQK
What Happens When You Run It
The script will:

✅ Connect to Google Sheets
✅ Read all job postings
✅ Extract keywords for new jobs (using AI)
✅ Update Google Sheet with extracted keywords
✅ Generate tailored resumes for jobs without existing resumes
✅ Upload resumes to Google Drive
✅ Update Google Sheet with Drive links
✅ Clean up local files
Progress is logged to both:

Console output (real-time)
resume_tailor.log file (persistent)
📊 Google Sheet Structure
Required Columns
Your Google Sheet must have these columns (exact names):

Column Name	Description	Auto-filled?
Job Title	Position name	Manual
Company name	Employer	Manual
Job Description (raw)	Full job posting text	Manual
Keywords extracted	AI-extracted keywords	✅ Auto
Resume version [link]	Google Drive link	✅ Auto
Example Row
Job Title	Company name	Job Description (raw)	Keywords extracted	Resume version [link]
Software Engineer	Google	We are seeking...	python (rank 1); aws (rank 2); docker (rank 3); ...	https://drive.google.com/file/d/...
Adding New Jobs
Open your Google Sheet
Add a new row with:
Job Title
Company name (optional but recommended)
Job Description (paste the full text)
Leave "Keywords extracted" and "Resume version [link]" blank
Run the script - it will fill these automatically!
🐛 Troubleshooting
Common Issues
1. "ModuleNotFoundError: No module named 'docx'"
Problem: Wrong package installed (old docx instead of python-docx)

Solution:

pip uninstall docx
pip install python-docx==1.1.0
2. "invalid_grant: Token has been expired or revoked"
Problem: OAuth token expired

Solution:

rm -f token.json authorized_user.json
python3 automated_resume_tailor.py --base-resume ./base_resume.docx --master-template ./Master_template2.docx
# Browser will open for re-authentication
3. "OPENAI_API_KEY is set to a placeholder value"
Problem: You didn't update the .env file with a real API key

Solution:

Get API key from OpenAI Platform
Edit .env and replace YOUR_ACTUAL_KEY_HERE with your real key
Make sure the key starts with sk-
4. "Worksheet 'Jobs' not found"
Problem: Worksheet name doesn't match

Solution:

Check your Google Sheet - the tab name must be exactly Jobs (case-sensitive)
OR update .env: GOOGLE_WORKSHEET=YourActualTabName
5. "Failed to initialize Google Sheets client"
Problem: client_secret.json file missing or incorrect

Solution:

Verify client_secret.json exists in project folder
Re-download OAuth credentials from Google Cloud Console
Make sure .env has: GOOGLE_CLIENT_SECRETS_FILE=./client_secret.json
6. "No jobs to process" or "No records found"
Problem: Google Sheet is empty or has wrong structure

Solution:

Verify your Google Sheet has data rows (beyond the header)
Check that column names match exactly (see Google Sheet Structure)
Ensure at least "Job Title" and "Job Description (raw)" are filled
7. Virtual Environment Errors (Python 3.13)
Problem: pydantic-core build fails on Python 3.13

Solution:

# Option 1: Use system Python instead of venv
deactivate  # if in a venv
python3 automated_resume_tailor.py ...

# Option 2: Use Python 3.11 or 3.12
pyenv install 3.11.0  # or download from python.org
python3.11 -m pip install -r requirements.txt
python3.11 automated_resume_tailor.py ...
Verification Commands
Test Python packages:

python3 -c "import gspread, openai, docx; print('✓ Packages OK')"
Test environment variables:

python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', 'SET' if os.getenv('OPENAI_API_KEY') else 'MISSING')"
Check script help:

python3 automated_resume_tailor.py --help
Log Files
Check these files for detailed error messages:

resume_tailor.log - Main application log
Terminal output - Real-time processing info
📁 Project Structure
workload/
├── automated_resume_tailor.py     # Main script
├── resume_txt_converter.py        # Formatting handler
├── requirements.txt               # Python dependencies
├── base_resume.docx               # Your actual resume
├── Master_template2.docx          # Formatting template
├── client_secret.json             # Google OAuth credentials
├── .env                           # Configuration (DO NOT COMMIT)
├── .env.example                   # Template for .env
├── token.json                     # Auto-generated (OAuth token)
├── resume_tailor.log              # Application logs
└── README2.md                     # This file
Generated files (auto-created):

token.json - OAuth authentication token
authorized_user.json - OAuth user info
Aishwaryeshwar_Manickavel_company_jobtitle.docx - Generated resumes (deleted after upload)
🔒 Security & Privacy
Important Notes
✅ Never commit .env, client_secret.json, or token.json to Git
✅ .gitignore already excludes these files
✅ API keys are sensitive - keep them private
✅ Generated resumes are uploaded to Drive then deleted locally
✅ OAuth tokens stored locally - only you can access your Google account
Best Practices
Rotate API keys periodically
Don't share your .env or client_secret.json files
Review Google Drive permissions regularly
Keep Python packages updated for security patches
Use separate Google account for testing if concerned
📖 How It Works
Workflow
1. Read Google Sheet
   ↓
2. For each job without keywords:
   → Extract keywords using AI
   → Save to Google Sheet
   ↓
3. For each job without resume:
   → Read job description + keywords
   → Generate tailored resume content (AI)
   → Create formatted .docx file
   → Upload to Google Drive
   → Save Drive link to Google Sheet
   → Delete local file
   ↓
4. Done! ✓
AI Prompting Strategy
The tool uses sophisticated prompts to:

Extract 15 ranked keywords from job descriptions
Generate achievement-focused bullet points using STAR method
Tailor technical skills section with 6 alternating categories
Maintain ATS-optimized formatting (1-page, specific fonts/margins)
Integrate default skills (Power BI, Python, SQL, etc.) naturally
Resume Customization
What gets tailored:

✅ Project bullets (2 per project)
✅ Work experience bullets (3 per role)
✅ Technical skills categories (6 total)
✅ Keywords naturally integrated throughout
What stays the same:

✅ Name, contact info
✅ Education details
✅ Company names
✅ University/project names
✅ Formatting (fonts, margins, spacing)
🎓 Package Reference
Required Python Packages
Package	Version	Purpose
gspread	5.12.4	Google Sheets API client
oauth2client	4.1.3	Google OAuth authentication
openai	1.3.7	OpenAI GPT API client
anthropic	0.7.8	Anthropic Claude API client
python-docx	1.1.0	Create/edit Word documents
PyDrive2	1.16.0	Google Drive integration
tenacity	8.2.3	Retry logic with exponential backoff
python-dotenv	1.0.0	Load environment variables
google-auth-oauthlib	1.2.0	Google OAuth flow
Installation Verification
After installing, verify each package:

python3 -c "
import gspread
import oauth2client
import openai
import anthropic
import docx
from pydrive2.auth import GoogleAuth
from tenacity import retry
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
print('✓ All packages imported successfully!')
"
If you see the success message, all packages are correctly installed!

🙏 Credits
AI Models:

OpenAI GPT-4o-mini
Anthropic Claude 3
Google APIs:

Google Sheets API
Google Drive API
Python Libraries:

gspread by burnash
python-docx by python-openxml
PyDrive2 community
📞 Support
Need help?

Check the Troubleshooting section
Review resume_tailor.log for error details
Verify all prerequisites are met
Ensure configuration is correct
Common questions:

"Do I need a web server?" → No, this is a CLI tool
"Do I need Supabase?" → No, Google Sheets is the database
"Can I use Anthropic instead of OpenAI?" → Yes, set LLM_PROVIDER=anthropic
"How much does it cost?" → OpenAI API costs ~$0.01-0.05 per resume
Happy Resume Tailoring! 🎯
