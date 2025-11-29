import streamlit as st
import pandas as pd
import json
import file_forge as forge

# ------------------------ STYLING ------------------------
st.set_page_config(
    page_title="⚔️ The File Forge 4.0",
    page_icon="⚔️",
    layout="wide",
)

st.markdown("""
<style>
/* Main background */
body {
    background-color: #0E1117;
}

/* Card style */
div[data-testid="stMarkdown"] {
    background-color: #161B22;
    padding: 15px;
    border-radius: 10px;
}

/* Buttons */
button[kind="primary"] {
    background: linear-gradient(90deg, #6C63FF, #5A54D1);
    color: white !important;
    font-weight: 600;
    border-radius: 8px !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------------ SIDEBAR ------------------------
st.sidebar.title("⚔️ The File Forge")
st.sidebar.subheader("Command Center")

page = st.sidebar.radio(
    "Navigate",
    ["🔨 Forge (Create)", "📜 Manage Files", "⚗️ Convert Files"],
)

def list_files():
    return forge.list_all_files()

# ------------------------ PAGE 1: CREATE ------------------------
if page == "🔨 Forge (Create)":
    st.title("🔨 Forge a New File")
    st.write("Craft new text, CSV, or JSON files.")

    col1, col2 = st.columns(2)

    with col1:
        filename = st.text_input("Filename", placeholder="example: heroes")

    with col2:
        ftype = st.selectbox("File Type", ["Text (.txt)", "CSV (.csv)", "JSON (.json)"])

    content = st.text_area("Initial Content", height=200)

    if st.button("🔥 Create File"):
        msg, path = forge.create_file(filename, content, ftype)
        if "Created" in msg:
            st.success(msg)
        else:
            st.error(msg)

# ------------------------ PAGE 2: MANAGE ------------------------
elif page == "📜 Manage Files":
    st.title("📜 Manage Files")

    files = list_files()

    if not files:
        st.warning("No files found. Create a file first.")
    else:
        selected = st.selectbox("Choose a file", files)

        st.subheader("📖 Read File")
        if st.button("Load File"):
            msg, data = forge.read_file(selected)
            st.info(msg)

            if isinstance(data, pd.DataFrame):
                st.dataframe(data)
            elif isinstance(data, dict) or isinstance(data, list):
                st.json(data)
            else:
                st.text_area("File Content", data, height=200)

        st.markdown("---")
        st.subheader("➕ Append to File")

        append_text = st.text_area("Append Content", height=120)
        if st.button("Add Content"):
            msg = forge.append_to_file(selected, append_text)
            if "Appended" in msg:
                st.success(msg)
            else:
                st.error(msg)

        st.markdown("---")
        st.subheader("🗑️ Delete File")

        if st.button("Delete File", type="primary"):
            msg = forge.delete_file(selected)
            if "Deleted" in msg:
                st.success(msg)
            else:
                st.error(msg)

# ------------------------ PAGE 3: CONVERT ------------------------
elif page == "⚗️ Convert Files":
    st.title("⚗️ File Conversion")
    st.write("Convert CSV ↔ JSON effortlessly.")

    files = list_files()

    if not files:
        st.warning("No files to convert.")
    else:
        selected = st.selectbox("Select a CSV or JSON file", files)

        if st.button("⚡ Convert"):
            msg, output_path = forge.convert_csv_json(selected)
            if "Converted" in msg:
                st.success(msg)

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Converted File",
                        data=f,
                        file_name=output_path.split("/")[-1],
                        mime="application/octet-stream"
                    )
            else:
                st.error(msg)
