# LinkedIn Scraper - README

## Overview

The LinkedIn Lead Scraper is a powerful web application built with Streamlit that helps you find and manage quality leads from LinkedIn. This tool allows you to search for potential leads based on keywords and location, filter results, and export data in various formats.

## Features

- **User Authentication**: Secure login system to protect your data
- **LinkedIn Search**: Find leads using keywords and location filters
- **Lead Management**: View, filter, and qualify leads in an interactive table
- **Custom Filters**: Create and save filters to identify high-quality leads
- **Data Export**: Export your leads in CSV or Excel format
- **Responsive Design**: Works on desktop and mobile devices

## Files in this Package

- `app.py`: The main Streamlit application code
- `requirements.txt`: List of Python dependencies
- `user_guide.md`: Comprehensive guide for using the application
- `deployment_guide.md`: Instructions for deploying to Streamlit Cloud

## Quick Start

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application locally:
   ```
   streamlit run app.py
   ```

3. Access the application at http://localhost:8501

## Deployment

For permanent deployment, follow the instructions in `deployment_guide.md` to deploy the application to Streamlit Cloud.

## Login Credentials

For demonstration purposes, use:
- Username: `demo`
- Password: `demo123`

## Requirements

- Python 3.7 or higher
- Streamlit
- Pandas
- Selenium (for actual LinkedIn scraping implementation)
- BeautifulSoup4 (for actual LinkedIn scraping implementation)

## Important Notes

- This application simulates LinkedIn scraping for demonstration purposes
- In a production environment, you would need to implement actual scraping functionality
- Always respect LinkedIn's terms of service and rate limits when scraping

## License

This project is licensed under the MIT License - see the LICENSE file for details.
