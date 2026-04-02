import streamlit as st
from app.core.pipeline import process_document, run_pipeline
import tempfile
import os
import warnings
warnings.filterwarnings("ignore")
st.set_page_config(
    page_title="CrossLens",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 CrossLens")
st.caption("Upload a document and verify claims against it — finds evidence on both sides")

with st.sidebar:
    st.header("📁 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "docx"]
    )

    if uploaded_file:
        if st.button("Process Document", type="primary"):
            with st.spinner("Processing document..."):
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=os.path.splitext(uploaded_file.name)[1]
                ) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                chunk_count = process_document(tmp_path)
                os.unlink(tmp_path)
                st.session_state.doc_processed = True
                st.session_state.doc_name = uploaded_file.name
                st.success(f"✅ Processed {chunk_count} chunks")

    if st.session_state.get("doc_processed"):
        st.info(f"📄 Active: {st.session_state.doc_name}")

    st.divider()
    st.markdown("**How it works:**")
    st.markdown("1. Upload any document")
    st.markdown("2. Ask a question or make a claim")
    st.markdown("3. CrossLens finds evidence for AND against")
    st.markdown("4. Get an honest verdict with confidence score")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question or make a claim about your document..."):
    if not st.session_state.get("doc_processed"):
        st.warning("Please upload and process a document first")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                result = run_pipeline(prompt)

            if result["type"] == "SIMPLE":
                st.markdown(result["answer"])
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"]
                })

            else:
                verdict_colors = {
                    "SUPPORTED": "🟢",
                    "CONTRADICTED": "🔴",
                    "AMBIGUOUS": "🟡"
                }
                confidence_colors = {
                    "HIGH": "🔵",
                    "MEDIUM": "🟠",
                    "LOW": "⚪"
                }

                verdict_icon = verdict_colors.get(result["verdict"], "🟡")
                confidence_icon = confidence_colors.get(result["confidence"], "🟠")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "Verdict",
                        f"{verdict_icon} {result['verdict']}"
                    )
                with col2:
                    st.metric(
                        "Confidence",
                        f"{confidence_icon} {result['confidence']}"
                    )

                if result["supporting"]:
                    with st.expander("✅ Supporting Evidence", expanded=True):
                        for point in result["supporting"]:
                            st.markdown(f"• {point}")

                if result["contradicting"]:
                    with st.expander("❌ Contradicting Evidence", expanded=True):
                        for point in result["contradicting"]:
                            st.markdown(f"• {point}")

                with st.expander("📋 Full Analysis"):
                    st.markdown(result["answer"])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"]
                })