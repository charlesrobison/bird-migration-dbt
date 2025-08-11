import streamlit as st
import duckdb

# Title
st.title("My DuckDB + Streamlit App")

# Connect to DuckDB
con = duckdb.connect("dev.duckdb")  # Change to your DB path if needed

# Run a sample query
df = con.execute("SELECT * FROM stg_recent_observations LIMIT 5").df()

# Show the dataframe
st.write("Sample Data from DuckDB:")
st.dataframe(df)
