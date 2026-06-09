# import streamlit as st
# from pypdf import PdfReader

# job_description = st.text_input("PLEASE ENTER YOUR DESCRIPTION")
# uploaded_files = st.file_uploader("Upload Multiple Documents", accept_multiple_files = True)

# if uploaded_files:
#     if len(uploaded_files) <= 50:
#         st.success(f"Successfully uploaded {len(uploaded_files)} file(s).")

#         for uploaded_file in uploaded_files:
            
#             pdf_reader = PdfReader(uploaded_file)
#             text = ""
            
#             for page in pdf_reader.pages:
#                 extracted_page = page.extract_text()
#                 if extracted_page:
#                     text += extracted_page

#             if text.strip():
#                 st.write(text)
#             else:
#                 st.warning("Could not extract text. The PDF might be scanned or empty.")
            
#             st.divider()
#     else:
#         st.error("You can only upload a maximum of 50 files.")























# import streamlit as st
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_core.documents import Document
# from langchain_huggingface import HuggingFaceEmbeddings
# import ollama
# from pypdf import PdfReader
# import logging

# logging.getLogger("transformers").setLevel(logging.ERROR)

# # 1. Cache the embedding model so it only loads once into memory
# @st.cache_resource
# def load_embedding_model():
#     return HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# embedding_function = load_embedding_model()

# st.title("Resume Matcher Assistant")

# job_description = st.text_input("PLEASE ENTER YOUR DESCRIPTION")
# uploaded_files = st.file_uploader("Upload Multiple Documents", accept_multiple_files=True)

# # 2. Prevent automatic ingestion; trigger it only when clicking a button
# if uploaded_files and len(uploaded_files) <= 50:
#     if st.button("Process and Ingest Resumes"):
#         with st.spinner("Processing PDF files..."):
#             all_chunks = []

#             for uploaded_file in uploaded_files:
#                 loader = PdfReader(uploaded_file)
#                 text = ""
#                 for page in loader.pages:
#                     text += page.extract_text() or ""

#                 doc = Document(page_content=text, metadata={"source": uploaded_file.name})
#                 text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#                 chunks = text_splitter.split_documents([doc])
#                 all_chunks.extend(chunks)

#             # 3. Create database in-memory or safely persist without reloading models
#             vector_db = Chroma.from_documents(
#                 all_chunks, 
#                 embedding_function, 
#                 persist_directory="./chroma_db"
#             )
#             st.success(f"Success! Ingested {len(all_chunks)} chunks into './chroma_db'")

# def resume_match_description(user_query: str):
#     # 4. Use the already loaded embedding function instead of creating a new one
#     vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
    
#     results = vector_db.similarity_search(user_query, k=10)
#     context = "\n\n".join([doc.page_content for doc in results])

#     system_prompt = f"""
#     You are a professional hiring assistant. Evaluate the uploaded resumes using ONLY the provided context below.
#     Compare them against the requirements in the job description query.
#     If you do not know the answer based on the context, state clearly that the information is not available.
    
#     CONTEXT:
#     {context}
#     """

#     with st.spinner("Ollama is analyzing..."):
#         response = ollama.chat(
#             model="llama3",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_query} 
#             ]
#         )
#     return response['message']['content']

# # 5. Trigger LLM generation via a dedicated action button
# if job_description:
#     if st.button("Analyze Matches"):
#         analysis_result = resume_match_description(job_description)
#         st.write(analysis_result)

































# import streamlit as st
# # from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_core.documents import Document
# from langchain_huggingface import HuggingFaceEmbeddings
# import ollama
# from pypdf import PdfReader
# import logging
# # Disables warnings from the transformers deep package scanner
# logging.getLogger("transformers").setLevel(logging.ERROR)

# @st.cache_resource
# def load_embedding_model():
#     return HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
# embedding_function = load_embedding_model()

# job_description = st.text_input("PLEASE ENTER YOUR DESCRIPTION")
# uploaded_files = st.file_uploader("Upload Multiple Documents", accept_multiple_files = True)

# if uploaded_files and len(uploaded_files) <= 50:
#     if st.button("Process and Ingest Resumes"):
#         st.success(f"Successfully uploaded {len(uploaded_files)} files.")
#         all_chunks = []

#         for uploaded_file in uploaded_files:
#         #     string_data = uploaded_file.read().decode("utf-8")
#         #     st.text(string_data)

