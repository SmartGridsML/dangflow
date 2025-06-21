import requests
import streamlit as st

# Configuration
AUDIT_API_URL = "http://127.0.0.1:7860/api/v1/run/410ad3c7-9ce2-45d5-b359-0b3950d2afba"

# Request headers
headers = {
    "Content-Type": "application/json"
}

def run_audit_flow(user_input):
    """Run the audit flow with the provided input"""
    try:
        # Prepare payload with user input
        payload = {
            "input_value": user_input,
            "output_type": "chat",
            "input_type": "chat"
        }

        # Call audit flow API
        response = requests.post(AUDIT_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        
        return response.text
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error making API request: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="Audit Room Agent", layout="wide")
st.title("🤖 Audit Room — Integrated Audit Agent")

st.markdown("""
Enter your report text below, then hit **Audit**  
— the agent will analyze your input and provide audit results.
""")

# Input options
text_input = st.text_area("Enter report text here", height=200, 
                         placeholder="Enter company information, reports, or specific audit requests...")

if st.button("▶️ Audit"):
    # Get input text
    prompt_text = text_input

    if not prompt_text.strip():
        st.error("Please enter some text.")
    else:
        with st.spinner("Running audit analysis..."):
            # Run the audit flow
            result = run_audit_flow(prompt_text)
            
            if result:
                st.success("✅ Audit complete")
                
                # Display results
                st.markdown("### 📋 Audit Results")
                st.write(result)