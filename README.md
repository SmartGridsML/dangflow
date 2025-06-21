Langflow hack 20/06/2025

The Audit Room

A multi-agent ESG and financial auditing system built for hackathons using Langflow, MCP, and Mistral-AI with a Streamlit UI.

🚀 Overview

The Audit Room ingests corporate sustainability reports and runs three specialized audit flows:

Financial Analyst Agent: Verifies ESG spend against financial data.

Governance Agent: Checks regulatory compliance and disclosure frameworks.

Greenwashing Detector Agent: Scours news and NGO data for contradictions.

After each flow runs, an Executive Summary is optionally generated via the Mistral LLM. A Streamlit app provides a simple UI for uploading reports, viewing individual agent outputs, and reading the summary.

📋 Prerequisites

Python 3.10+

Langflow with your three flows imported:

Financial flow (e.g. Flow ID FIN_FLOW_ID)

Governance flow (Flow ID GOV_FLOW_ID)

Greenwashing flow (Flow ID GREEN_FLOW_ID)

Mistral-AI API key

(Optional) Streamlit Community Cloud account for deployment

📦 Installation

Clone the repo:

git clone https://github.com/your-username/audit-room-streamlit.git
cd audit-room-streamlit

Create a venv & install:

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Set environment variables (locally or in .env):

export LANGFLOW_BASE_URL="http://localhost:7860/api/v1"
export FIN_FLOW_ID="<your-financial-flow-id>"
export GOV_FLOW_ID="<your-governance-flow-id>"
export GREEN_FLOW_ID="<your-greenwashing-flow-id>"
export MISTRAL_API_KEY="<your_mistral_api_key>"

🏃 Running Locally

Start Langflow and ensure your three flows are loaded and accessible on port 7860.

Run the Streamlit app:

streamlit run streamlit_client.py

Open http://localhost:8501 in your browser.

Upload PDF(s) or paste report text, then click Run Audits. Optionally check Summarize to see the Mistral-generated summary.

☁️ Deploying to Streamlit Cloud

Push this repo to GitHub (branch main).

On Streamlit Cloud, create a new app pointing at streamlit_client.py in your repo.

In Secrets, add the same environment variables as above.

Deploy—your app will be live at share.streamlit.io/<username>/audit-room-streamlit.

🔍 Project Structure

├── streamlit_client.py    # Main Streamlit UI
├── client.py              # Example Python client for CLI use
├── requirements.txt       # Python dependencies
├── .streamlit/            # (Optional) local Streamlit config
└── README.md              # This file

🤖 Architecture

Langflow: Orchestrates multi-agent flows via the Run Flow API.

MCP (optional): For a more advanced setup, flows can be exposed as MCP actions and called via mcp-proxy.

Mistral-AI: Generates the Executive Summary from combined outputs.

Streamlit: Provides the browser UI for report upload and result display.