#             loader = PdfReader(uploaded_file)
#             text = ""
#             for page in loader.pages:
#                 text += page.extract_text() or ""

#             doc = Document(page_content=text, metadata={"source": uploaded_file.name})

#             text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#             chunks = text_splitter.split_documents([doc])
#             all_chunks.extend(chunks)
#         vector_db = Chroma.from_documents(all_chunks, embedding_function, persist_directory = "./chroma_db")
#         st.success(f"Success! Ingested {len(all_chunks)} chunks into './chroma_db'")


# def resume_match_description(user_query:str):
#     vector_db = Chroma(persist_directory = "./chroma_db", embedding_function = embedding_function)

#     results = vector_db.similarity_search(user_query, k=50)
#     # context = "\n\n".join([doc.page_content for doc in results])

#     if not results:
#         return "no matching resume found"

#     matched_resumes = {}
#     for doc in results:
#         if len(matched_resumes) >= 10:
#             break
            
#         source_name = doc.metadata.get("source", "Unknown")
#         full_text = doc.metadata.get("full_resume_text", doc.page_content)
#         matched_resumes[source_name] = full_text

#     total_found = len(matched_resumes)
#     st.info(f"Retrieved the top {total_found} unique resumes matching your criteria.")

#     context_blocks = []
#     for filename, text in matched_resumes.items():
#         context_blocks.append(f"--- START OF RESUME: {filename} ---\n{text}\n--- END OF RESUME ---")
    
#     context = "\n\n".join(context_blocks)

#     system_prompt = f"""
#     You are a professional hiring assistant. Evaluate the uploaded resumes using ONLY the provided context below.
#     Compare them against the requirements in the job description query.
#     If you do not know the answer based on the context, state clearly that the information is not available.
    
#     CONTEXT:
#     {context}
#     """

#     response = ollama.chat(
#         model="llama3",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_query} 
#         ]
#     )
#     return response['message']['content']

# if job_description:
#     if st.button("Analyze Matches"):
#         analysis_result = resume_match_description(job_description)
#         st.write(analysis_result)












# ===============================FINAL============================



# import os
# import re
# import logging
# import streamlit as st
# import ollama
# from pypdf import PdfReader
# from docx import Document as DocxDocument
# from striprtf.striprtf import rtf_to_text
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_core.documents import Document
# from langchain_huggingface import HuggingFaceEmbeddings

# logging.getLogger("transformers").setLevel(logging.ERROR)

# # Help avoid reloading the entire model
# @st.cache_resource
# def load_embedding_model():
#     return HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# embedding_function = load_embedding_model()

# st.title("Resume Matcher Assistant")

# job_description = st.text_input("PLEASE ENTER YOUR DESCRIPTION")
# uploaded_files = st.file_uploader("Upload Multiple Documents", accept_multiple_files=True)

# if uploaded_files and len(uploaded_files) <= 50:
#     if st.button("Process and Ingest Resumes"):
#         all_chunks = []
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

#         for uploaded_file in uploaded_files:
#             ext = os.path.splitext(uploaded_file.name)[1].lower()
#             text = ""

#             try:
#                 # PDF
#                 if ext == ".pdf":
#                     pdf = PdfReader(uploaded_file)
#                     for page in pdf.pages:
#                         text += page.extract_text() or ""

#                 # DOCX
#                 elif ext == ".docx":
#                     doc = DocxDocument(uploaded_file)
#                     text = "\n".join(para.text for para in doc.paragraphs)

#                 # RTF
#                 elif ext == ".rtf":
#                     content = uploaded_file.read().decode("utf-8", errors="ignore")
#                     text = rtf_to_text(content)

#                 # TXT
#                 elif ext == ".txt":
#                     text = uploaded_file.read().decode("utf-8", errors="ignore")

#                 else:
#                     st.warning(f"{uploaded_file.name} is not a supported resume format.")
#                     continue

#                 # If text was successfully extracted, split it into chunks and assign metadata
#                 if text.strip():
#                     chunks = text_splitter.split_text(text)
#                     for chunk in chunks:
#                         doc_obj = Document(
#                             page_content=chunk,
#                             metadata={"source": uploaded_file.name}
#                         )
#                         all_chunks.append(doc_obj)

#             except Exception as e:
#                 st.error(f"Error processing {uploaded_file.name}: {e}")

