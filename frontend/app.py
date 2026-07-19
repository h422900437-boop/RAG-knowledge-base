# frontend/app.py
import streamlit as st
import requests
import json

# 1. Page interface configurations
st.set_page_config(page_title="Corporate AI HR Assistant", page_icon="🤖", layout="wide")

BACKEND_URL = "http://127.0.0.1:8000"

st.title("🤖 Corporate AI HR Assistant (RAG System)")
st.caption("Powered by Local Chroma DB and Synced DeepSeek Model")

# ------------------------------------------------------------------
# 📂 Sidebar: Incremental Ingestion Controller with Multimodal Support
# ------------------------------------------------------------------
with st.sidebar:
    st.header("📁 Document Ingestion")
    st.write("Upload company policies in multiple formats (TXT, PDF, Word, Excel).")

    uploaded_file = st.file_uploader(
        "📄 Choose a document",
        type=["txt", "pdf", "docx", "xlsx"],
        help="Supported formats: TXT, PDF, Word (.docx), Excel (.xlsx)"
    )

    if uploaded_file is not None:
        # Display file info
        col1, col2 = st.columns(2)
        with col1:
            st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
        with col2:
            st.metric("File Type", uploaded_file.type or "unknown")

        if st.button("🚀 Confirm Ingestion", use_container_width=True):
            with st.spinner(f"🔄 Processing {uploaded_file.name}..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=120)

                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"🎉 Success! '{uploaded_file.name}' added to database.")

                        # Display detailed information
                        with st.expander("📊 Extraction Details"):
                            st.json({
                                "File Type": result.get("file_type"),
                                "Extracted Characters": result.get("extracted_chars"),
                                "Metadata": result.get("metadata")
                            })
                    else:
                        error_detail = response.json().get('detail', 'Unknown error')
                        st.error(f"❌ Upload failed: {error_detail}")
                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timeout - file too large or backend unresponsive")
                except Exception as e:
                    st.error(f"📡 Connection failed: {e}")

# ------------------------------------------------------------------
# 💬 Main Interface: Chat History Render Loop
# ------------------------------------------------------------------
# Session state initialization to maintain chat logs across page reruns
if "messages" not in st.session_state:
    st.session_state.messages = []

# Re-render previous conversation turns including their saved reference sources
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If the history round contains reference sources, render them underneath
        if "sources" in message and message["sources"]:
            with st.expander("🔍 View Retrieved Sources"):
                for src in message["sources"]:
                    st.caption(f"**Chunk {src['chunk_id']}** | Source: `{src['source']}`")
                    st.text(src["content"])

# Capture new user input from the chat bar
if user_query := st.chat_input("Ask a question about corporate compliance or attendance..."):
    
    # 1. Instantly display user message bubble
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # 2. Connect to HTTP streaming response and update UI turn dynamically
    with st.chat_message("assistant"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={"message": user_query},
                stream=True,
                timeout=300  # Set timeout to 5 minutes for long-running queries
            )

            if response.status_code == 200:
                # Safe closure container to extract hidden metadata during streaming iterations
                stream_context = {"intercepted_sources": []}
                response_text = ""

                def response_generator():
                    # Iterate over stream chunks/lines received from the backend service
                    for chunk in response.iter_lines(decode_unicode=True):
                        if chunk:
                            cleaned_chunk = chunk.strip()
                            # Robust check to intercept RAG reference sources embedded in the text stream
                            if "[SOURCES]:" in cleaned_chunk:
                                source_json = cleaned_chunk.split("[SOURCES]:")[-1].strip()
                                try:
                                    stream_context["intercepted_sources"] = json.loads(source_json)
                                except Exception as parse_error:
                                    st.warning(f"Failed to parse sources: {parse_error}")
                                continue  # Skip rendering this metadata chunk in the main chat UI

                            # Deliver standard text tokens exactly as they are to prevent styling breakage
                            yield cleaned_chunk

                # Trigger smooth streaming effect and capture the final synthesized response text
                ai_answer = st.write_stream(response_generator())

                # Retrieve parsed source objects from the shared tracking block
                intercepted_sources = stream_context["intercepted_sources"]

                # Dynamically append expandable citation layout cards once text loading concludes
                if intercepted_sources:
                    with st.expander("🔍 View Retrieved Sources"):
                        for src in intercepted_sources:
                            st.caption(f"**Chunk {src['chunk_id']}** | Source: `{src['source']}`")
                            st.text(src["content"])

                # Commit the entire context packet entry into the Streamlit session history memory ledger
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_answer,
                    "sources": intercepted_sources
                })
            else:
                st.error(f"❌ Backend service returned error: {response.status_code} - {response.text}")

        except requests.exceptions.Timeout:
            st.error("⏱️ Request timeout - the query took too long. Try a simpler question.")
        except requests.exceptions.ConnectionError:
            st.error(f"📡 Connection failed. Verify FastAPI is running on {BACKEND_URL}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")