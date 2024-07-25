import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Title of the app
st.title("UAS MPML Data Analysis")

# Upload CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(data.head())

    # Preprocessing
    st.subheader("Data Preprocessing")
    data_cleaned = data.drop(columns=['Unnamed: 12'])
    st.write("Cleaned Data:")
    st.write(data_cleaned.head())

    # Check for missing values
    missing_values = data_cleaned.isnull().sum()
    st.write("Missing Values:")
    st.write(missing_values)

    # Perform one-hot encoding on categorical variables
    data_encoded = pd.get_dummies(data_cleaned, columns=[
        'Gender', 'Marital Status', 'Occupation', 'Monthly Income',
        'Educational Qualifications', 'Feedback', 'Output'
    ])
    st.write("Encoded Data:")
    st.write(data_encoded.head())

    # Plot distributions of age and family size
    st.subheader("Distributions of Age and Family Size")
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    sns.histplot(data_encoded['Age'], kde=True, color='skyblue', ax=ax[0])
    ax[0].set_title('Age Distribution')
    ax[0].set_xlabel('Age')
    ax[0].set_ylabel('Frequency')

    sns.histplot(data_encoded['Family size'], kde=True, color='lightgreen', ax=ax[1])
    ax[1].set_title('Family Size Distribution')
    ax[1].set_xlabel('Family Size')
    ax[1].set_ylabel('Frequency')

    st.pyplot(fig)

    # Plot correlation matrix
    st.subheader("Correlation Matrix")
    fig, ax = plt.subplots(figsize=(15, 10))
    correlation_matrix = data_encoded.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
