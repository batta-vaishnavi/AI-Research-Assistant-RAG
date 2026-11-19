
import streamlit as st
import sys
from pathlib import Path

# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "src"))

from generate import generate_answer, generate_without_rag
from retrieve import retrieve_documents

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="💜",
    layout="wide"
)


# ==========================================
# 2. LAVENDER & PURPLE THEME
# ==========================================

st.markdown("""
<style>

/* Main background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(
        135deg, #f5f3ff, #ede9fe, #ddd6fe
    ) !important;
}

[data-testid="stMain"] {
    background: transparent !important;
}

/* General text */
.stMarkdown,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #312e81 !important;
    font-size: 16px;
    line-height: 1.8;
}

/* Headings */
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: #5b21b6 !important;
}

/* Bold text */
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] b {
    color: #4c1d95 !important;
}

/* Tables */
[data-testid="stMarkdownContainer"] table,
[data-testid="stMarkdownContainer"] th,
[data-testid="stMarkdownContainer"] td {
    color: #312e81 !important;
    border-color: #c4b5fd !important;
}

/* Code */
[data-testid="stMarkdownContainer"] code {
    color: #6d28d9 !important;
    background-color: #ede9fe !important;
}

/* Header */
[data-testid="stHeader"] {
    background: rgba(245, 243, 255, 0.85);
}

/* Main title */
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #4c1d95;
    padding: 20px 10px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #6d28d9;
    font-size: 18px;
    margin-bottom: 25px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg, #ede9fe, #ddd6fe
    ) !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #4c1d95 !important;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(
        90deg, #7c3aed, #a78bfa
    ) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 20px !important;
    font-weight: bold !important;
    width: 100%;
}

div.stButton > button:hover {
    background: linear-gradient(
        90deg, #6d28d9, #8b5cf6
    ) !important;
}

/* Input */
[data-testid="stTextInput"] input {
    border: 2px solid #c4b5fd !important;
    border-radius: 10px !important;
    background-color: white !important;
    color: #312e81 !important;
}

/* Expander */
[data-testid="stExpander"] {
    background-color: #f5f3ff !important;
    border: 1px solid #c4b5fd !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span {
    color: #4c1d95 !important;
}

/* Captions */
[data-testid="stCaptionContainer"] {
    color: #5b21b6 !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #6d28d9;
    font-size: 15px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. MAIN HEADER
# ==========================================

st.markdown(
    '<div class="main-title">💜 AI Research Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Explore AI and Machine Learning research '
    'with Retrieval-Augmented Generation'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:

    st.markdown(
        "<h2 style='color:#4c1d95;'>📚 Knowledge Base</h2>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div style="
        background-color:#f5f3ff;
        padding:15px;
        border-radius:12px;
        border:1px solid #c4b5fd;
        color:#4c1d95;
        line-height:2.2;
    ">
        📄 Attention Is All You Need<br>
        📄 BERT<br>
        📄 LoRA
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "📚 Research Assistant",
            "📊 RAG vs Non-RAG"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("""
    <div style="
        background-color:#ddd6fe;
        padding:15px;
        border-radius:12px;
        color:#4c1d95;
        font-size:14px;
        line-height:1.8;
    ">
        <b>⚙️ Powered by:</b><br>
        ChromaDB<br>
        Sentence Transformers<br>
        Gemini
    </div>
    """, unsafe_allow_html=True)

    st.caption("AI Research Assistant | RAG Project")


# ==========================================
# 5. RESEARCH ASSISTANT PAGE
# ==========================================

if page == "📚 Research Assistant":

    st.markdown("## 📚 Research Assistant")

    st.write(
        "Ask questions about the research papers "
        "stored in your knowledge base."
    )

    question = st.text_input(
        "Enter your research question",
        placeholder="Example: How does self-attention work?",
        key="research_question"
    )

    if st.button("✨ Get Research-Based Answer"):

        if question.strip():

            with st.spinner(
                "🔍 Searching research papers and generating answer..."
            ):

                try:

                    answer = generate_answer(question)
                    documents = retrieve_documents(
                        question,
                        top_k=3
                    )

                    st.session_state["research_answer"] = answer
                    st.session_state["research_documents"] = documents

                except Exception as e:

                    st.error(f"Something went wrong: {e}")

        else:

            st.warning("Please enter a research question.")

    # Display answer outside the button block
    if "research_answer" in st.session_state:

        st.divider()

        st.markdown("### 💡 Research-Based Answer")

        st.markdown(
            st.session_state["research_answer"]
        )

        st.divider()

        st.markdown("### 📖 Retrieved Research Sources")

        documents = st.session_state.get(
            "research_documents", []
        )

        if documents:

            for i, doc in enumerate(documents, start=1):

                source = doc.get("source", "Unknown source")
                page_number = doc.get("page", "Unknown")

                with st.expander(
                    f"📄 {i}. {source} — Page {page_number}"
                ):

                    st.markdown(doc.get("text", "No text available."))

        else:

            st.info("No relevant sources were retrieved.")


# ==========================================
# 6. RAG VS NON-RAG COMPARISON PAGE
# ==========================================

elif page == "📊 RAG vs Non-RAG":

    st.markdown("## 📊 RAG vs Non-RAG Comparison")

    st.write(
        "Compare Gemini's general knowledge with answers "
        "generated using your research-paper database."
    )

    question = st.text_input(
        "Enter a question for comparison",
        placeholder="Example: What is the difference between BERT and Transformer?",
        key="comparison_question"
    )

    if st.button("✨ Compare RAG vs Non-RAG"):

        if question.strip():

            non_rag_answer = None
            rag_answer = None
            documents = []

            with st.spinner("🤖 Generating both answers..."):

                try:

                    non_rag_answer = generate_without_rag(question)

                except Exception as e:

                    st.error(f"Without RAG failed: {e}")

                try:

                    documents = retrieve_documents(
                        question,
                        top_k=3
                    )

                    rag_answer = generate_answer(question)

                except Exception as e:

                    st.error(f"With RAG failed: {e}")

            st.session_state["comparison_non_rag"] = non_rag_answer
            st.session_state["comparison_rag"] = rag_answer
            st.session_state["comparison_documents"] = documents

        else:

            st.warning("Please enter a question first.")

    # Display comparison results
    if (
        "comparison_non_rag" in st.session_state
        or "comparison_rag" in st.session_state
    ):

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 🌐 Without RAG")

            st.caption("Gemini general knowledge")

            answer = st.session_state.get(
                "comparison_non_rag"
            )

            if answer:
                st.markdown(answer)
            else:
                st.warning("Answer could not be generated.")

        with col2:

            st.markdown("### 📚 With RAG")

            st.caption("Gemini + Retrieved Research Papers")

            answer = st.session_state.get(
                "comparison_rag"
            )

            if answer:
                st.markdown(answer)
            else:
                st.warning("Answer could not be generated.")

        st.divider()

        st.markdown("### 📖 Retrieved Research Sources")

        documents = st.session_state.get(
            "comparison_documents", []
        )

        if documents:

            for i, doc in enumerate(documents, start=1):

                source = doc.get("source", "Unknown source")
                page_number = doc.get("page", "Unknown")

                with st.expander(
                    f"📄 {i}. {source} — Page {page_number}"
                ):

                    st.markdown(doc.get("text", "No text available."))

        else:

            st.info("No retrieved sources are available.")


# ==========================================
# 7. FOOTER
# ==========================================

st.markdown("---")

st.markdown("""
<div class="footer">
    Made with 💜 using Retrieval-Augmented Generation
    <br>
    Powered by ChromaDB, Sentence Transformers and Gemini
</div>
""", unsafe_allow_html=True)
