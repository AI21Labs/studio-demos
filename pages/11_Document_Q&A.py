import streamlit as st
import re
import pdfplumber
from utils.studio_style import apply_studio_style
from constants import DOC_QA, ai21

max_chars = 500000

def merge_segments(segments, max_char=2000):
    res = list()
    curr = ''
    for s in segments:
        if len(s) + len(curr) <= max_char:
            curr += '\n' + s
        else:
            res.append(curr.strip())
            curr = s
    if len(curr):
        res.append(curr)
    return res

def write_to_library(segmented_text, file_name):
    index = 0
    paths = []
    for segment in segmented_text:
        path = f"doc_ca_demo{file_name}-{index}.txt"
        f = open(path, "w")
        f.write(segment)
        index += 1
        f.close()
        paths.append(path)
    
    return paths

st.set_page_config(
    page_title="Document Q&A",
)

if __name__ == '__main__':
    apply_studio_style()
    st.title("Document Q&A")
    st.write("Upload a document ")
    uploaded_file = st.file_uploader("choose .pdf/.txt file ", type=["pdf", "text", "txt"])
    files_ids = []

    if uploaded_file and not st.session_state.get('file_uploaded',False):
        file_type = uploaded_file.type
    
        #TODO add support in TXT
        if file_type == "text/plain":
            plaintext = str(uploaded_file.read(), "utf-8")
        else:
            with st.spinner("File is being processed..."):
                with pdfplumber.open(uploaded_file) as pdf:
                    all_text = [p.extract_text() for p in pdf.pages]
    
                filtered = [i.strip() for i in all_text]
                filtered = ['\n'.join([i.strip() for i in page.split('\n')[:-1]]).strip() for page in filtered]
                filtered = [re.sub(' +', ' ', i) for i in filtered]
                segmented_text = merge_segments(filtered, max_chars)
                files_paths    = write_to_library(segmented_text, uploaded_file.name)

                for file_path in files_paths:
                    files_ids.append(ai21.Library.Files.upload(file_path=file_path))
                
                st.session_state['file_ids']      = files_ids    
                st.session_state['file_uploaded'] = True

    st.write("Ask a question on the uploaded document") 
    question = st.text_input(label = "Question:", value = DOC_QA)

    if st.button(label = "Answer"):
        with st.spinner("Loading..."):
            response = ai21.Library.Answer.execute(question=question, fileIds = files_ids)
            st.session_state["answer"] = response['answer']
            
    if "answer" in st.session_state:
        st.write(st.session_state['answer'])

    st.write("Please remove your files before leaving ")
    if st.button("Remove files"):
        with st.spinner("Loading..."):
            for file_id in st.session_state['file_ids']:
                ai21.Library.Files.delete(file_id)
