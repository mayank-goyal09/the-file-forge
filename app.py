import streamlit as st
import pandas as pd
import json
import file_forge as forge
from io import StringIO, BytesIO

# ------------------------ PAGE CONFIG ------------------------
st.set_page_config(
    page_title="⚔️ The File Forge 4.0",
    page_icon="⚔️",
    layout="wide",
)

# ------------------------ GLOBAL STYLING ------------------------
st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background: radial-gradient(circle at top left, #102316 0, #050908 45%, #020403 100%);
        color: #E5F7E7;
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #07140B 0%, #040806 100%);
        border-right: 1px solid #1C3B22;
    }
    section[data-testid="stSidebar"] * {
        color: #E5F7E7 !important;
    }

    /* Titles */
    h1, h2, h3 {
        color: #D5FFE0 !important;
        text-shadow: 0 0 12px rgba(0, 255, 140, 0.25);
    }

    /* Card-like markdown containers */
    div[data-testid="stMarkdownContainer"] {
        border-radius: 12px;
    }

    /* General card wrapper using blocks */
    .forge-card {
        background: rgba(5, 20, 10, 0.9);
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid rgba(46, 204, 113, 0.25);
        box-shadow:
            0 0 18px rgba(0, 0, 0, 0.9),
            0 0 24px rgba(46, 204, 113, 0.08);
        backdrop-filter: blur(8px);
        transition: transform 0.18s ease-out,
                    box-shadow 0.18s ease-out,
                    border-color 0.18s ease-out;
    }

    .forge-card:hover {
        transform: translateY(-3px);
        box-shadow:
            0 0 22px rgba(0, 0, 0, 1),
            0 0 26px rgba(46, 204, 113, 0.18);
        border-color: rgba(46, 204, 113, 0.5);
    }

    /* Buttons */
    button[kind="primary"],
    .stButton > button {
        background: linear-gradient(90deg, #16A34A, #22C55E);
        color: #F0FFF4 !important;
        font-weight: 600;
        border-radius: 999px !important;
        border: 1px solid #4ADE80;
        box-shadow: 0 0 12px rgba(34, 197, 94, 0.45);
        transition: transform 0.15s ease-out,
                    box-shadow 0.15s ease-out,
                    filter 0.15s ease-out;
    }

    .stButton > button:hover {
        transform: translateY(-1px) scale(1.01);
        filter: brightness(1.05);
        box-shadow: 0 0 18px rgba(34, 197, 94, 0.7);
    }

    .stButton > button:active {
        transform: translateY(0) scale(0.99);
        box-shadow: 0 0 6px rgba(34, 197, 94, 0.45);
    }

    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div {
        background: rgba(2, 10, 5, 0.9);
        color: #E5F7E7 !important;
        border-radius: 10px;
        border: 1px solid #14532D;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus,
    .stSelectbox div[data-baseweb="select"]:focus-within {
        border-color: #22C55E !important;
        box-shadow: 0 0 0 1px #16A34A;
    }

    /* Upload widget */
    .stFileUploader {
        background: rgba(3, 12, 6, 0.9);
        border-radius: 12px;
        padding: 10px 10px 6px 10px;
        border: 1px dashed rgba(34, 197, 94, 0.45);
    }

    /* Subtle fade-in animation for main container */
    .forge-fade-in {
        animation: forgeFade 0.45s ease-out;
    }

    @keyframes forgeFade {
        from {
            opacity: 0;
            transform: translateY(6px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Horizontal rule */
    hr {
        border-color: rgba(21, 128, 61, 0.4);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------ SIDEBAR ------------------------
st.sidebar.title("⚔️ The File Forge")
st.sidebar.caption("Version 4.0 • File handling lab")

page = st.sidebar.radio(
    "Navigate",
    ["🔨 Forge (Create)", "📜 Manage Files", "⚗️ Convert Files"],
)

def list_files():
    return forge.list_all_files()

# ------------------------ PAGE 1: CREATE ------------------------
if page == "🔨 Forge (Create)":
    st.markdown('<div class="forge-card forge-fade-in">', unsafe_allow_html=True)
    st.title("🔨 Forge a New File")
    st.write("Craft fresh **text**, **CSV**, or **JSON** files directly in the forge.")

    col1, col2 = st.columns(2)

    with col1:
        filename = st.text_input("Filename (without extension)", placeholder="example: heroes")

    with col2:
        ftype = st.selectbox("File Type", ["Text (.txt)", "CSV (.csv)", "JSON (.json)"])

    content = st.text_area("Initial Content", height=200, placeholder="Start writing your content here...")

    create_col, _ = st.columns([1, 3])
    with create_col:
        if st.button("🔥 Create File"):
            msg, path = forge.create_file(filename, content, ftype)
            if "Created" in msg:
                st.success(msg)
            else:
                st.error(msg)

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------ PAGE 2: MANAGE ------------------------
elif page == "📜 Manage Files":
    st.markdown('<div class="forge-card forge-fade-in">', unsafe_allow_html=True)
    st.title("📜 Manage Files")

    tab1, tab2 = st.tabs(["📂 Existing Forge Files", "💻 Upload From Device"])

    # ---- Tab 1: Existing files handled by file_forge ----
    with tab1:
        files = list_files()

        if not files:
            st.warning("No files found in the forge directory. Create a file first.")
        else:
            selected = st.selectbox("Choose a file from the forge", files)

            st.subheader("📖 Read File")
            if st.button("Load Forge File"):
                msg, data = forge.read_file(selected)
                st.info(msg)

                if isinstance(data, pd.DataFrame):
                    st.dataframe(data, use_container_width=True)
                elif isinstance(data, (dict, list)):
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

    # ---- Tab 2: Work with uploaded files (read-only / append logical) ----
    with tab2:
        st.subheader("📥 Read a Local File")
        uploaded = st.file_uploader(
            "Upload a text, CSV, or JSON file from your system",
            type=["txt", "csv", "json"],
        )

        if uploaded is not None:
            ext = uploaded.name.split(".")[-1].lower()
            st.caption(f"Detected file: **{uploaded.name}**")

            if ext == "csv":
                try:
                    df = pd.read_csv(uploaded)
                    st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"Could not read CSV: {e}")
            elif ext == "json":
                try:
                    data = json.load(uploaded)
                    st.json(data)
                except Exception as e:
                    st.error(f"Could not read JSON: {e}")
            else:  # txt or others treated as text
                string_data = uploaded.read().decode("utf-8", errors="ignore")
                st.text_area("File Content", string_data, height=220)

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------ PAGE 3: CONVERT ------------------------
elif page == "⚗️ Convert Files":
    st.markdown('<div class="forge-card forge-fade-in">', unsafe_allow_html=True)
    st.title("⚗️ File Conversion")
    st.write("Convert **CSV ↔ JSON** effortlessly, either from forge files or from your own device.")

    tab1, tab2 = st.tabs(["📂 Forge Files", "💻 Upload & Convert"])

    # ---- Tab 1: Convert existing forge files with file_forge ----
    with tab1:
        files = list_files()

        if not files:
            st.warning("No files to convert in the forge.")
        else:
            selected = st.selectbox("Select a CSV or JSON file from forge", files)

            if st.button("⚡ Convert Forge File"):
                msg, output_path = forge.convert_csv_json(selected)
                if "Converted" in msg:
                    st.success(msg)

                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Converted File",
                            data=f,
                            file_name=output_path.split("/")[-1],
                            mime="application/octet-stream",
                        )
                else:
                    st.error(msg)

    # ---- Tab 2: Upload file from device and convert ----
    with tab2:
        st.subheader("💻 Upload CSV or JSON to Convert")
        uploaded_conv = st.file_uploader(
            "Upload a CSV or JSON file",
            type=["csv", "json"],
            key="upload_convert",
        )

        direction = st.radio(
            "Conversion Direction",
            ["CSV → JSON", "JSON → CSV"],
            horizontal=True,
        )

        if uploaded_conv is not None:
            st.caption(f"Working with **{uploaded_conv.name}**")

            if st.button("⚡ Convert Uploaded File"):
                ext = uploaded_conv.name.split(".")[-1].lower()

                # CSV -> JSON
                if direction == "CSV → JSON":
                    try:
                        df = pd.read_csv(uploaded_conv)
                        json_str = df.to_json(orient="records", indent=2)
                        # Provide as downloadable file
                        b = BytesIO()
                        b.write(json_str.encode("utf-8"))
                        b.seek(0)
                        st.download_button(
                            label="⬇️ Download JSON",
                            data=b,
                            file_name=uploaded_conv.name.rsplit(".", 1)[0] + ".json",
                            mime="application/json",
                        )
                        st.success("Conversion successful! JSON ready to download.")
                    except Exception as e:
                        st.error(f"Error converting CSV to JSON: {e}")

                # JSON -> CSV
                else:
                    try:
                        # Load JSON
                        raw = uploaded_conv.read().decode("utf-8", errors="ignore")
                        data = json.loads(raw)
                        df = pd.json_normalize(data)
                        csv_buffer = StringIO()
                        df.to_csv(csv_buffer, index=False)
                        csv_bytes = BytesIO()
                        csv_bytes.write(csv_buffer.getvalue().encode("utf-8"))
                        csv_bytes.seek(0)

                        st.download_button(
                            label="⬇️ Download CSV",
                            data=csv_bytes,
                            file_name=uploaded_conv.name.rsplit(".", 1)[0] + ".csv",
                            mime="text/csv",
                        )
                        st.success("Conversion successful! CSV ready to download.")
                    except Exception as e:
                        st.error(f"Error converting JSON to CSV: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
