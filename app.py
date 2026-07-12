import streamlit as st
import json
import os

# Page Configuration for wide layout
st.set_page_config(layout="wide")

@st.cache_data
def load_code_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {}

data = load_code_data()

st.title("🏗️ Multi-Code Clause Cross-Reference Tool")

if "concrete_cover" in data:
    item = data["concrete_cover"]
    st.subheader(item["title"])
    st.caption(item["description"])
    st.markdown("---")
    
    # Loop through each standard cleanly as a structural block row
    for std in item["standards"]:
        # Code Header Row
        st.markdown(f"### 📘 {std['code_name']}")
        
        # Grid layout for the specific code parameters
        col1, col2, col3 = st.columns([1, 2, 2])
        
        with col1:
            st.markdown(f"**Clause Ref:**\n`{std['clause']}`")
            st.markdown(f"**Notes:**\n*{std['notes']}*")
            
        with col2:
            st.markdown("**Permissible Limits / Criteria:**")
            st.markdown(std['limits'], unsafe_allow_html=True)
            
        with col3:
            st.markdown("**Governing Equation:**")
            st.markdown(std['formula'])
            st.markdown("**Parameter Breakdown:**")
            st.markdown(std['notation'], unsafe_allow_html=True)
            
        st.markdown("---")
else:
    st.error("Target data key not found. Please verify data.json matches.")
