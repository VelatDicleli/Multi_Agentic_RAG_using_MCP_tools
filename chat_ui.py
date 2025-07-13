import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="PDF Chat Agent",
    layout="wide",
    page_icon="📄"
)


st.markdown("""
<style>
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .title-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.header("📎 Upload PDF")


    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Select a PDF document to start chatting",
        key="pdf_uploader"
    )

    if uploaded_file is None and st.session_state.get("uploaded_file_exists", False):
    
        with st.spinner("Removing PDF and clearing vector store..."):
            try:
                res = requests.get(f"{API_URL}/delete_store")
                if res.status_code == 200:
                    st.success("🗑️ PDF kaldırıldı ve vector store temizlendi.")
                    st.session_state.chat_history = []
                else:
                    st.error("❌ Vector store temizlenemedi.")
            except Exception as e:
                st.error(f"❌ Temizleme sırasında hata: {e}")
        st.session_state.uploaded_file_exists = False
        st.rerun() 

    
    if uploaded_file is not None:
        st.session_state.uploaded_file_exists = True
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)
        st.info(f"📁 **{uploaded_file.name}**\n📊 Size: {file_size:.2f} MB")

        if st.button("📤 Upload and Process PDF"):
            with st.spinner("Processing PDF..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    res = requests.post(f"{API_URL}/upload_file", files=files)
                    if res.status_code == 200:
                        st.success("✅ PDF uploaded successfully.")
                        st.session_state.chat_history = []
                        st.rerun()
                    else:
                        try:
                            error_msg = res.json().get("error", res.text)
                        except:
                            error_msg = f"HTTP {res.status_code}"
                        st.error(f"❌ Upload failed: {error_msg}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to server. Please check if the API is running.")
                except Exception as e:
                    st.error(f"❌ Upload failed: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)

  
    if st.button("🔄 Reset Session"):
        with st.spinner("Resetting session..."):
            try:
                res = requests.get(f"{API_URL}/reset_chat_history_id")
                if res.status_code == 200:
                    st.session_state.chat_history = []
                    st.success("✅ Session reset successfully.")
                    st.rerun()
                else:
                    st.error("❌ Failed to reset session.")
            except requests.exceptions.RequestException:
                st.error("❌ Cannot connect to server to reset session.")


    # if st.button("🗑️ Delete Vector Store"):
    #     with st.spinner("Deleting vector store..."):
    #         try:
    #             res = requests.get(f"{API_URL}/delete_store")
    #             if res.status_code == 200:
    #                 st.session_state.chat_history = []
    #                 st.success("✅ Vector store deleted and session reset.")
    #                 st.rerun()
    #             else:
    #                 try:
    #                     error_msg = res.json().get("detail", res.text)
    #                 except:
    #                     error_msg = f"HTTP {res.status_code}"
    #                 st.error(f"❌ Failed to delete vector store: {error_msg}")
    #         except requests.exceptions.RequestException:
    #             st.error("❌ Cannot connect to server to delete vector store.")

st.markdown("""
<div class="title-container">
    <h1>📄 Multi-Agentic RAG Chatbot</h1>
    <p>🔍 Ask anything: Analyze your uploaded files, discuss trending topics, or have a friendly conversation.</p>
</div>
""", unsafe_allow_html=True)


for role, msg in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(msg)

user_input = st.chat_input("Ask your PDF...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Waiting for response..."):
        try:
            res = requests.post(f"{API_URL}/ask", json={"query": user_input})
            if res.status_code == 200:
                bot_reply = res.json().get("answer", "No answer found.")
                st.session_state.chat_history.append(("assistant", bot_reply))
            else:
                st.session_state.chat_history.append(("assistant", f"❌ Error: {res.text}"))
        except Exception as e:
            st.session_state.chat_history.append(("assistant", f"❌ Exception: {str(e)}"))

    st.rerun()
