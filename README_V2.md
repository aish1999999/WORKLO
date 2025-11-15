# Automated Resume Tailor - V1 vs V2

This repository contains two versions of the Automated Resume Tailor with different approaches.

## Version 1 (automated_resume_tailor.py)

**Original Logic:**
- Extracts 15 keywords from job descriptions
- Resume structure: Header → Education → Projects → Professional Experience → Skills
- Balanced approach with moderate keyword coverage
- Uses top 10 keywords for resume generation

**Best for:**
- General applications where comprehensive keyword coverage isn't critical
- Positions where projects and education are equally important as experience

**Usage:**
```bash
python3 automated_resume_tailor.py --sheet-id YOUR_SHEET_ID --worksheet "Jobs" --base-resume ./base_resume.docx --master-template ./Master_template2.docx
```

## Version 2 (automated_resume_tailor_v2.py)

**Alternative Logic - 100% Job Description Driven:**
- Extracts **30 keywords** (2x more comprehensive ATS coverage) - ALL from job description
- **No hardcoded skills**: No default categories like "Data & Analytics (Power BI, Tableau, SQL)"
- **No predefined tools**: Every skill comes from the actual job requirements
- Resume structure: Header → **Professional Experience → Education → Projects** → Skills
- **Experience-first approach** (most important for recruiters)
- Uses **all 30 keywords** strategically distributed across bullets
- **Keyword-driven bullets**: Each bullet incorporates 3-5 specific keywords from the JD
- **6 JD-derived skill categories**: All technical skills section categories come from the job description
- **Zero repetition**: Ensures all 6 work experience bullets are unique
- Strategic keyword distribution:
  - IIT Madras bullets use keywords 1-10, 11-20, 21-30 (from JD)
  - A.V.C Pvt Ltd bullets use different keywords to avoid overlap (from JD)

**Best for:**
- ATS-heavy application processes
- Competitive positions requiring maximum keyword optimization
- Roles where work experience is the primary evaluation criterion
- Applications requiring domain-specific tailoring (not generic data science/software skills)
- Industrial Engineers applying to diverse roles across different domains

**Usage:**
```bash
python3 automated_resume_tailor_v2.py --sheet-id YOUR_SHEET_ID --worksheet "Jobs" --base-resume ./base_resume.docx --master-template ./Master_template2.docx
```

## Key Differences Summary

| Feature | V1 | V2 |
|---------|----|----|
| Keywords Extracted | 15 | 30 |
| Keywords Used in Resume | Top 10 | All 30 |
| Keyword Source | Job Description | **100% Job Description** |
| Hardcoded Skills | Some defaults | **ZERO - All from JD** |
| Technical Skills Categories | 3 JD + 3 Default | **6 JD Categories** |
| Default Categories | Yes (Data & Analytics, Design & Simulation, Process & Quality) | **NO - All from JD** |
| Resume Order | Education → Projects → Experience | **Experience → Education → Projects** |
| Bullet Strategy | General tailoring | Keyword-driven, zero repetition |
| Keyword Distribution | Organic | Strategic (keywords 1-10, 11-20, 21-30) |
| Best For | Balanced applications | ATS-heavy, domain-specific roles |
| Applicability | General roles | **Diverse roles across any domain** |
| Log File | `resume_tailor.log` | `resume_tailor_v2.log` |

## Which Version Should You Use?

**Use V1 if:**
- You want a balanced resume that highlights education and projects equally
- The job posting doesn't have many specific technical keywords
- You prefer a more traditional resume structure

**Use V2 if:**
- You're applying to roles with extensive technical requirements
- The ATS system is known to be strict about keyword matching
- You want to maximize keyword coverage (30 vs 15)
- Work experience is more important than projects for the role
- You want to ensure each bullet point is completely unique
- **You're applying to diverse roles** (not just data science/software roles)
- **You want zero bias** from hardcoded skill lists
- **You need domain-specific tailoring** (operations, quality, supply chain, controls, etc.)
- **The job description has unique/specialized skills** not covered by generic defaults

## Running Both Versions

You can run both versions independently:

```bash
# Generate resume using V1 logic
python3 automated_resume_tailor.py --sheet-id YOUR_SHEET_ID --worksheet "Jobs"

# Generate resume using V2 logic
python3 automated_resume_tailor_v2.py --sheet-id YOUR_SHEET_ID --worksheet "Jobs"
```

Both versions use the same Google Sheet and environment variables, but generate different resume outputs based on their logic.

## Notes

- Both versions avoid fabrication and only reframe existing content
- Company names and educational institutions remain unchanged in both versions
- Both versions support dry-run mode with `--dry-run` flag
- V2 takes slightly longer due to extracting and processing 30 keywords instead of 15
