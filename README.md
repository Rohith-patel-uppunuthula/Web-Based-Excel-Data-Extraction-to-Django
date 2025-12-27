# Web-Based-Excel-Data-Extraction-to-Django
# 📊 Excel Data Extraction to Django Models (MVP)

## Overview
This project is a **proof-of-concept (MVP)** that validates end-to-end data flow from a **web portal providing monthly Excel sheets** into a **local Django database**.

The current phase focuses on **one-time execution only** to ensure correctness before introducing automation.

---

## Problem Statement
- A single URL exposes **multiple monthly Excel files**
- Each Excel file contains data for **multiple areas**
- Requirement:
  - Select **one specific area**
  - Extract its data
  - Save it into **Django models**

---

## Scope

### ✅ Implemented
- Website flow analysis
- One-time Excel download
- Excel parsing using Pandas
- Area-based data filtering
- Data persistence in Django models

### ❌ Not Implemented (Yet)
- Monthly looping
- Scheduling / automation
- Background processing
- Retry & logging mechanisms

---

## Tech Stack
- Django
- Selenium
- Pandas
- Python 3.x

---

## Project Structure
project_root/
│
├── manage.py
├── core/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── scraper/
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── models.py
│ ├── services/
│ │ ├── init.py
│ │ ├── browser.py # website navigation & Excel download
│ │ ├── excel_parser.py # Excel reading & filtering
│ │ └── saver.py # save data into models
│ ├── scripts/
│ │ ├── init.py
│ │ └── run_once.py # one-time execution entry point
│ └── migrations/
│
├── media/
│ └── downloads/ # Excel files downloaded here
│
└── requirements.txt


---

## Workflow
1. Open the target website
2. Navigate to monthly Excel list
3. Download one Excel file
4. Read Excel using Pandas
5. Filter required area
6. Save extracted data into Django models
7. Verify data using Django Admin

---

## Django Model (Example)
python
from django.db import models

class TestData(models.Model):
    area = models.CharField(max_length=100)
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.area

requirements.txt
Django>=4.2
selenium>=4.15.0
pandas>=2.0.0
openpyxl>=3.1.0
webdriver-manager>=4.0.0
