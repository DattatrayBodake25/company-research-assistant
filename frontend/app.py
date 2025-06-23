import streamlit as st
import requests

st.set_page_config(page_title="Company Research Assistant", layout="wide")

# --- Sidebar Navigation ---
with st.sidebar:
    st.title("📊 Research Assistant")
    st.markdown("Navigate steps:")
    st.markdown("- 🏢 Input Company")
    st.markdown("- ✨ Generate Questions")
    st.markdown("- 🌐 Web Research")
    st.markdown("- 📚 Build FAISS Index")
    st.markdown("- 📝 Generate Report")
    st.markdown("- 💬 Ask Questions")
    st.info("Powered by 🧠 Gemini + 🔎 Multi-Search + 📚 RAG")

# --- Session State Setup ---
if "queries" not in st.session_state:
    st.session_state.queries = []
if "filepath" not in st.session_state:
    st.session_state.filepath = None
if "generated_report" not in st.session_state:
    st.session_state.generated_report = None

st.title("Company Research Assistant")

# --- TABS Layout ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏢 Input Company", 
    "✨ Questions", 
    "🌐 Research", 
    "📚 Build Index", 
    "📝 Report", 
    "💬 Ask Questions"
])

# --- Tab 1: Company Input ---
with tab1:
    st.header("🏢 Step 1: Enter Company Name")
    company = st.text_input("Company Name", placeholder="e.g., Tech Mahindra")
    if company:
        st.success(f"Selected company: **{company}**")

# --- Tab 2: Generate Questions ---
with tab2:
    st.header("✨ Step 2: Generate Research Questions")
    if company and st.button("Generate Questions"):
        with st.spinner("Generating questions using Gemini..."):
            try:
                res = requests.get("http://localhost:8000/generate-queries/", params={"company": company}, timeout=20)
                if res.status_code == 200:
                    st.session_state.queries = res.json()["queries"]
                    st.success("Questions generated!")
                else:
                    st.error("Failed to fetch questions.")
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.queries:
        with st.expander("✏️ Edit Questions"):
            updated = []
            for i, q in enumerate(st.session_state.queries):
                updated.append(st.text_input(f"Q{i+1}", value=q))
            st.session_state.queries = updated

# --- Tab 3: Start Research ---
with tab3:
    st.header("🌐 Step 3: Run Web Research")
    if st.session_state.queries and st.button("Start Research"):
        with st.spinner("Running search engines..."):
            try:
                res = requests.post(
                    "http://localhost:8000/search-all/",
                    json={"company": company, "questions": st.session_state.queries},
                    timeout=600
                )
                if res.status_code == 200 and res.json()["status"] == "success":
                    st.session_state.filepath = res.json()["filepath"]
                    st.success("Research complete!")
                    st.code(f"Data saved at: {res.json()['filepath']}")
                else:
                    st.error(f"{res.json().get('error')}")
            except Exception as e:
                st.error(f"Exception: {e}")

# --- Tab 4: Build FAISS Index ---
with tab4:
    st.header("📚 Step 4: Build RAG Index")
    if st.session_state.filepath and st.button("Build FAISS Index"):
        with st.spinner("Indexing company research data..."):
            try:
                res = requests.post("http://localhost:8000/build-rag/", json={
                    "company": company,
                    "filepath": st.session_state.filepath
                })
                if res.status_code == 200 and res.json().get("status") == "success":
                    st.success("FAISS index created!")
                else:
                    st.error(f"Failed: {res.json().get('error')}")
            except Exception as e:
                st.error(f"Exception: {e}")

# --- Tab 5: Generate Report ---
with tab5:
    st.header("📝 Step 5: Generate Report")
    if st.session_state.filepath and st.button("Generate Final Report"):
        with st.spinner("Compiling contextual report using Gemini..."):
            try:
                res = requests.get("http://localhost:8000/generate-report/", params={"filepath": st.session_state.filepath})
                if res.status_code == 200 and res.json().get("status") == "success":
                    st.session_state.generated_report = res.json()["report"]
                    st.success("Report ready!")
                else:
                    st.error(f"Error: {res.json().get('error')}")
            except Exception as e:
                st.error(f"Exception: {e}")

    if st.session_state.generated_report:
        st.download_button(
            "Download Markdown Report",
            st.session_state.generated_report,
            file_name=f"{company.replace(' ', '_')}_report.md",
            mime="text/markdown"
        )
        with st.expander("View Report"):
            st.markdown(st.session_state.generated_report)

# --- Tab 6: RAG QA ---
with tab6:
    st.header("💬 Step 6: Ask a Question (RAG)")
    st.markdown("Ask a question based on your company's indexed research.")

    user_q = st.text_input("Ask something about the company:", key="rag_input")

    if user_q and st.button("🔍 Ask Gemini with Context"):
        with st.spinner("Retrieving relevant context and generating answer..."):
            try:
                res = requests.post("http://localhost:8000/ask/", json={
                    "company": company,
                    "question": user_q
                })
                if res.status_code == 200 and res.json()["status"] == "success":
                    st.success("Gemini's Answer:")
                    st.markdown(res.json()["answer"])
                else:
                    st.error(f"{res.json().get('error')}")
            except Exception as e:
                st.error(f"Exception: {e}")