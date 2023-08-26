import pandas as pd
import re
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Upload a csv and correlate its columns!")
st.caption("Totally secure. Trust me, bro.")


def sanitize_data(df):
    df.columns = df.columns.str.strip()
    df.columns = df.columns.map(lambda x: re.sub(r'\W+', '_', x))
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def display_box_plots(df, selected_columns):
    st.write("Box Plots:")
    for column in selected_columns:
        try:
            df[column] = pd.to_numeric(df[column], errors='coerce')
        except:
            st.error("Cannot convert to numeric column")

            return

        plt.figure(figsize=(8, 6))
        sns.boxplot(x=column, data=df)
        plt.xlabel(column)
        plt.ylabel("Value")
        plt.title(f"Box Plot of {column}")
        st.pyplot(plt)


def display_pair_plots(df, selected_columns):
    st.write("Pair Plots (Scatter Plot Matrix):")
    sns.pairplot(df[selected_columns])
    st.pyplot(plt)


def display_line_plots(df, selected_columns):
    st.write("Line Plots:")
    for column in selected_columns:
        plt.figure(figsize=(8, 6))
        plt.plot(df[column])
        plt.xlabel("Index")
        plt.ylabel(column)
        plt.xticks(rotation=90)
        plt.title(f"Line Plot of {column}")
        st.pyplot(plt)


def display_scatter_plots(df, selected_columns):
    st.write("Scatter Plot:")
    plt.figure(figsize=(8, 6))
    plt.scatter(df[selected_columns[0]], df[selected_columns[1]])
    plt.xlabel(selected_columns[0])
    plt.ylabel(selected_columns[1])
    plt.xticks(rotation=90)
    plt.title(f"Scatter Plot between {selected_columns[0]} and {selected_columns[1]}")
    st.pyplot(plt)


def display_histograms(df, selected_columns):
    st.write("Histograms:")
    for column in selected_columns:
        plt.figure(figsize=(8, 6))
        plt.hist(df[column], bins=df[column].nunique())
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.title(f"Histogram of {column}")
        plt.xticks(rotation=90)
        st.pyplot(plt)


try:
    uploaded_file = st.file_uploader('Upload your csv', type=['csv'])
except UnicodeDecodeError:
    st.error("Something went wrong with the upload. ¯\_(ツ)_/¯")

# try:
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    df = sanitize_data(df)

    st.dataframe(df)

    selected_columns = st.multiselect(
        'Select collumns for correlation', df.columns)

    if len(selected_columns) >= 1:
        # Data Visualization Options
        visualization_option = st.selectbox(
            "Select a visualization option",
            [
                "Box", "Line", "Pair", "Histogram", "Scatter",
            ]
        )

        if visualization_option == "Box":
            display_box_plots(df, selected_columns)
        elif visualization_option == "Pair":
            display_pair_plots(df, selected_columns)
        elif visualization_option == "Line":
            display_line_plots(df, selected_columns)
        elif visualization_option == "Scatter":
            display_scatter_plots(df, selected_columns)
        elif visualization_option == "Histogram":
            display_histograms(df, selected_columns)
    else:
        st.warning("Select at least one column for analysis.")
# except Exception as err:
#     st.error(
#         "Something went wrong. Maybe non-numeric collumns? I havent really data-proofed this much")
