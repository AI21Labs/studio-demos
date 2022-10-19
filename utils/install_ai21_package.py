import time
import sys
import os
import subprocess
import streamlit as st

SSH_KEY_FILENAME = "bitbucket_ssh_key"
SECRET_NAME = "BITBUCKET_SSH_KEY"

def _write_ssh_key_to_file():
    with open(SSH_KEY_FILENAME, 'w') as f:
        f.write(st.secrets[SECRET_NAME])
    p = subprocess.Popen([f'chmod 600 {SSH_KEY_FILENAME}'], shell=True)
    out, err = p.communicate()
    if p.returncode != 0:
        print(err)


def _install_ai21_package(repo_ssh_url):
    _write_ssh_key_to_file()
    os.environ["GIT_SSH_COMMAND"] = f"ssh -i {SSH_KEY_FILENAME} -o StrictHostKeyChecking=no"
    start = time.time()
    p = subprocess.Popen([f'{sys.executable} -m pip install {repo_ssh_url}'], shell=True)
    out, err = p.communicate()
    if p.returncode != 0:
        print(err)
    end = time.time()
    print(f"finished installing {repo_ssh_url.split('/')[-1].split('.git')[0]}, took {end-start} secs")


def install_ai21_package_if_needed(package_name, repo_ssh_url):
    try:
        exec(f"import {package_name}")
    except ModuleNotFoundError:
        _install_ai21_package(repo_ssh_url)