import logging
import os
import time
from docx import Document
from langchain_huggingface import HuggingFaceEmbeddings
from pypdf import PdfReader
from sklearn.metrics.pairwise import cosine_similarity
from striprtf.striprtf import rtf_to_text
import streamlit as st

logging.getLogger("transformers").setLevel(logging.ERROR)

# It loads the embedidng mdoel into memory exactly once (prevent from being reload)
@st.cache_resource
def load_embedding_model():
    return HuggingFaceEmbeddings(model_name="./saved_embedding_model")

# It stores the results of the embedding calculations
@st.cache_data
def get_resume_embeddings(texts):
    return embedding_model.embed_documents(texts)

# Calls function and stores model object
embedding_model = load_embedding_model()

st.title("Resume Matcher Assistant")

# Create large textbox
job_description = st.text_area("Enter Job Description", height=200)

# Create upload
uploaded_files = st.file_uploader(
    "Upload Resumes (Max 50)", accept_multiple_files=True
)

# Text extraction function
def extract_text(file):
    # Get extension
    ext = os.path.splitext(file.name)[1].lower()
    text = ""

    if ext == ".pdf":
        pdf = PdfReader(file)
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    elif ext == ".docx":
        doc = Document(file)
        text = "\n".join(p.text for p in doc.paragraphs)

    elif ext == ".rtf":
        content = file.read().decode("utf-8", errors="ignore")
        text = rtf_to_text(content)

    elif ext == ".txt":
        text = file.read().decode("utf-8", errors="ignore")

    return text.strip()


def is_valid_resume(text):
    words = text.split()
    # Reject tiny documents
    if len(words) < 30:
        return False

    return True


def get_score(item):
    return item["score"]


if uploaded_files:
    if len(uploaded_files) > 50:
        st.error("Maximum 50 resumes allowed.")
    # Runs matching only when button clicked.
    elif st.button("Match Resumes"):
        # if checkbox empty
        if not job_description.strip():
            st.error("Please enter a job description.")
            # stops execution
            st.stop()
        # valid resumes
        resumes = []

        with st.spinner("Reading resumes..."):
            for file in uploaded_files:
                try:
                    text = extract_text(file)
                    if is_valid_resume(text):
                        resumes.append({"filename": file.name, "text": text})

                except Exception as e:
                    st.error(f"Error in {file.name}: {e}")

        if not resumes:
            st.warning("No valid resume text found.")
            st.stop()

        st.success(f"{len(resumes)} resumes processed.")

        with st.spinner("Calculating scores..."):
            # Start timer.
            start = time.time()
            job_embedding = embedding_model.embed_query(job_description)
            st.write(f"Job embedding time: {time.time() - start:.2f} sec")

            # Only first 3000 characters used.
            resume_texts = [resume["text"] for resume in resumes]

            start = time.time()
            # creates vectors of all resumes
            resume_embeddings = get_resume_embeddings(resume_texts)
            st.write(f"Resume embedding time: {time.time() - start:.2f} sec")

            results = []
            # pair resumes and embeddings
            for resume, resume_embedding in zip(resumes, resume_embeddings):
                # computes similarity
                score = cosine_similarity([job_embedding], [resume_embedding])[0][0]

                results.append(
                    {
                        "filename": resume["filename"],
                        "text": resume["text"],
                        "score": score,
                    }
                )

        # Sort results
        results.sort(key=get_score, reverse=True)

        # Top 10
        top_resumes = results[:10]

        st.subheader("Top 10 Matching Resumes")

        for index, resume in enumerate(top_resumes, start=1):
            st.write(
                f"{index}. {resume['filename']} ",
                # f"({resume['score'] * 100:.2f}% Match)",
            )
