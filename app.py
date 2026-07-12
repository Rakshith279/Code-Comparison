import streamlit as st
import json
import os

# 1. Page Configuration for an expansive wide layout
st.set_page_config(
    page_title="Multi-Code Clause Cross-Reference Tool",
    page_icon="🏗️",
    layout="wide"
)

# 2. Hard-load Data without caching to allow instant updates
def load_code_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {"categories": {}}

data = load_code_data()
categories = data.get("categories", {})

st.title("🏗️ Multi-Code Clause Cross-Reference Tool")
st.caption("Production-ready side-by-side technical standard matrix mapping global structural engineering criteria.")
st.markdown("---")

if not categories:
    st.error("No engineering data found. Please ensure data.json is populated correctly.")
else:
    # 3. Top Search Engine
    search_query = st.text_input("🔍 Search Design Topics (e.g., 'cover', 'buckling', 'anchor', 'IS 456'):").strip().lower()
    
    # Filter topics based on search keywords or text parameters
    filtered_categories = {}
    for key, value in categories.items():
        search_blob = f"{value['title']} {value['description']} {value['keywords']}".lower()
        if not search_query or search_query in search_blob:
            filtered_categories[key] = value

    if not filtered_categories:
        st.warning("No structural topics found matching your search query.")
    else:
        # 4. Sidebar Navigation Panel using filtered dictionary elements
        st.sidebar.header("Design Categories")
        
        # Build map displaying clean titles instead of raw JSON keys
        display_map = {value['title']: key for key, value in filtered_categories.items()}
        selected_title = st.sidebar.radio("Select Target Structural Check:", list(display_map.keys()))
        
        # Retrieve the final chosen topic dataset
        target_key = display_map[selected_title]
        item = categories[target_key]
        
        # 5. Main Clean Interface Output
        st.subheader(item["title"])
        st.info(item["description"])
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Grid loop displaying all cataloged design standards for that category
        for std in item["standards"]:
            st.markdown(f"#### 📘 {std['code_name']}")
            
            # 3-Column Split to isolate content and lock horizontal lines
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
                
            # Consistent Row Line Separator
            st.markdown("<hr style='margin-top:1em;margin-bottom:2em;border-color:#4A5568;'>", unsafe_allow_html=True)
