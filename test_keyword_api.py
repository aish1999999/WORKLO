#!/usr/bin/env python3
"""Test keyword extraction API"""
import requests
import json

JOB_DESCRIPTION = """The Process Engineer should develop control plans, monitor process parameters using SPC and MSA, implement 5S and waste reduction initiatives, perform failure analysis, and establish safety procedures. Focus on material handling, ergonomics, KPIs, and failure modes mitigation."""

response = requests.post(
    "http://localhost:8000/api/extract-keywords",
    data={
        "job_description": JOB_DESCRIPTION,
        "job_title": "Process Engineer"
    }
)

print(f"Status Code: {response.status_code}")
print(f"\nResponse:")
try:
    result = response.json()
    print(json.dumps(result, indent=2))

    # Check if keywords key exists
    if "keywords" in result:
        keywords = result["keywords"]
        print(f"\n✅ Got {len(keywords)} keywords")
        print(f"First 5 keywords:")
        for k in keywords[:5]:
            print(f"  - {k}")
    else:
        print("\n❌ No 'keywords' key in response")

except Exception as e:
    print(f"Error: {e}")
    print(f"Raw response: {response.text}")
