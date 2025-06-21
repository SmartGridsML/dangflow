# streamlit_app.py

import os
import streamlit as st
import requests
from io import BytesIO
from PyPDF2 import PdfReader

# ─── CONFIG ────────────────────────────────────────────────────────────────────

# Where your MCP proxy is listening
MCP_PROXY_URL = os.getenv("MCP_PROXY_URL", "http://localhost:5001")

# The action names for each flow, as defined in Langflow's MCP Server tab
FLOW_NAMES = {
    "Financial Audit": os.getenv("FIN_FLOW_NAME", "FINANCIALAGENT"),
"ESG Audit":       os.getenv("ESG_FLOW_NAME", "GOVERNANCE"),
    "Governance Audit":os.getenv("GOV_FLOW_NAME", "GREENNWASHING"),
}

# ─── HELPERS ────────────────────────────────────────────────────────────────────

def extract_text_from_pdf(uploaded_file: BytesIO) -> str:
    """Read all pages from a PDF BytesIO and return the concatenated text."""
    reader = PdfReader(uploaded_file)
    texts = []
    for page in reader.pages:
        txt = page.extract_text()
        if txt:
            texts.append(txt)
    return "\n\n".join(texts)

def call_flow(flow_id: str, text: str) -> str:
    """
    Invoke a Langflow flow (via MCP proxy) and return its 'Chat Output'.
    Assumes each flow has a 'Chat Input' component and returns 'Chat Output'.
    """
    payload = {
        "inputs": [
            {
                "components": ["Chat Input"],
                "input_value": text,
            }
        ],
        "outputs": ["Chat Output"],
        "stream": False,
    }
    url = f"{MCP_PROXY_URL}/actions/{flow_id}"
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    # The exact nesting may vary; adjust if needed
    return data["outputs"]["Chat Output"]

# ─── STREAMLIT UI ──────────────────────────────────────────────────────────────

st.set_page_config(page_title="Audit Room UI", layout="wide")
st.title("📊 The Audit Room: Multi-Agent ESG & Financial Audit")

st.markdown(
    """
    Upload your company sustainability reports below (PDF).  
    Then hit **Run Full Audit** to invoke the Financial, ESG, and Governance agent flows.
    """
)

uploaded_files = st.file_uploader(
    "Upload PDF reports",
    type="pdf",
    accept_multiple_files=True,
    help="You can upload one or more PDF files."
)

if not uploaded_files:
    st.info("Please upload at least one PDF to proceed.")
    st.stop()

if st.button("▶️ Run Full Audit"):
    # 1) Extract text from all PDFs
    with st.spinner("Extracting text from uploaded PDFs…"):
        combined_text = ""
        for pdf in uploaded_files:
            combined_text += extract_text_from_pdf(pdf) + "\n\n---\n\n"

    results = {}
    # 2) Call each flow in turn
    for label, flow_id in FLOW_NAMES.items():
        st.subheader(label)
        try:
            with st.spinner(f"Running {label} flow…"):
                output = call_flow(flow_id, combined_text)
            results[label] = output
            st.text_area(f"{label} Result", output, height=200)
        except Exception as e:
            st.error(f"Error running {label} flow: {e}")

    # 3) Show combined summary
    st.markdown("## 🏁 Combined Audit Summary")
    combined = "\n\n".join(f"### {lbl}\n{txt}" for lbl, txt in results.items())
    st.text_area("Full Audit Report", combined, height=300)
