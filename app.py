import streamlit as st
import json

st.set_page_config(page_title="Global Structural Code Matrix", layout="wide")
st.title("🏗️ Smart Structural Engineering Multi-Code Index")
st.subheader("Instantly map equivalents across IS, IRC, Eurocode, ACI, and fib Model Code standards.")
st.markdown("---")

try:
    with open("data.json", "r", encoding="utf-8") as f:
        database = json.load(f)
except FileNotFoundError:
    st.error("Missing data.json file in your directory.")
    st.stop()

user_query = st.text_input("🔎 Type a design check or component:", placeholder="e.g., Concrete cover...").strip().lower()
matched_entries = []

if user_query:
    for key, data in database.items():
        if user_query in data["title"].lower() or user_query in data["description"].lower() or any(user_query in kw.lower() for kw in data["keywords"]):
            matched_entries.append(data)
else:
    matched_entries = list(database.values())

if not matched_entries:
    st.warning("⚠️ No specific match found.")
else:
    for topic in matched_entries:
        with st.expander(f"📊 {topic['title']}", expanded=True):
            st.markdown(f"**Engineering Objective:** {topic['description']}")
            st.markdown("---")
            
            code_items = list(topic["codes"].items())
            
            cols1 = st.columns(len(code_items))
            for idx, (code_name, details) in enumerate(code_items):
                with cols1[idx]:
                    st.markdown(f"#### {code_name}")
                    st.info(f"📑 **{details['clause']}**")
            
            st.markdown("---")
            st.markdown("### 📏 Permissible Limits / Criteria")
            cols2 = st.columns(len(code_items))
            for idx, (code_name, details) in enumerate(code_items):
                with cols2[idx]:
                    st.markdown(f"{details['limit']}")
            
            st.markdown("---")
            st.markdown("### 🧮 Governing Equations")
            cols3 = st.columns(len(code_items))
            for idx, (code_name, details) in enumerate(code_items):
                with cols3[idx]:
                    if "$$" in details['formula']:
                        st.latex(details['formula'].replace("$$", ""))
                    else:
                        st.markdown(f"*{details['formula']}*")
            
            st.markdown("---")
            st.markdown("### 📝 Parameter Breakdown & Notations")
            cols4 = st.columns(len(code_items))
            for idx, (code_name, details) in enumerate(code_items):
                with cols4[idx]:
                    if "notation" in details:
                        st.caption(details["notation"])
            
            st.markdown("---")
            st.markdown("### 🏢 Design Office Operational Notes")
            cols5 = st.columns(len(code_items))
            for idx, (code_name, details) in enumerate(code_items):
                with cols5[idx]:
                    if "consensus" in details:
                        st.warning(f"{details['consensus']}")
