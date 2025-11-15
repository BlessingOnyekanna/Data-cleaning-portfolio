@"
# E-Commerce Data Cleaning Portfolio Project

A comprehensive data cleaning pipeline that demonstrates end-to-end data quality improvement techniques using Python and Pandas.

## 📋 Project Overview

This project showcases professional data cleaning skills by:
1. Generating a realistic messy e-commerce dataset with intentional quality issues
2. Building a robust cleaning pipeline with 9 specialized functions
3. Producing clean, analysis-ready data with comprehensive quality reports

## 🎯 Business Problem

Raw e-commerce data often contains quality issues that prevent accurate analysis:
- Duplicate orders inflating metrics
- Inconsistent formatting breaking automated systems
- Missing critical information reducing dataset usability
- Invalid data leading to incorrect business decisions

This pipeline solves these problems systematically.

## 🛠️ Technologies Used

- **Python 3.14**
- **Pandas** - Data manipulation and cleaning
- **NumPy** - Numerical operations
- **Regex** - Pattern matching for validation
- **datetime** - Date standardization

## 📊 Data Quality Issues Addressed

| Issue Type | Examples | Solution |
|------------|----------|----------|
| **Duplicates** | 35 duplicate orders | Removed exact duplicates |
| **Whitespace** | \`"  John  Smith  "\` | Trimmed and normalized |
| **Invalid Emails** | \`john@\`, \`@smith.com\` | Validated format, marked invalid as missing |
| **Phone Formats** | \`(555)-123-4567\`, \`555.123.4567\` | Standardized to \`XXX-XXX-XXXX\` |
| **Date Formats** | \`01/15/2024\`, \`15-01-2024\`, \`Jan 15, 2024\` | Converted to \`YYYY-MM-DD\` |
| **Price Formats** | \`$49.99\`, \`$1,234.56\` | Removed symbols, converted to float |
| **Invalid Quantities** | \`-5\`, \`0\`, \`"3"\` | Validated positive integers |
| **Category Variations** | \`Electronics\`, \`ELECTRONICS\`, \`elec\` | Standardized to consistent names |
| **Status Variations** | \`Shipped\`, \`SHIPPED\`, \`Shippd\` | Consolidated to 4 standard values |

## 🖼️ Screenshots

### Data Cleaning Pipeline in Action
![Pipeline Running](screenshots/pipeline-running.png.png)

### Before: Messy Data
![Messy Data](screenshots/messy-data.png.png)

### After: Clean Data
![Clean Data](screenshots/cleaned-data.png.png)

### Comprehensive Cleaning Report
![Cleaning Report](screenshots/cleaning-report1.png.png)

## 📁 Project Structure

\`\`\`
data-cleaning-portfolio/
├── data/
│   ├── raw/
│   │   └── ecommerce_orders_messy.csv       # Generated messy dataset
│   └── cleaned/
│       └── ecommerce_orders_cleaned.csv     # Cleaned output
├── scripts/
│   ├── generate_messy_data.py               # Creates test dataset
│   └── clean_data.py                        # Main cleaning pipeline
├── reports/
│   └── cleaning_report.txt                  # Detailed cleaning report
├── screenshots/                             # Project screenshots
├── requirements.txt                         # Python dependencies
└── README.md                                # Project documentation
\`\`\`

## 🚀 How to Run

### 1. Clone the repository
\`\`\`bash
git clone https://github.com/YOUR-USERNAME/data-cleaning-portfolio.git
cd data-cleaning-portfolio
\`\`\`

### 2. Set up virtual environment
\`\`\`bash
python -m venv venv

# On Windows:
.\venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
\`\`\`

### 3. Install dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Generate messy dataset
\`\`\`bash
python scripts/generate_messy_data.py
\`\`\`

### 5. Run cleaning pipeline
\`\`\`bash
python scripts/clean_data.py
\`\`\`

## 📈 Results

### Before Cleaning
- **Total Rows:** 250
- **Duplicates:** 35
- **Missing Emails:** 34
- **Missing Phones:** 41
- **Invalid Dates:** 14
- **Category Variations:** 16
- **Status Variations:** 20

### After Cleaning
- **Total Rows:** 215 (35 duplicates removed)
- **Valid Emails:** 133 (48 invalid removed)
- **Valid Phones:** 179 (standardized format)
- **Valid Dates:** 199 (YYYY-MM-DD format)
- **Valid Prices:** 211 (numeric format)
- **Category Variations:** 4 (consolidated)
- **Status Variations:** 4 (standardized)

**Data Quality Improvement: ~85% cleaner dataset**

## 💡 Skills Demonstrated

- **Data Quality Assessment** - Identifying and categorizing data issues
- **Data Transformation** - Standardizing formats and structures
- **Data Validation** - Implementing business rules and constraints
- **Python Programming** - OOP, pandas operations, regex
- **Documentation** - Clear code comments and project documentation
- **Problem Solving** - Handling edge cases and invalid data

## 📧 Contact

LinkedIn: [Your LinkedIn Profile]
GitHub: [Your GitHub Profile]

## 📄 License

This project is open source and available under the MIT License.
"@ | Out-File -FilePath README.md -Encoding utf8