#         if all_chunks:
#             vector_db = Chroma.from_documents(
#                 all_chunks, 
#                 embedding_function, 
#                 persist_directory="./chroma_db"
#             )
#             st.success(f"Success! Ingested {len(all_chunks)} chunks into './chroma_db'")
#         else:
#             st.warning("No text was extracted from the uploaded files.")

# # Match keyword
# def get_matching_resumes(job_description):
#     if not os.path.exists("./chroma_db"):
#         return []

#     vector_db = Chroma(
#         persist_directory="./chroma_db",
#         embedding_function=embedding_function
#     )

#     results = vector_db.similarity_search(
#         job_description,
#         k=100
#     )

#     # Search database for matching words or meaning
#     matching_files = []
#     keywords = job_description.lower().split()

#     for doc in results:
#         text = doc.page_content.lower()

#         for word in keywords:
#             if re.search(r"\b" + re.escape(word) + r"\b", text):
#                 filename = doc.metadata.get("source", "Unknown Source")

#                 if filename not in matching_files:
#                     matching_files.append(filename)
#                 break

#     return matching_files

# if job_description:
#     if st.button("Find Matching Resumes"):
#         matches = get_matching_resumes(job_description)

#         if len(matches) >= 0:
#             st.success(f"Found {len(matches)} matching resumes")
#             for file in matches:
#                 st.write(file)
#         else:
#             st.warning("No matching resumes found")
















# ==============================================================================

# import os
# import re
# import logging
# import streamlit as st
# import ollama
# from pypdf import PdfReader
# from docx import Document as DocxDocument
# from striprtf.striprtf import rtf_to_text
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_chroma import Chroma
# from langchain_core.documents import Document
# from langchain_huggingface import HuggingFaceEmbeddings
# import shutil

# logging.getLogger("transformers").setLevel(logging.ERROR)

# # Help avoid reloading the entire model
# @st.cache_resource
# def load_embedding_model():
#     return HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# embedding_function = load_embedding_model()

# st.title("Resume Matcher Assistant")

# job_description = st.text_input("PLEASE ENTER YOUR DESCRIPTION")
# uploaded_files = st.file_uploader("Upload Multiple Documents", accept_multiple_files=True)

# if uploaded_files and len(uploaded_files) <= 50:
#     if st.button("Process and Ingest Resumes"):
#         all_chunks = []
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

#         for uploaded_file in uploaded_files:
#             ext = os.path.splitext(uploaded_file.name)[1].lower()
#             text = ""

#             try:
#                 # PDF
#                 if ext == ".pdf":
#                     pdf = PdfReader(uploaded_file)
#                     for page in pdf.pages:
#                         text += page.extract_text() or ""

#                 # DOCX
#                 elif ext == ".docx":
#                     doc = DocxDocument(uploaded_file)
#                     text = "\n".join(para.text for para in doc.paragraphs)

#                 # RTF
#                 elif ext == ".rtf":
#                     content = uploaded_file.read().decode("utf-8", errors="ignore")
#                     text = rtf_to_text(content)

#                 # TXT
#                 elif ext == ".txt":
#                     text = uploaded_file.read().decode("utf-8", errors="ignore")

#                 else:
#                     st.warning(f"{uploaded_file.name} is not a supported resume format.")
#                     continue

#                 # If text was successfully extracted, split it into chunks and assign metadata
#                 if text.strip():
#                     chunks = text_splitter.split_text(text)
#                     for chunk in chunks:
#                         doc_obj = Document(
#                             page_content=chunk,
#                             metadata={"source": uploaded_file.name}
#                         )
#                         all_chunks.append(doc_obj)

#             except Exception as e:
#                 st.error(f"Error processing {uploaded_file.name}: {e}")

#         if all_chunks:
#             try:
#                 db = Chroma(
#                     persist_directory = "./chroma_db",
#                     embedding_function = embedding_function
#                 )
#                 db.delete_collection()

#             except Exception:
#                 pass

#             vector_db = Chroma.from_documents(
#                 all_chunks, 
#                 embedding_function, 
#                 persist_directory="./chroma_db"
#             )
#             st.success(f"Success! Ingested {len(all_chunks)} chunks into './chroma_db'")
#         else:
#             st.warning("No text was extracted from the uploaded files.")

# # Match keyword
# def get_matching_resumes(job_description):
#     if not os.path.exists("./chroma_db"):
#         return []

#     vector_db = Chroma(
#         persist_directory="./chroma_db",
#         embedding_function=embedding_function
#     )

