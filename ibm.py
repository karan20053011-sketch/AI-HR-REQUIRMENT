import streamlit as st
import ollama
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="AI HR Recruitment Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI HR Recruitment Assistant")
st.write("AI-powered Resume Screening & RAG-based Resume Q&A using Qwen3")

st.divider()

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def extract_resume_text(uploaded_file):
    text = ""

    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"
    else:
        text = uploaded_file.read().decode("utf-8")

    return text


def create_chunks(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def retrieve_relevant_chunks(question, chunks, top_k=4):
    if not chunks:
        return ""

    documents = chunks + [question]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(documents)

    question_vector = vectors[-1]
    document_vectors = vectors[:-1]

    similarities = cosine_similarity(
        question_vector,
        document_vectors
    )[0]

    top_indices = similarities.argsort()[-top_k:][::-1]

    relevant_chunks = [
        chunks[index]
        for index in top_indices
    ]

    return "\n\n".join(relevant_chunks)


st.subheader("📄 Upload Candidate Resume")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "txt"]
)

if uploaded_file is not None:
    resume_text = extract_resume_text(uploaded_file)

    if resume_text.strip():
        st.session_state.resume_text = resume_text
        st.session_state.chunks = create_chunks(resume_text)
        st.session_state.chat_history = []

        st.success(
            "✅ Resume uploaded and RAG knowledge base created!"
        )

        with st.expander("👀 View Extracted Resume Text"):
            st.text(resume_text[:5000])
    else:
        st.error("Could not extract text from the resume.")


st.subheader("💼 Job Description")

job_description = st.text_area(
    "Enter the Job Description",
    height=200,
    placeholder="""We are looking for a Python Developer Intern.

Required Skills:
Python, SQL, HTML, CSS, Git and Machine Learning.

Responsibilities:
Develop Python applications, work with databases,
maintain code and collaborate with the development team."""
)

st.divider()

if st.button("🔍 Analyze Candidate", type="primary"):

    if not st.session_state.resume_text:
        st.warning("Please upload a resume first.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        resume_for_analysis = st.session_state.resume_text[:12000]

        prompt = f"""
You are an AI HR Recruitment Assistant.

Analyze the candidate resume against the job description.

Use only information available in the resume.
Do not invent information.

RESUME:
{resume_for_analysis}

JOB DESCRIPTION:
{job_description}

Provide the result in this format:

Candidate Name:

Match Percentage:

Matching Skills:
-

Missing Skills:
-

Candidate Strengths:
-

Candidate Weaknesses:
-

Hiring Recommendation:
-

Interview Questions:
1.
2.
3.
4.
5.

Give a clear and professional recruitment analysis.
"""

        with st.spinner("🤖 Qwen3 is analyzing the candidate..."):

            try:
                response = ollama.chat(
                    model="qwen3:4b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    think=False
                )

                result = response["message"]["content"]

                st.subheader("📊 Recruitment Analysis")
                st.markdown(result)

            except Exception as e:
                st.error(
                    f"❌ Ollama error: {e}"
                )


st.divider()

st.header("💬 Ask Anything About This Resume")

st.write(
    "Ask any question about the uploaded resume. "
    "The RAG system retrieves relevant resume information "
    "and Qwen3 generates the answer."
)

if not st.session_state.resume_text:

    st.info(
        "📄 Please upload a resume to start asking questions."
    )

else:

    question = st.text_input(
        "Ask your question",
        placeholder="Example: What projects has the candidate worked on?"
    )

    if st.button("💬 Ask Qwen"):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            relevant_context = retrieve_relevant_chunks(
                question,
                st.session_state.chunks
            )

            rag_prompt = f"""
You are an AI Resume Assistant.

Answer the user's question using ONLY the provided resume context.

Rules:

1. Use only the information present in the resume context.
2. Do not invent or assume information.
3. Do not use outside knowledge.
4. If the answer is not available in the resume context, say:
"This information is not available in the provided resume."
5. Give a clear and concise answer.

RESUME CONTEXT:
{relevant_context}

USER QUESTION:
{question}
"""

            with st.spinner(
                "🧠 Retrieving resume information and generating answer..."
            ):

                try:

                    response = ollama.chat(
                        model="qwen3:4b",
                        messages=[
                            {
                                "role": "user",
                                "content": rag_prompt
                            }
                        ],
                        think=False
                    )

                    answer = response["message"]["content"]

                    st.subheader("🤖 Qwen3 Answer")
                    st.success(answer)

                    st.session_state.chat_history.append(
                        {
                            "question": question,
                            "answer": answer
                        }
                    )

                except Exception as e:

                    st.error(
                        f"❌ Ollama error: {e}"
                    )


if st.session_state.chat_history:

    st.divider()
    st.subheader("📝 Previous Questions")

    for chat in reversed(st.session_state.chat_history):

        st.markdown(
            f"**👤 Question:** {chat['question']}"
        )

        st.markdown(
            f"**🤖 Answer:** {chat['answer']}"
        )

        st.divider()


st.caption(
    "Powered by Python + Streamlit + Ollama + Qwen3:4B + RAG"
)