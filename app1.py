import streamlit as st
import requests

st.title("GitHub User Repositories")

# Input for GitHub username
username = st.text_input("Enter GitHub username")

# Fetch repositories if username is provided
if username:
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    
    if response.status_code == 200:
        repos = response.json()
        if repos:
            for repo in repos:
                st.write(f"**Repository Name:** {repo['name']}")
                st.write(f"**Description:** {repo['description']}")
                st.write(f"**URL:** {repo['html_url']}")
                st.write("---")
        else:
            st.write("No repositories found.")
    else:
        st.write("Failed to fetch repositories.")
