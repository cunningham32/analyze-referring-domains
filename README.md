# IP Address Analysis Tool
=======================

This tool analyzes CSV files containing domain backlink data to identify patterns in IP addresses. It specifically looks for:
- Multiple domains sharing the same IP address
- Domains using sequential IP addresses (same first two octets with sequential third octet)

## Setup
-----

1. Create a virtual environment:

Create virtual environment:
```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. Install required packages:
```bash
   pip install pandas
   ```

## Directory Structure
------------------

Before running the script, ensure your directory is structured as follows:
```
your-project-directory/
├── analyze.py
├── reports/          # Place your CSV files here
└── processed/        # Created automatically; stores processed files
```

## Input File Requirements
----------------------

Your CSV files should include these columns:
- IP Address
- Country
- Domain

## Usage
-----

1. Place your CSV files in the 'reports' directory

2. Run the script:
```bash
   python analyze.py
   ```

## Results
-------

For each processed CSV file:
1. A new results file will be created with the naming pattern: '{original_name}_analysis_results.csv'
2. The original file will be moved to the 'processed' directory

The results CSV will contain:
- IP Address
- Country
- Domain
- Group Type (either 'Identical' or 'Sequential')

Only groups with multiple related IP addresses will be included in the results.

## Example
-------

If you process 'backlinks.csv', you'll get:
- A new file 'backlinks_analysis_results.csv' in the main directory
- The original 'backlinks.csv' moved to the 'processed' directory

## Deactivating Virtual Environment
--------------------------------

When finished, deactivate the virtual environment:
```bash
deactivate 
```