#     results = vector_db.similarity_search(
#         job_description,
#         k=100
#     )

#     # Search database for matching words or meaning
#     matching_files = []
#     keywords = job_description.lower().split()

#     for doc in results:
#         text = doc.page_content.lower()

#         for word in keywords:
#             if re.search(r"\b" + re.escape(word) + r"\b", text):
#                 filename = doc.metadata.get("source", "Unknown Source")

#                 if filename not in matching_files:
#                     matching_files.append(filename)
#                 break

#     return matching_files

# if job_description:
#     if st.button("Find Matching Resumes"):
#         matches = get_matching_resumes(job_description)

#         if len(matches) > 0:
#             st.success(f"Found {len(matches)} matching resumes")
#             for file in matches:
#                 st.write(file)
#         else:
#             st.warning("No matching resumes found")
















# import os
# import re
# import logging
# import streamlit as st
# from pypdf import PdfReader
# from langchain_chroma import Chroma
# from docx import Document as DocxDocument
# from striprtf.striprtf import rtf_to_text
# from langchain_core.documents import Document
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# logging.getLogger("transformers").setLevel(logging.ERROR)

# # Cache embedding model to prevent reloading
# @st.cache_resource
# def load_embedding_model():
#     return HuggingFaceEmbeddings(model_name="./saved_embedding_model")

# embedding_function = load_embedding_model()

# st.title("Resume Matcher Assistant")

# # --- UI Inputs ---
# job_description = st.text_area("Enter Job Description for Keyword Matching:")
# uploaded_files = st.file_uploader("Upload Resumes (Max 50)", accept_multiple_files=True)

# # --- Logic: Core Functions ---

# def get_matching_resumes(query_text: str):
#     if not os.path.exists("./chroma_db"):
#         return []
        
#     vector_db = Chroma(
#         persist_directory="./chroma_db", 
#         embedding_function=embedding_function
#     )

#     results = vector_db.similarity_search(query_text, k=5)
#     matching_files = []
#     keywords = query_text.lower().split()

#     for doc in results:
#         text = doc.page_content.lower()
#         for word in keywords:
#             if re.search(r"\b" + re.escape(word) + r"\b", text):
#                 filename = doc.metadata.get("source", "Unknown Source")
#                 if filename not in matching_files:
#                     matching_files.append(filename)
#                 break
#     return matching_files


# def ask_ai_assistant(user_query: str):
#     if not os.path.exists("./chroma_db"):
#         return "Please upload and process resumes first."
        
#     vector_db = Chroma(
#         persist_directory="./chroma_db", 
#         embedding_function=embedding_function
#     )

#     results = vector_db.similarity_search(user_query, k=3)
#     context = "\n\n".join([doc.page_content for doc in results])

#     system_prompt = f"""
#     You are a professional, helpful assistant. Answer the user's question using ONLY the provided context below.
#     If you do not know the answer based on the context, state clearly that the information is not available.
#     Do not use external knowledge or invent facts.
    
#     CONTEXT:
#     {context}
#     """
#     try:
#         response = ollama.chat(
#             model="llama3",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_query} 
#             ]
#         )
#         return response['message']['content']
#     except Exception as e:
#         return f"Ollama Error: {e}"



# # Job Description Matcher
# if job_description:
#     if st.button("Find Matching Resumes"):
#         with st.spinner("Scanning resumes..."):
#             matches = get_matching_resumes(job_description)
#             if len(matches) > 0:
#                 st.success(f"Found {len(matches)} matching resumes based on context and keywords:")
#                 for file in matches:
#                     st.write(file)
#             else:
#                 st.warning("No highly relevant resumes matched those keywords.")

# st.write("---")

# # AI Assistant Q&A
# user_question = st.text_input("Ask a question about the uploaded resumes (e.g., 'Who knows Kubernetes?'):")

# if user_question:
#     if st.button("Ask AI Assistant"):
#         with st.spinner("Analyzing resumes via Llama3..."):
#             answer = ask_ai_assistant(user_question)
#             st.info(answer)

# st.write("---")

# # File Processing & Ingestion
# if uploaded_files:
#     if len(uploaded_files) > 50:
#         st.error("Please upload a maximum of 50 files at once.")

#     elif st.button("Process and Ingest Resumes"):
#         all_chunks = []
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1000,
#             chunk_overlap=200
#         )

