import streamlit as st
import pandas as pd


# Load the precomputed data from cached_data.csv
@st.cache_data
def load_cached_data():
    return pd.read_csv("./experimentals/cached_data.csv")


# Streamlit UI
st.title("Sentence Comparison")

# Load the precomputed results
df = load_cached_data()

# Model selection using Multi-Select (Now Includes SecBERT)
unique_models = sorted(df["Model"].unique())  # Ensure consistent order
selected_models = st.multiselect(
    "Select Models to Compare", options=unique_models, default=unique_models
)

# Algorithm selection
similarity_algorithms = [
    "Cosine Similarity",
    "Euclidean Distance",
    "Manhattan Distance",
    "Mahalanobis Distance",
    "Jaccard Similarity",
    "Levenshtein Distance",
    "Hamming Distance",
]
selected_algo = st.selectbox("Select Algorithm", options=similarity_algorithms)

# Table display button
if st.button("Display Results"):
    if selected_algo not in df.columns:
        st.error(f"Error: '{selected_algo}' column is missing in cached_data.csv!")
    else:
        # Filter DataFrame by selected models
        selected_results = df[df["Model"].isin(selected_models)]

        # Pivot the table to show models side-by-side for comparison
        display_df = selected_results.pivot_table(
            index=["Description", "First Sentence", "Second Sentence"],
            columns="Model",
            values=selected_algo,
        ).reset_index()

        # Ensure consistent column order based on selected models
        column_order = ["Description", "First Sentence", "Second Sentence"] + sorted(
            selected_models
        )
        display_df = display_df[column_order]

        # Remove column index title
        display_df.columns.name = None

        # Apply custom CSS to wrap text in the sentence columns
        st.markdown(
            """
            <style>
            .stDataFrame div[data-testid="stVerticalBlock"] {
                overflow-wrap: break-word;
                word-break: break-word;
                white-space: normal !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Display the results with text wrapping
        st.dataframe(display_df, use_container_width=True)
