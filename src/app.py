"""
Copyright (C) 2023 G.I.T.S.3 - All Rights Reserved
You may use, distribute, and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: gits3.1project@gmail.com

"""

from flask import Flask, request, render_template

import gits_createrepo
import gits_delete
import gits_clone
import gits_fork
import gits_checkbranch
import gits_branch
import gits_countcommit
import gits_merge
import gits_diff
import gits_createbranch
import gits_commit
import gits_push
import gits_status
import gits_log

import yaml
import os


# replace this with your token
#global token

app = Flask(__name__, static_url_path='/static')
from flask import session

import secrets

# Generate a random 24-byte (192-bit) secret key
secret_key = secrets.token_hex(24)

app.secret_key = secret_key

@app.route('/')
def index():
    return render_template('GIITS.html')


@app.route('/token_selection', methods=['POST'])
def token_selection():
    token = request.form.get('token')
    session['github_token'] = token  # Store the token in a session variable
    print("Token set in session: " + session['github_token'])
    return f'Selected environment: {token}'


@app.route('/create_repo', methods=['POST'])
def create_github_repo():
    # Get the repo name and token from the form
    repo_name = request.form['repoName']
    token = session.get('github_token')

    if not token:
        return "No GitHub token found. Please select a token first."

    response = gits_createrepo.create_github_repo(token, repo_name)
    print(response)

    if response.status_code == 201:
        return "Repository created successfully!"
    else:
        return f"Error creating repository. Status code: {response.status_code}"

@app.route('/clone_repo', methods=['POST'])
def clone_repository():
    repo_url = request.form['repoURL']
    destination_path = request.form['destinationPath']
    result = gits_clone.clone_repository(repo_url, destination_path)
    if result.returncode == 0:
        return "Repository cloned successfully!"
    else:
        return f"Error cloning repository. Error message: {result.stderr}"


@app.route('/delete_repo', methods=['POST'])
def delete_repository():
    user_name = request.form['userName']
    repo_name = request.form['repoName']
    token = session.get('github_token')

    if not token:
        return "No GitHub token found. Please select a token first."

    print("delete"+token)

    result = gits_delete.delete_github_repo(token, user_name, repo_name)
    if result.status_code == 204:
        return "Repository deleted successfully!"
    else:
        return f"Error deleting repository. Error message: {result.json()}"


@app.route('/fork_repo', methods=['POST'])
def fork_repository():
    user_name = request.form['userName']
    repo_name = request.form['repoName']
    token = session.get('github_token')

    if not token:
        return "No GitHub token found. Please select a token first."
    result = gits_fork.fork_repo(user_name, repo_name, token)
    if result.status_code == 202:
        return "Repository forked successfully!"
    else:
        return f"Error forking repository. Error message: {result.json()}"


@app.route('/check_branch', methods=['POST'])
def check_branch():
    user_name = request.form['userName']
    repo_name = request.form['repoName']
    branch_name = request.form['branchName']
    token = session.get('github_token')

    if not token:
        return "No GitHub token found. Please select a token first."
    result = gits_checkbranch.check_branch_exists(token, user_name, repo_name, branch_name)
    if result.status_code == 200:
        return f"Branch {branch_name} in the {repo_name} exists!"
    else:
        return f"Error!! Error message: {result.json()}"


@app.route('/create_branch', methods=['POST'])
def create_branch():
    user_name = request.form['userName']
    repo_name = request.form['repoName']
    base_branch = request.form['baseBranch']
    new_branch = request.form['newBranch']
    token = session.get('github_token')

    if not token:
        return "No GitHub token found. Please select a token first."
    result = gits_createbranch.create_branch(user_name, repo_name, base_branch, new_branch, token)
    if result.status_code == 422:
        return f"Branch {new_branch} in the repo {repo_name} already exists!"
    elif result.status_code == 201:
        return f"Branch {new_branch} in the repo {repo_name} created successfully!"
    else:
        return f"Error!! Error message: {result.json()}"


@app.route('/get_branches', methods=['POST'])
def get_branches():
    repo_owner = request.form['repoOwner']
    repo_name = request.form['repoName']
    token = session.get('github_token')

    if not token:
        return "No GitHub token found. Please select a token first."
    result = gits_branch.get_github_branches(repo_owner, repo_name, token)
    if result.status_code == 200:
        return [branch['name'] for branch in result.json()]
    else:
        return f"Error: Unable to fetch branches - Status Code {result.status_code}"


@app.route('/commit_count', methods=['POST'])
def get_commit_count():
    repo_url = request.form['repoURL']
    result = gits_countcommit.count_commits_in_github_repo(repo_url)
    return f"The total number of commits in the given repo is {result}"


@app.route('/git_status', methods=['POST'])
def get_git_status_route():
    try:
        repo_path = request.form.get('repoPath', '.')  # Default to the current directory if not provided
        status_info = gits_status.get_git_status()
        return f"Git Status:\n{status_info}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/git_log', methods=['POST'])
def get_git_log_route():
    try:
        repo_path = request.form.get('repoPath', '.')  # Default to the current directory if not provided
        log_info = gits_log.get_git_log()
        return f"Git log:\n{log_info}"
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/merge_branch', methods=['POST'])
def merge_branch():
    repo_owner = request.form['repoOwner']
    repo_name = request.form['repoName']
    branch_name = request.form['branchName']
    token = session.get('github_token')

    if not token:
        return "No GitHub token found. Please select a token first."
    result = gits_merge.merge_github_branch(repo_owner, repo_name, branch_name, token)
    return result


@app.route('/commit_diff', methods=['POST'])
def commit_diff():
    local_path = request.form['localPath']
    branch_name = request.form['branchName']
    filename = request.form['filename']
    commit_msg = request.form['commit_msg']
    result = gits_commit.commit(local_path, branch_name, filename, commit_msg)
    if result.returncode == 0:
        return "Given files committed successfully!"
    else:
        return f"Error commiting files. Error message: {result.stderr}"


@app.route('/push', methods=['POST'])
def push():
    user_name = request.form['userName']
    local_path = request.form['localPath']
    repo_name = request.form['repoName']
    branch_name = request.form['branchName']
    filename = request.form['filename']
    commit_msg = request.form['commit_msg']
    token = session.get('github_token')

    if not token:
        return "No GitHub token found. Please select a token first."
    result = gits_push.push(token,user_name, local_path, repo_name, branch_name, filename, commit_msg)
    if result.returncode == 0:
        return "Code pushed to the repository successfully!"
    else:
        return f"Error pushing code to the repository. Error message: {result.stderr}"


@app.route('/diff', methods=['POST'])
def diff():
    repo_owner = request.form['repoOwner']
    repo_name = request.form['repoName']
    branch_name = request.form['branchName']
    result = gits_diff.get_github_diff(repo_owner, repo_name, branch_name, token)
    return result


if __name__ == '__main__':
    app.run(debug=False, port=80)
    