#         for uploaded_file in uploaded_files:
#             ext = os.path.splitext(uploaded_file.name)[1].lower()
#             text = ""

#             try:
#                 if ext == ".pdf":
#                     pdf = PdfReader(uploaded_file)
#                     for page in pdf.pages:
#                         text += page.extract_text() or ""

#                 elif ext == ".docx":
#                     doc = DocxDocument(uploaded_file)
#                     text = "\n".join(para.text for para in doc.paragraphs)

#                 elif ext == ".rtf":
#                     content = uploaded_file.read().decode(
#                         "utf-8",
#                         errors="ignore"
#                     )
#                     text = rtf_to_text(content)

#                 elif ext == ".txt":
#                     text = uploaded_file.read().decode(
#                         "utf-8",
#                         errors="ignore"
#                     )

#                 else:
#                     st.warning(
#                         f"{uploaded_file.name} is not a supported format."
#                     )
#                     continue

#                 if text.strip():
#                     chunks = text_splitter.split_text(text)

#                     for chunk in chunks:
#                         doc_obj = Document(
#                             page_content=chunk,
#                             metadata={"source": uploaded_file.name}
#                         )
#                         all_chunks.append(doc_obj)

#             except Exception as e:
#                 st.error(
#                     f"Error processing {uploaded_file.name}: {e}"
#                 )

#         if all_chunks:
#             try:
#                 # Basic cleanup before rewrite
#                 db = Chroma(
#                     persist_directory="./chroma_db",
#                     embedding_function=embedding_function
#                 )
#                 db.delete_collection()

#             except Exception:
#                 pass

#             vector_db = Chroma.from_documents(
#                 documents=all_chunks,
#                 embedding=embedding_function,
#                 persist_directory="./chroma_db"
#             )

#             st.success(
#                 f"Success! Ingested {len(all_chunks)} chunks into Chroma DB."
#             )

#         else:
#             st.warning(
#                 "No text could be extracted from the provided files."
#             )



import os
import re
import streamlit as st
from pypdf import PdfReader
from docx import Document
from striprtf.striprtf import rtf_to_text
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import concurrent.futures
import time
import logging

# Mute all warning logs coming from the transformers library
logging.getLogger("transformers").setLevel(logging.ERROR)


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Resume Matcher", page_icon="📄")
st.title("📄 Resume Matcher — 100% Local")


# ─────────────────────────────────────────────
# LOAD EMBEDDING MODEL (cached so it only loads once)
#
# Change model_name to any sentence-transformers model.
# Fast options:
#   - "all-MiniLM-L6-v2"        (80MB, very fast)
#   - "all-MiniLM-L12-v2"       (120MB, slightly better)
#   - "./saved_embedding_model"  (your local saved model)
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    st.info("Loading embedding model (only once)...")
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

embedding_model = load_model()


# ─────────────────────────────────────────────
# STEP 1: EXTRACT TEXT FROM FILE
# ─────────────────────────────────────────────
def extract_text(file) -> str:
    ext = os.path.splitext(file.name)[1].lower()

    if ext == ".pdf":
        pdf = PdfReader(file)
        return "".join(page.extract_text() or "" for page in pdf.pages)

    if ext == ".docx":
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)

    if ext == ".rtf":
        content = file.read().decode("utf-8", errors="ignore")
        return rtf_to_text(content)

    if ext == ".txt":
        return file.read().decode("utf-8", errors="ignore")

    return ""


# ─────────────────────────────────────────────
# STEP 2: READ ALL FILES IN PARALLEL
#
# Instead of reading one file at a time, we read
# all files at the same time using threads.
# 8 resumes at once → much faster total read time.
# ─────────────────────────────────────────────
def read_all_resumes(uploaded_files) -> list[dict]:
    def read_one(file):
        try:
            text = extract_text(file)
            if text.strip():
                return {"filename": file.name, "text": text}
        except Exception as e:
            st.warning(f"⚠️ Could not read {file.name}: {e}")
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(read_one, uploaded_files))

    return [r for r in results if r is not None]


