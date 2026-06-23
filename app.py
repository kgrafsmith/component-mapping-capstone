import streamlit as st
import json

# Load data
with open("mappings.json", "r") as f:
    mappings = json.load(f)

st.set_page_config(page_title="Component Mapping Explorer", layout="wide")

st.title("Component Mapping Explorer")
st.caption("Multi-select exploration of Category → Material → Intended Use → Format")

# -----------------------------
# CATEGORY (multi-select)
# -----------------------------
categories = st.multiselect(
    "Select Category(ies)",
    list(mappings.keys())
)

if not categories:
    st.info("Select at least one category to begin.")
    st.stop()

# -----------------------------
# MATERIALS (multi-select, filtered by categories)
# -----------------------------
all_materials = set()

for cat in categories:
    all_materials.update(mappings[cat].keys())

materials = st.multiselect(
    "Select Material(s)",
    sorted(all_materials)
)

if not materials:
    st.info("Select at least one material.")
    st.stop()

# -----------------------------
# INTENDED USES (multi-select, filtered by category + material)
# -----------------------------
all_uses = set()

for cat in categories:
    for mat in materials:
        if mat in mappings.get(cat, {}):
            all_uses.update(mappings[cat][mat].keys())

uses = st.multiselect(
    "Select Intended Use(s)",
    sorted(all_uses)
)

if not uses:
    st.info("Select at least one intended use.")
    st.stop()

# -----------------------------
# EXPAND ALL VALID PATHS
# -----------------------------
results = []

for cat in categories:
    for mat in materials:
        if mat in mappings.get(cat, {}):
            for use in uses:
                if use in mappings[cat][mat]:
                    for fmt in mappings[cat][mat][use]:
                        results.append({
                            "Category": cat,
                            "Material": mat,
                            "Intended Use": use,
                            "Format": fmt
                        })


st.subheader("Table View: Valid Component Mappings")
st.dataframe(results)


import pandas as pd
from datetime import datetime

st.divider()
st.subheader("Don't see your mapping? Request it here")

# Initialize session storage
if "requests" not in st.session_state:
    st.session_state.requests = []

with st.form("ticket_form"):
    component = st.text_input("Component Name")
    mapping_request = st.text_area("What mapping do you need?")
    submitted = st.form_submit_button("Submit Request")

if submitted:
    if component and mapping_request:

        new_row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "component": component,
            "mapping_request": mapping_request
        }

        st.session_state.requests.append(new_row)

        st.success("Request added!")
    else:
        st.error("Please fill out both fields.")

# Convert to DataFrame
df = pd.DataFrame(st.session_state.requests)

st.subheader("All Requests")

if not df.empty:
    st.dataframe(df)

    # Download as Excel
    excel_file = "help_requests.xlsx"
    df.to_excel(excel_file, index=False)

    with open(excel_file, "rb") as f:
        st.download_button(
            "Download Excel File",
            f,
            file_name="help_requests.xlsx"
        )