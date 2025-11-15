# Quick Start Guide - Resume Tailor V2

## ✅ V2 is Ready to Use!

The V2 alternative logic has been successfully implemented with a **100% Job Description-Driven Approach** in: `automated_resume_tailor_v2.py`

## 🚀 Running V2

```bash
# Activate virtual environment
source .venv/bin/activate

# Run V2 (30 keywords, Experience-first, JD-only)
python3 automated_resume_tailor_v2.py --sheet-id YOUR_SHEET_ID --worksheet "Jobs" --base-resume ./base_resume.docx --master-template ./Master_template2.docx
```

## 📊 What V2 Does Differently

### 1. **30 Keywords Instead of 15 (100% from JD)**
- V1: Extracts 15 keywords
- V2: **Extracts 30 keywords** - ALL extracted from the job description only
- **No hardcoded skills**: No default skill lists (Power BI, Tableau, Python, Lean Six Sigma, etc.)
- **No predefined categories**: All skills come from the actual job requirements

### 2. **Experience-First Resume Structure**
- V1: Header → Education → Projects → Experience → Skills
- V2: **Header → Experience → Education → Projects → Skills**
- Recruiters see your work experience first!

### 3. **Keyword-Driven Bullet Points (JD-Only)**
- Each bullet point incorporates 3-5 specific keywords FROM THE JOB DESCRIPTION
- Strategic distribution across all 6 work experience bullets:
  - IIT Madras bullets use keywords ranked 1-10, 11-20, 21-30 (from JD)
  - A.V.C Pvt Ltd bullets use different keywords to maximize variety (from JD)
- ALL keywords come from the job description - zero hardcoded skills

### 4. **100% Job Description-Driven Technical Skills**
- **ALL 6 skill categories** are created from the job description
- V1: 3 JD categories + 3 default categories (Data & Analytics, Design & Simulation, Process & Quality)
- V2: **6 JD categories** - NO defaults, NO hardcoded skills
- Every skill must be explicitly mentioned or clearly implied by the JD

### 5. **Zero Repetition Strategy**
- V2 ensures every bullet is unique
- No keyword overlap between bullets
- Fresh content crafted specifically for each bullet

## 📝 Example Keyword Distribution

**Job Description Keywords (30 total):**
1-10: automation, plc programming, scada, process optimization, oee, data analysis, lean six sigma, root cause analysis, statistical process control, minitab

11-20: power bi, sql, python, manufacturing execution systems, continuous improvement, quality management, fmea, project management, cross-functional teams, kaizen

21-30: vendor management, cost reduction, supply chain, inventory control, 5s methodology, preventive maintenance, downtime reduction, production scheduling, workflow optimization, standard operating procedures

**V2 Bullet Strategy:**
- IIT Madras Bullet 1: Uses "automation," "plc programming," "scada," "oee"
- IIT Madras Bullet 2: Uses "power bi," "sql," "python," "continuous improvement"
- IIT Madras Bullet 3: Uses "vendor management," "cost reduction," "inventory control"
- A.V.C Bullet 1: Uses "process optimization," "lean six sigma," "minitab" (different from IIT Bullet 1)
- A.V.C Bullet 2: Uses "manufacturing execution systems," "fmea," "project management" (different from IIT Bullet 2)
- A.V.C Bullet 3: Uses "preventive maintenance," "downtime reduction," "5s methodology" (different from IIT Bullet 3)

## 🔍 Log Files

- V1 logs: `resume_tailor.log`
- V2 logs: `resume_tailor_v2.log`

Monitor V2 progress:
```bash
tail -f resume_tailor_v2.log
```

## ⚡ Performance

- V1: ~3-4 minutes per resume (15 keywords)
- V2: ~4-5 minutes per resume (30 keywords, more complex prompts)

## 🎯 When to Use V2

Use V2 when:
- Job posting has 20+ technical keywords
- ATS system is strict about keyword matching
- Work experience is more important than projects
- You want maximum keyword coverage
- Applying to competitive roles

## 📂 Files Created

- `automated_resume_tailor_v2.py` - Main V2 script
- `README_V2.md` - Detailed comparison
- `QUICK_START_V2.md` - This file
- `resume_tailor_v2.log` - V2 execution logs

## ✨ Key Benefits

1. **2x Keyword Coverage**: 30 keywords vs 15
2. **Experience-First**: Recruiters see work experience immediately
3. **Strategic Distribution**: Each bullet focuses on different keyword clusters
4. **Zero Redundancy**: All 6 bullets are completely unique
5. **ATS Optimized**: Maximum keyword saturation across all content
