@st.cache_resource: 
    Tells Streamlit to load this model only once into memory when the server starts. This prevents your app from lagging every time a button is clicked.


In Streamlit, @st.cache_resource is a built-in decorator used to cache expensive, long-lived resources so they only load once.


./saved_embedding_model: 
    Instead of pulling from the internet, it loads the embedding model locally from the folder you created using your save.py script.


Chunking: 
    AI systems struggle to read entire documents at once. This tool splits each resume into overlapping segments of roughly 1000 characters. The 200 character overlap ensures no context is split awkwardly in half between chunks.


Database Reset: 
    Before saving new data, the script attempts to call db.delete_collection() to wipe out old data in ./chroma_db. This keeps your search fresh for only the currently uploaded resumes.


Ingestion: 
    Chroma.from_documents processes all text blocks into mathematical points and commits them to disk.


Semantic Search: 
    vector_db.similarity_search instantly pulls the top 100 closest matching text chunks based on the overall meaning of your job description.


What is :.2f?
    f → floating point number
    .2 → show 2 digits after the decimal point




[Upload Resumes] ──> [Extract Text] ──> [Split Chunks] ──> [Save to Chroma DB]
                                                                   │
[Job Description] ──> [Semantic Search] ──> [Regex Filter] <───────┘
                                                 │
                                       [Display Matching Files]