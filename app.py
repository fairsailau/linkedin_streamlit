import streamlit as st
import pandas as pd
import time
import random
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="LinkedIn Lead Scraper",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0077B5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0077B5;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
        border-left: 4px solid #0077B5;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0077B5;
    }
    .metric-label {
        font-size: 1rem;
        color: #6c757d;
    }
    .footer {
        margin-top: 3rem;
        text-align: center;
        color: #6c757d;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'leads' not in st.session_state:
    st.session_state.leads = pd.DataFrame(columns=[
        'name', 'title', 'company', 'location', 'industry', 
        'company_size', 'connections', 'profile_url', 'is_qualified'
    ])
if 'filters' not in st.session_state:
    st.session_state.filters = []
if 'current_job' not in st.session_state:
    st.session_state.current_job = None

# Mock user credentials (in a real app, this would be stored securely)
USERS = {
    "admin": "password123",
    "demo": "demo123"
}

# Mock function to simulate LinkedIn scraping
def scrape_linkedin(keywords, location, page_limit):
    """Simulate scraping LinkedIn profiles based on search criteria"""
    st.info(f"Searching LinkedIn for '{keywords}' in '{location}'...")
    
    # Simulate processing time
    progress_bar = st.progress(0)
    for i in range(page_limit):
        # Simulate page scraping
        time.sleep(0.5)
        progress_bar.progress((i + 1) / page_limit)
    
    # Generate mock data
    num_results = random.randint(5, 15) * page_limit
    
    # Job titles related to keywords
    job_titles = [
        "Software Engineer", "Senior Developer", "Product Manager",
        "Data Scientist", "Marketing Specialist", "Sales Director",
        "Account Executive", "HR Manager", "Operations Director",
        "CEO", "CTO", "CFO", "VP Engineering", "VP Sales"
    ]
    
    # Companies
    companies = [
        "Google", "Microsoft", "Amazon", "Facebook", "Apple",
        "Netflix", "Salesforce", "Oracle", "IBM", "Intel",
        "Cisco", "Adobe", "Twitter", "LinkedIn", "Uber"
    ]
    
    # Locations
    locations = [location] * 5 + ["Remote", "New York", "San Francisco", "London", "Berlin"]
    
    # Industries
    industries = [
        "Technology", "Software", "Finance", "Healthcare", "Education",
        "Retail", "Manufacturing", "Consulting", "Marketing", "Media"
    ]
    
    # Company sizes
    company_sizes = [
        "1-10", "11-50", "51-200", "201-500", "501-1000",
        "1001-5000", "5001-10000", "10000+"
    ]
    
    # Connections
    connections = ["500+", "500+", "500+", "200-500", "100-200", "50-100", "<50"]
    
    # Generate mock leads
    leads = []
    for i in range(num_results):
        name = f"Person {i+1}"
        title = random.choice(job_titles)
        company = random.choice(companies)
        loc = random.choice(locations)
        industry = random.choice(industries)
        company_size = random.choice(company_sizes)
        connection = random.choice(connections)
        profile_url = f"https://linkedin.com/in/person{i+1}"
        is_qualified = random.choice([True, False])
        
        leads.append({
            'name': name,
            'title': title,
            'company': company,
            'location': loc,
            'industry': industry,
            'company_size': company_size,
            'connections': connection,
            'profile_url': profile_url,
            'is_qualified': is_qualified
        })
    
    return pd.DataFrame(leads)

# Function to filter leads based on criteria
def filter_leads(leads_df, filter_criteria):
    """Filter leads based on specified criteria"""
    filtered_df = leads_df.copy()
    
    if filter_criteria.get('job_titles'):
        titles = [t.strip().lower() for t in filter_criteria['job_titles'].split(',')]
        filtered_df = filtered_df[filtered_df['title'].str.lower().apply(
            lambda x: any(title in x.lower() for title in titles)
        )]
    
    if filter_criteria.get('companies'):
        companies = [c.strip().lower() for c in filter_criteria['companies'].split(',')]
        filtered_df = filtered_df[filtered_df['company'].str.lower().apply(
            lambda x: any(company in x.lower() for company in companies)
        )]
    
    if filter_criteria.get('industries'):
        industries = [i.strip().lower() for i in filter_criteria['industries'].split(',')]
        filtered_df = filtered_df[filtered_df['industry'].str.lower().apply(
            lambda x: any(industry in x.lower() for industry in industries)
        )]
    
    if filter_criteria.get('locations'):
        locations = [l.strip().lower() for l in filter_criteria['locations'].split(',')]
        filtered_df = filtered_df[filtered_df['location'].str.lower().apply(
            lambda x: any(location in x.lower() for location in locations)
        )]
    
    if filter_criteria.get('min_connections') == '500+':
        filtered_df = filtered_df[filtered_df['connections'] == '500+']
    elif filter_criteria.get('min_connections') == '200-500':
        filtered_df = filtered_df[filtered_df['connections'].isin(['500+', '200-500'])]
    elif filter_criteria.get('min_connections') == '100-200':
        filtered_df = filtered_df[filtered_df['connections'].isin(['500+', '200-500', '100-200'])]
    
    if filter_criteria.get('qualified_only'):
        filtered_df = filtered_df[filtered_df['is_qualified'] == True]
    
    return filtered_df

# Login page
def show_login_page():
    st.markdown("<h1 class='main-header'>LinkedIn Lead Scraper</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Login")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username in USERS and USERS[username] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='footer'>
        <p>For demonstration purposes, use:</p>
        <p>Username: <code>demo</code> | Password: <code>demo123</code></p>
    </div>
    """, unsafe_allow_html=True)

# Dashboard page
def show_dashboard():
    st.markdown("<h1 class='main-header'>LinkedIn Lead Scraper</h1>", unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"**Welcome, {st.session_state.username}!**")
        st.divider()
        
        page = st.radio("Navigation", [
            "Dashboard", 
            "Search LinkedIn", 
            "Manage Leads", 
            "Create Filters", 
            "Settings"
        ])
        
        st.divider()
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.experimental_rerun()
    
    # Page content
    if page == "Dashboard":
        show_dashboard_page()
    elif page == "Search LinkedIn":
        show_search_page()
    elif page == "Manage Leads":
        show_leads_page()
    elif page == "Create Filters":
        show_filters_page()
    elif page == "Settings":
        show_settings_page()

# Dashboard page content
def show_dashboard_page():
    st.markdown("<h2 class='sub-header'>Dashboard</h2>", unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>{}</div>
            <div class='metric-label'>Searches</div>
        </div>
        """.format(len(st.session_state.search_history)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>{}</div>
            <div class='metric-label'>Total Leads</div>
        </div>
        """.format(len(st.session_state.leads)), unsafe_allow_html=True)
    
    with col3:
        qualified_leads = len(st.session_state.leads[st.session_state.leads['is_qualified'] == True]) if not st.session_state.leads.empty else 0
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>{}</div>
            <div class='metric-label'>Qualified Leads</div>
        </div>
        """.format(qualified_leads), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-value'>{}</div>
            <div class='metric-label'>Filters</div>
        </div>
        """.format(len(st.session_state.filters)), unsafe_allow_html=True)
    
    # Recent activity
    st.markdown("<h3 class='sub-header'>Recent Activity</h3>", unsafe_allow_html=True)
    
    if st.session_state.search_history:
        for search in reversed(st.session_state.search_history[-5:]):
            st.markdown(f"""
            <div class='card'>
                <strong>Search:</strong> {search['keywords']} in {search['location']}<br>
                <strong>Date:</strong> {search['date']}<br>
                <strong>Results:</strong> {search['results']} leads found
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent activity. Start by searching for leads on LinkedIn.")
    
    # Quick actions
    st.markdown("<h3 class='sub-header'>Quick Actions</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("New Search", use_container_width=True):
            st.session_state.page = "Search LinkedIn"
            st.experimental_rerun()
    
    with col2:
        if st.button("View All Leads", use_container_width=True):
            st.session_state.page = "Manage Leads"
            st.experimental_rerun()
    
    with col3:
        if st.button("Create Filter", use_container_width=True):
            st.session_state.page = "Create Filters"
            st.experimental_rerun()

# Search page content
def show_search_page():
    st.markdown("<h2 class='sub-header'>Search LinkedIn</h2>", unsafe_allow_html=True)
    
    with st.form("search_form"):
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        keywords = st.text_input("Keywords (e.g., 'software engineer python')")
        location = st.text_input("Location (e.g., 'San Francisco')")
        page_limit = st.slider("Number of pages to scrape", 1, 10, 3)
        
        search_submitted = st.form_submit_button("Start Search")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    if search_submitted and keywords and location:
        # Simulate scraping
        new_leads = scrape_linkedin(keywords, location, page_limit)
        
        # Update session state
        if not st.session_state.leads.empty:
            st.session_state.leads = pd.concat([st.session_state.leads, new_leads]).reset_index(drop=True)
        else:
            st.session_state.leads = new_leads
        
        # Add to search history
        st.session_state.search_history.append({
            'keywords': keywords,
            'location': location,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'results': len(new_leads)
        })
        
        st.success(f"Search completed! Found {len(new_leads)} leads.")
        
        # Display results
        st.markdown("<h3 class='sub-header'>Search Results</h3>", unsafe_allow_html=True)
        st.dataframe(new_leads, use_container_width=True)
        
        # Export options
        st.markdown("<h3 class='sub-header'>Export Results</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Export as CSV", use_container_width=True):
                csv = new_leads.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"linkedin_leads_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("Export as Excel", use_container_width=True):
                # Create a temporary Excel file
                excel_file = f"linkedin_leads_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
                new_leads.to_excel(excel_file, index=False)
                
                # Read the file and provide download button
                with open(excel_file, "rb") as f:
                    excel_data = f.read()
                
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name=excel_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
                # Clean up the temporary file
                os.remove(excel_file)

# Leads page content
def show_leads_page():
    st.markdown("<h2 class='sub-header'>Manage Leads</h2>", unsafe_allow_html=True)
    
    if st.session_state.leads.empty:
        st.info("No leads found. Start by searching for leads on LinkedIn.")
        return
    
    # Filters
    st.markdown("<h3 class='sub-header'>Filter Leads</h3>", unsafe_allow_html=True)
    
    with st.expander("Filter Options", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            filter_title = st.text_input("Filter by Job Title")
            filter_company = st.text_input("Filter by Company")
            filter_qualified = st.checkbox("Show only qualified leads")
        
        with col2:
            filter_industry = st.text_input("Filter by Industry")
            filter_location = st.text_input("Filter by Location")
            filter_connections = st.selectbox(
                "Minimum Connections",
                options=["Any", "500+", "200-500", "100-200"]
            )
        
        # Apply filters
        filtered_df = st.session_state.leads.copy()
        
        if filter_title:
            filtered_df = filtered_df[filtered_df['title'].str.contains(filter_title, case=False)]
        
        if filter_company:
            filtered_df = filtered_df[filtered_df['company'].str.contains(filter_company, case=False)]
        
        if filter_industry:
            filtered_df = filtered_df[filtered_df['industry'].str.contains(filter_industry, case=False)]
        
        if filter_location:
            filtered_df = filtered_df[filtered_df['location'].str.contains(filter_location, case=False)]
        
        if filter_connections != "Any":
            if filter_connections == "500+":
                filtered_df = filtered_df[filtered_df['connections'] == '500+']
            elif filter_connections == "200-500":
                filtered_df = filtered_df[filtered_df['connections'].isin(['500+', '200-500'])]
            elif filter_connections == "100-200":
                filtered_df = filtered_df[filtered_df['connections'].isin(['500+', '200-500', '100-200'])]
        
        if filter_qualified:
            filtered_df = filtered_df[filtered_df['is_qualified'] == True]
    
    # Display leads
    st.markdown("<h3 class='sub-header'>Lead List</h3>", unsafe_allow_html=True)
    st.write(f"Showing {len(filtered_df)} of {len(st.session_state.leads)} leads")
    
    # Enable editing
    edited_df = st.data_editor(
        filtered_df,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "is_qualified": st.column_config.CheckboxColumn(
                "Qualified",
                help="Mark as a qualified lead",
                default=False,
            ),
            "profile_url": st.column_config.LinkColumn(
                "Profile URL",
                help="LinkedIn profile URL",
            ),
        },
        hide_index=True,
    )
    
    # Save changes
    if not filtered_df.equals(edited_df):
        # Update the main dataframe with edited values
        for index, row in edited_df.iterrows():
            # Find the corresponding row in the original dataframe
            original_index = st.session_state.leads[
                (st.session_state.leads['name'] == row['name']) & 
                (st.session_state.leads['company'] == row['company'])
            ].index
            
            if not original_index.empty:
                # Update the is_qualified status
                st.session_state.leads.loc[original_index, 'is_qualified'] = row['is_qualified']
        
        st.success("Changes saved successfully!")
    
    # Export options
    st.markdown("<h3 class='sub-header'>Export Leads</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export as CSV", use_container_width=True):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"linkedin_leads_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Export as Excel", use_container_width=True):
            # Create a temporary Excel file
            excel_file = f"linkedin_leads_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            filtered_df.to_excel(excel_file, index=False)
            
            # Read the file and provide download button
            with open(excel_file, "rb") as f:
                excel_data = f.read()
            
            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name=excel_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            # Clean up the temporary file
            os.remove(excel_file)

# Filters page content
def show_filters_page():
    st.markdown("<h2 class='sub-header'>Create Filters</h2>", unsafe_allow_html=True)
    
    # Create new filter
    with st.form("filter_form"):
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("New Filter")
        
        filter_name = st.text_input("Filter Name")
        job_titles = st.text_input("Job Titles (comma-separated)")
        companies = st.text_input("Companies (comma-separated)")
        industries = st.text_input("Industries (comma-separated)")
        locations = st.text_input("Locations (comma-separated)")
        min_connections = st.selectbox(
            "Minimum Connections",
            options=["Any", "500+", "200-500", "100-200"]
        )
        qualified_only = st.checkbox("Qualified leads only")
        
        filter_submitted = st.form_submit_button("Create Filter")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    if filter_submitted and filter_name:
        # Create new filter
        new_filter = {
            'name': filter_name,
            'job_titles': job_titles,
            'companies': companies,
            'industries': industries,
            'locations': locations,
            'min_connections': min_connections,
            'qualified_only': qualified_only,
            'date_created': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        st.session_state.filters.append(new_filter)
        st.success(f"Filter '{filter_name}' created successfully!")
    
    # Display existing filters
    st.markdown("<h3 class='sub-header'>Saved Filters</h3>", unsafe_allow_html=True)
    
    if not st.session_state.filters:
        st.info("No filters created yet.")
    else:
        for i, filter_item in enumerate(st.session_state.filters):
            with st.expander(f"{filter_item['name']} ({filter_item['date_created']})"):
                st.write(f"**Job Titles:** {filter_item['job_titles']}")
                st.write(f"**Companies:** {filter_item['companies']}")
                st.write(f"**Industries:** {filter_item['industries']}")
                st.write(f"**Locations:** {filter_item['locations']}")
                st.write(f"**Minimum Connections:** {filter_item['min_connections']}")
                st.write(f"**Qualified Only:** {'Yes' if filter_item['qualified_only'] else 'No'}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"Apply Filter", key=f"apply_{i}"):
                        # Apply filter to leads
                        filter_criteria = {
                            'job_titles': filter_item['job_titles'],
                            'companies': filter_item['companies'],
                            'industries': filter_item['industries'],
                            'locations': filter_item['locations'],
                            'min_connections': filter_item['min_connections'],
                            'qualified_only': filter_item['qualified_only']
                        }
                        
                        filtered_leads = filter_leads(st.session_state.leads, filter_criteria)
                        
                        st.session_state.filtered_leads = filtered_leads
                        st.success(f"Filter applied! Found {len(filtered_leads)} matching leads.")
                        
                        # Display filtered leads
                        st.dataframe(filtered_leads, use_container_width=True)
                        
                        # Export options
                        if not filtered_leads.empty:
                            csv = filtered_leads.to_csv(index=False)
                            st.download_button(
                                label="Download Filtered Results",
                                data=csv,
                                file_name=f"filtered_leads_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                                mime="text/csv"
                            )
                
                with col2:
                    if st.button(f"Delete Filter", key=f"delete_{i}"):
                        st.session_state.filters.pop(i)
                        st.experimental_rerun()

# Settings page content
def show_settings_page():
    st.markdown("<h2 class='sub-header'>Settings</h2>", unsafe_allow_html=True)
    
    # Account settings
    st.markdown("<h3 class='sub-header'>Account Settings</h3>", unsafe_allow_html=True)
    
    with st.expander("Change Password", expanded=False):
        with st.form("change_password_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Change Password"):
                if current_password != USERS[st.session_state.username]:
                    st.error("Current password is incorrect")
                elif new_password != confirm_password:
                    st.error("New passwords do not match")
                elif not new_password:
                    st.error("New password cannot be empty")
                else:
                    # In a real app, this would update the password in a database
                    USERS[st.session_state.username] = new_password
                    st.success("Password changed successfully!")
    
    # Application settings
    st.markdown("<h3 class='sub-header'>Application Settings</h3>", unsafe_allow_html=True)
    
    with st.expander("Scraper Settings", expanded=False):
        st.slider("Default page limit", 1, 10, 3)
        st.checkbox("Auto-qualify leads based on criteria")
        st.checkbox("Enable browser notifications")
    
    # Data management
    st.markdown("<h3 class='sub-header'>Data Management</h3>", unsafe_allow_html=True)
    
    with st.expander("Manage Data", expanded=False):
        if st.button("Clear Search History"):
            st.session_state.search_history = []
            st.success("Search history cleared!")
        
        if st.button("Clear All Leads"):
            st.session_state.leads = pd.DataFrame(columns=[
                'name', 'title', 'company', 'location', 'industry', 
                'company_size', 'connections', 'profile_url', 'is_qualified'
            ])
            st.success("All leads cleared!")
        
        if st.button("Clear All Filters"):
            st.session_state.filters = []
            st.success("All filters cleared!")
        
        if st.button("Reset All Data"):
            st.session_state.search_history = []
            st.session_state.leads = pd.DataFrame(columns=[
                'name', 'title', 'company', 'location', 'industry', 
                'company_size', 'connections', 'profile_url', 'is_qualified'
            ])
            st.session_state.filters = []
            st.success("All data reset successfully!")
    
    # About
    st.markdown("<h3 class='sub-header'>About</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card'>
        <h4>LinkedIn Lead Scraper</h4>
        <p>Version 1.0.0</p>
        <p>This application helps you find and manage quality leads from LinkedIn.</p>
        <p>Built with Streamlit.</p>
    </div>
    """, unsafe_allow_html=True)

# Main app logic
def main():
    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
