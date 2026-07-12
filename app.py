import streamlit as st
import json
import os

# 1. Page Configuration for an expansive wide layout
st.set_page_config(
    page_title="Multi-Code Clause Cross-Reference Tool",
    page_icon="🏗️",
    layout="wide"
)

# 2. Hard-load Data (No cache to prevent development data mismatches)
def load_code_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {}

data = load_code_data()

st.title("🏗️ Multi-Code Clause Cross-Reference Tool")
st.caption("Production-ready side-by-side technical standard matrix mapping global structural engineering criteria.")
st.markdown("---")

# 3. Dynamic Structural Grid Rendering Engine
if "concrete_cover" in data:
    item = data["concrete_cover"]
    st.subheader(item["title"])
    st.info(item["description"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Track row sequence for clean grouping UI
    for idx, std in enumerate(item["standards"]):
        # Code Master Header Block
        st.markdown(f"#### 📘 {std['code_name']}")
        
        # 3-Column Split to handle highly detailed, asymmetric data loads without text overlapping
        col_meta, col_limits, col_equations = st.columns([1.2, 2.3, 2.5])
        
        with col_meta:
            st.markdown("**Clause Reference:**")
            st.code(std['clause'], language="text")
            st.markdown("**Notes:**")
            st.markdown(f"*{std['notes']}*")
            
        with col_limits:
            st.markdown("**Permissible Limits / Criteria:**")
            st.markdown(std['limits'], unsafe_allow_html=True)
            
        with col_equations:
            st.markdown("**Governing Equation:**")
            if std['formula'] == "No Formula Provided":
                st.caption("*No Formula Provided*")
            else:
                st.markdown(std['formula'])
                
            st.markdown("**Parameter Breakdown & Notations:**")
            st.markdown(std['notation'], unsafe_allow_html=True)
            
        # Add visual separator between separate engineering codes
        st.markdown("<hr style='margin-top:1em;margin-bottom:2em;border-color:#4A5568;'>", unsafe_allow_html=True)
else:
    st.error("Target data key 'concrete_cover' not found inside data.json. Ensure your JSON matches the new 'standards' list structure exactly.")
