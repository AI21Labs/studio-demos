import streamlit as st
import re
import pdfplumber
from ai21.errors import UnprocessableEntity
from utils.studio_style import apply_studio_style
from constants import DOC_QA, ai21
import os
from datetime import date

max_chars = 200000
label = 'multi_doc'+str(date.today())


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
    folder_name = "file"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    for segment in segmented_text:
        path = f"./{folder_name}/doc_ca_demo_{file_name}_part_{index}.txt"
        f = open(path, "w")
        f.write(segment)
        index += 1
        f.close()
        paths.append(path)
    
    return paths


def parse_file(uploaded_file):
    file_type = uploaded_file.type
    with st.spinner("File is being processed..."):
        if file_type == "text/plain":
            plaintext = str(uploaded_file.read(), "utf-8", errors='ignore')
            segmented_text = []
            ind = 0
            while ind < (len(plaintext)):
                if (ind + max_chars) > len(plaintext):
                    curr_max_chars = len(plaintext)-ind
                else:
                    curr_max_chars = max_chars

                segmented_text.append(plaintext[ind:ind+curr_max_chars])
                ind += curr_max_chars
        else:
            with pdfplumber.open(uploaded_file) as pdf:
                all_text = [p.extract_text() for p in pdf.pages]

            filtered = [i.strip() for i in all_text]
            filtered = ['\n'.join([i.strip() for i in page.split('\n')[:-1]]).strip() for page in filtered]
            filtered = [re.sub(' +', ' ', i) for i in filtered]
            segmented_text = merge_segments(filtered, max_chars)
        
        files_paths = write_to_library(segmented_text, uploaded_file.name)
        return files_paths
        

def upload_file(files_paths):
    files_ids = []
    for file_path in files_paths:
        try:
            files_ids.append(ai21.Library.Files.upload(file_path=file_path, labels=label).fileId)
            st.session_state['files_ids'] = files_ids
            st.session_state['file_uploaded'] = True
        except UnprocessableEntity:
            # st.write("This file already exists, please rename the file")
            break

    return files_ids


def parse_and_upload_file(uploaded_file):
    files_paths = parse_file(uploaded_file)
    files_ids = upload_file(files_paths)
    return files_ids, files_paths


st.set_page_config(
    page_title="Multi-Document Q&A",
)

if __name__ == '__main__':
    apply_studio_style()
    st.title("Multi-Document Q&A")
    st.markdown("**Upload documents**")
    
    uploaded_files = st.file_uploader("choose .pdf/.txt file ",
                                      accept_multiple_files=True,
                                      type=["pdf", "text", "txt"],
                                      key="a")
    files_ids_list = []
    files_paths_list = []
    for uploaded_file_g in uploaded_files:
        files_id, files_path = parse_and_upload_file(uploaded_file_g)
        files_ids_list.append(files_id)
        files_paths_list.append(files_path)

    if st.button("Remove file"):
        flat_path_list = []
        for files_path in files_paths_list:
            flat_path_list.extend(files_path)
        for file in flat_path_list:
            try:
                os.remove(file)
            except:
                continue

        # flat_id_list = []
        # for file_id in files_ids_g:
        #     flat_id_list.extend(file_id)
        # for file_id in flat_id_list:
            # with st.spinner("Loading..."):
                # try:
                #     ai21.Library.Files.delete(file_id)
                # except:
                #     continue
    #
        st.write("files removed successfully")
        # del st.session_state['file_uploaded']
        # del st.session_state['files_ids']
    #         st.experimental_rerun()
    #     else:
    #         st.write("No files to remove")
            
    st.markdown("**Ask a question about the uploaded document**") 
    question = st.text_input(label="Question:", value=DOC_QA)

    if st.button(label="Answer"):
        with st.spinner("Loading..."):
            if 'files_ids' not in st.session_state:
                st.write("Please upload a document")
            else:
                response = ai21.Library.Answer.execute(question=question, label=label)
                if response['answer'] is None:
                    st.session_state["answer"] = "The answer is not in the documents"
                else:
                    st.session_state["answer"] = response['answer']
            
    if "answer" in st.session_state:
        st.write(st.session_state['answer'])
        del st.session_state['answer']

   
        