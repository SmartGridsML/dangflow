import requests
import streamlit as st

# Configuration
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_API_KEY = 'p4TbrXcO3lepjPDgdtN6rbf26NRyd8SN'
governance_url = "http://localhost:7860/api/v1/run/1fe84af5-5548-48c1-9ef5-bbaf2a398794"
financial_url = "http://localhost:7860/api/v1/run/b8d150de-0d1f-44fd-bfd6-088a4a534139"

# Request headers
headers = {
    "Content-Type": "application/json"
}

def analyze_text_with_mistral(text, user_prompt, model="mistral-large-latest"):
    """Analyze text using Mistral API"""
    mistral_headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    system_message = (
        "You are an expert analyst. Analyze the following text according to the user's instructions."
    )
    user_message = f"Text:\n{text}\n\nUser Instructions:\n{user_prompt}\n\nAnalysis:"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    response = requests.post(MISTRAL_API_URL, headers=mistral_headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

def run_audit_flows(user_input):
    """Run both governance and financial audit flows"""
    try:
        # Prepare payloads with user input
        governance_payload = {
            "input_value": user_input,
            "output_type": "chat",
            "input_type": "chat"
        }
        financial_payload = {
            "input_value": user_input,
            "output_type": "chat",
            "input_type": "chat"
        }

        # Call governance audit flow
        governance_response = requests.post(governance_url, json=governance_payload, headers=headers)
        governance_response.raise_for_status()

        # Call financial audit flow
        financial_response = requests.post(financial_url, json=financial_payload, headers=headers)
        financial_response.raise_for_status()

        # Combine responses and summarize with Mistral
        combined_text = governance_response.text + financial_response.text
        summary = analyze_text_with_mistral(combined_text, 'Summarise the findings from both governance and financial audits')
        
        return {
            "governance_result": governance_response.text,
            "financial_result": financial_response.text,
            "summary": summary
        }

    except requests.exceptions.RequestException as e:
        st.error(f"Error making API request: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="Audit Room Agent", layout="wide")
st.title("🤖 Audit Room — Multi-Agent Audit with Mistral & MCP")

st.markdown("""
Enter your report text below, then hit **Audit**  
— the agent will run governance and financial audits and return a combined analysis.
""")

# Input options
text_input = st.text_area("Enter report text here", height=200, 
                         placeholder="Enter company information, reports, or specific audit requests...")

# Custom analysis prompt
analysis_prompt = st.text_input("Custom analysis instructions (optional)", 
                               placeholder="e.g., Focus on ESG compliance issues")

if st.button("▶️ Audit"):
    # Get input text
    prompt_text = text_input

    if not prompt_text.strip():
        st.error("Please enter some text.")
    else:
        with st.spinner("Running audit flows..."):
            # Run the audit flows
            results = run_audit_flows(prompt_text)
            
            if results:
                st.success("✅ Audit complete")
                
                # Display results in tabs
                tab1, tab2, tab3 = st.tabs(["📋 Summary", "🏛️ Governance Audit", "💰 Financial Audit"])
                
                with tab1:
                    st.markdown("### 🎯 Combined Analysis Summary")
                    st.write(results["summary"])
                
                with tab2:
                    st.markdown("### 🏛️ Governance Audit Results")
                    st.write(results["governance_result"])
                
                with tab3:
                    st.markdown("### 💰 Financial Audit Results")
                    st.write(results["financial_result"])
                
                # Optional: Custom analysis if user provided additional prompt
                if analysis_prompt.strip():
                    st.markdown("### 🔍 Custom Analysis")
                    with st.spinner("Running custom analysis..."):
                        custom_analysis = analyze_text_with_mistral(
                            results["summary"], 
                            analysis_prompt
                        )
                        st.write(custom_analysis)