# ─────────────────────────────────────────────
# STEP 3: EMBED AND SCORE ALL RESUMES
#
# Key fix from your original code:
# - We embed ALL resumes in ONE batch call
#   instead of one by one → much faster
# - We only use first 1000 chars per resume
#   (enough context, keeps embedding fast)
# ─────────────────────────────────────────────
def score_resumes(job_description: str, resumes: list[dict]) -> list[dict]:

    # Embed job description (single query)
    job_embedding = embedding_model.embed_query(job_description)

    # Embed all resumes in ONE batch (fastest way)
    resume_texts = [r["text"][:1000] for r in resumes]
    resume_embeddings = embedding_model.embed_documents(resume_texts)

    # Score each resume against the job description
    for resume, embedding in zip(resumes, resume_embeddings):
        score = cosine_similarity([job_embedding], [embedding])[0][0]
        resume["score"] = float(score)

    # Sort highest score first
    return sorted(resumes, key=lambda x: x["score"], reverse=True)


# ─────────────────────────────────────────────
# STEP 4: EXTRACT KEY INFO FROM RESUME TEXT
#
# Simple rule-based parsing to pull out:
# - Candidate name (first non-empty line)
# - Email address
# - Phone number
# - Skills (looks for a "Skills" section)
# - Years of experience (looks for "X years" pattern)
#
# This replaces the AI analysis step completely.
# No API needed — just text parsing.
# ─────────────────────────────────────────────
def extract_info(text: str) -> dict:
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # Name: assume first non-empty line is the candidate's name
    name = lines[0] if lines else "Not Found"

    # Email: find anything matching email pattern
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    email = email_match.group() if email_match else "Not Found"

    # Phone: find 10+ digit numbers (handles spaces/dashes)
    phone_match = re.search(r"(\+?\d[\d\s\-]{9,15})", text)
    phone = phone_match.group().strip() if phone_match else "Not Found"

    # Years of experience: find "X years" or "X+ years" pattern
    exp_match = re.search(r"(\d+\+?\s+years?)", text, re.IGNORECASE)
    experience = exp_match.group() if exp_match else "Not Found"

    # Skills: find text after a "Skills" heading, grab next 2 lines
    skills = "Not Found"
    for i, line in enumerate(lines):
        if re.search(r"\bskills?\b", line, re.IGNORECASE):
            # Grab up to 2 lines after the "Skills" heading
            skill_lines = lines[i+1 : i+3]
            if skill_lines:
                skills = " | ".join(skill_lines)
            break

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "experience": experience,
        "skills": skills,
    }


# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────
job_description = st.text_area(" Enter Job Description", height=180)

uploaded_files = st.file_uploader(
    " Upload Resumes (Max 50)",
    accept_multiple_files=True,
    type=["pdf", "docx", "rtf", "txt"]
)

if uploaded_files:

    if len(uploaded_files) > 50:
        st.error(" Maximum 50 resumes allowed.")
        st.stop()

    if st.button(" Match Resumes", type="primary"):

        if not job_description.strip():
            st.error(" Please enter a job description.")
            st.stop()

        total_start = time.time()

        # --- Read files in parallel ---
        with st.spinner(f"Reading {len(uploaded_files)} resumes..."):
            t = time.time()
            resumes = read_all_resumes(uploaded_files)
            st.write(f" Read {len(resumes)} resumes in **{time.time() - t:.2f}s**")

        if not resumes:
            st.warning("No valid resume text found.")
            st.stop()

        # --- Score with embeddings ---
        with st.spinner("Scoring resumes with embedding model..."):
            t = time.time()
            scored = score_resumes(job_description, resumes)
            top_10 = scored[:10]
            st.write(f" Scored {len(resumes)} resumes in **{time.time() - t:.2f}s**")

        # --- Show results table ---
        st.subheader(" Top 10 Matching Resumes")

        for i, resume in enumerate(top_10, 1):
            info = extract_info(resume["text"])
            match_pct = resume["score"] * 100

            # Color the score: green > 60%, orange > 40%, red below
            if match_pct >= 60:
                color = ""
            elif match_pct >= 40:
                color = ""
            else:
                color = ""

            with st.expander(
                f"{i}. {info['name']} — {color} {match_pct:.1f}% match  | {resume['filename']}"
            ):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"** Email:** {info['email']}")
                    st.markdown(f"** Phone:** {info['phone']}")
                    st.markdown(f"**Experience:** {info['experience']}")

                with col2:
                    st.markdown(f"** Skills:** {info['skills']}")
                    st.markdown(f"** Match Score:** {match_pct:.2f}%")

                st.markdown("** Resume Preview:**")
                st.text(resume["text"][:500] + "...")

        st.success(f" Total time: **{time.time() - total_start:.1f} seconds**")