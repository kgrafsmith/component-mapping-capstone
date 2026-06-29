import streamlit as st
import json

# Load data
with open("mappings.json", "r") as f:
    mappings = json.load(f)

# Fomat Page; Titles, Headers, Caption
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


st.divider()
st.subheader("Don't see your mapping? Submit a request")

st.markdown(
    """
    👉 Submit a request here:
    https://forms.office.com/Pages/ResponsePage.aspx?id=BP0ZkiIsZECVetvKJbSpjFH7PB2hgExHqBx7f12zMDRUMVRPNlBOTjBLTTRVU1lLNFo3MVpOTFBPRC4u
    """
)