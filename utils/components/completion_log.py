import streamlit as st
import pandas as pd
import datetime


def init_log(log_cols):
    if "completion_log" not in st.session_state:
        st.session_state["completion_log"] = CompletionLog(cols=log_cols)


class CompletionLog:

    def __init__(self, cols):
        self.completion_log = pd.DataFrame(columns=cols)

    def get_completions_log(self):
        return self.completion_history

    def add_completion(self, completion_data):
        self.completion_log = pd.concat([self.completion_log, pd.DataFrame(completion_data)], ignore_index=True)

    def add_completion_button(self, completion_data):
        if st.button("Add item to dataset"):
            self.add_completion(completion_data)

    def remove_completion(self, ind):
        self.completion_log.drop(ind, axis=0)

    def download_history(self):
        st.download_button(
            "Download Completion Log",
            self.completion_log.to_csv().encode('utf-8'),
            f"completion_log_{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.csv",
            "text/csv",
            key='download-csv'
        )

    def display(self):
        st.markdown('#')
        st.subheader("Completion Log")
        st.dataframe(self.completion_log)
        self.download_history()
