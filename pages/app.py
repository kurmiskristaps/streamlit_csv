import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Upload a csv and correlate its columns!")

def display_correlation_heatmap(df, selected_columns):
    corr_matrix = df[selected_columns].corr()

    st.write("Correlation Matrix:")
    plt.figure(figsize=(10,8))

    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0)
    st.pyplot(plt)

def display_scatter_plots(df, selected_columns):
    st.write("Scatter Plots:")
    for column in selected_columns:
        plt.figure(figsize=(8, 6))
        plt.scatter(df[column], df[selected_columns[0]])
        plt.xlabel(column)
        plt.ylabel(selected_columns[0])
        plt.title(f"Scatter Plot between {column} and {selected_columns[0]}")
        st.pyplot(plt)

def display_histograms(df, selected_columns):
    st.write("Histograms:")
    for column in selected_columns:
        plt.figure(figsize=(8, 6))
        plt.hist(df[column], bins=20)
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.title(f"Histogram of {column}")
        st.pyplot(plt)


uploaded_file = st.file_uploader('Upload your csv', type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.dataframe(df)

    selected_columns = st.multiselect('Select collumns for correlation', df.columns)

    if len(selected_columns) >= 1:
        # Data Visualization Options
        visualization_option = st.selectbox(
            "Select a visualization option", ["Histogram", "Correlation Heatmap", "Scatter Plot", ]
        )

        if visualization_option == "Correlation Heatmap":
            display_correlation_heatmap(df, selected_columns)
        elif visualization_option == "Scatter Plot":
            display_scatter_plots(df, selected_columns)
        elif visualization_option == "Histogram":
            display_histograms(df, selected_columns)
    else:
        st.warning("Select at least one column for analysis.")