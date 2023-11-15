import unittest
from unittest.mock import Mock, patch
import subprocess
import json
import requests
from gits_commit import commit
from gits_createrepo import create_github_repo
from gits_branch import get_github_branches
from gits_checkbranch import check_branch_exists
from gits_diff import get_github_diff
from gits_fork import fork_repo
from gits_merge import merge_github_branch
from gits_countcommit import count_commits_in_github_repo
# from read_token import  username
from gits_createbranch import create_branch
from gits_push import push
import app
from flask import Flask, session
from src.app import create_github_repo
import src.app
from src.app import delete_repository
from src.app import clone_repository
from src.app import  fork_repository
from src.app import check_branch
from src.app import create_branch
import os

# github_token = os.environ["GITS_GITHUB_TOKEN"]
# github_username = os.environ["GITS_USERNAME"]
from src.app import token_selection
from src.app import get_branches
github_token = "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"
username = 'GITSSE23'


class Test(unittest.TestCase):

    def testapp_token_selection(self):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        with app.test_request_context('/token_selection', method='POST', data={'token': 'testToken123'}):
            response = token_selection()

            self.assertEqual(session.get('github_token'), 'testToken123')
            self.assertIn('Selected environment: testToken123', response)

    @patch('app.gits_createrepo.create_github_repo')
    def testapp_create_repo(self, mock_create_repo):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        mock_response = Mock()
        mock_response.status_code = 201
        mock_create_repo.return_value = mock_response

        with app.test_request_context('/create_repo', method='POST', data={'repoName': 'test_repo'}):
            session['github_token'] = 'testToken123'  # 设置 session
            response = create_github_repo()
            self.assertEqual(response, "Repository created successfully!")

    @patch('app.gits_createrepo.create_github_repo')
    def testapp_create_repo_failure(self, mock_create_repo):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        mock_response = Mock()
        mock_response.status_code = 400  # Simulate a failure
        mock_create_repo.return_value = mock_response

        with app.test_request_context('/create_repo', method='POST', data={'repoName': 'test_repo'}):
            session['github_token'] = 'testToken123'
            response = create_github_repo()
            self.assertIn("Error creating repository. Status code: 400", response)

    @patch('app.gits_delete.delete_github_repo')
    def testapp_delete_repo_failure(self, mock_delete_repo):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        mock_response = Mock()
        mock_response.status_code = 404  # Simulate a failure (e.g., repo not found)
        mock_response.json.return_value = {"message": "Not Found"}
        mock_delete_repo.return_value = mock_response

        with app.test_request_context('/delete_repo', method='POST', data={'userName': 'test_user', 'repoName': 'nonexistent_repo'}):
            session['github_token'] = 'testToken123'
            response = delete_repository()
            self.assertIn("Error deleting repository. Error message: {'message': 'Not Found'}", response)

    @patch('app.gits_clone.clone_repository')
    def testapp_clone_repo_failure(self, mock_clone_repo):
        app = Flask(__name__)
        mock_result = Mock()
        mock_result.returncode = 1  # Simulate a failure
        mock_result.stderr = "Error cloning repository"
        mock_clone_repo.return_value = mock_result

        with app.test_request_context('/clone_repo', method='POST', data={'repoURL': 'https://nonexistent.com/repo.git', 'destinationPath': '/invalid/path'}):
            response = clone_repository()
            self.assertIn("Error cloning repository. Error message: Error cloning repository", response)




    @patch('app.gits_delete.delete_github_repo')
    def testapp_delete_repo(self, mock_delete_repo):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        mock_response = Mock()
        mock_response.status_code = 204  # 模拟成功的删除操作
        mock_delete_repo.return_value = mock_response

        with app.test_request_context('/delete_repo', method='POST', data={'userName': 'test_user', 'repoName': 'test_repo'}):
            session['github_token'] = 'testToken123'  # 设置 session
            response = delete_repository()
            self.assertEqual(response, "Repository deleted successfully!")

    @patch('app.gits_clone.clone_repository')
    def testapp_clone_repo(self, mock_clone_repo):
        app = Flask(__name__)
        mock_result = Mock()
        mock_result.returncode = 0
        mock_clone_repo.return_value = mock_result

        with app.test_request_context('/clone_repo', method='POST', data={'repoURL': 'https://example.com/repo.git',
                                                                          'destinationPath': '/path/to/dest'}):
            response = clone_repository()
            self.assertEqual(response, "Repository cloned successfully!")

    @patch('app.gits_fork.fork_repo')
    def testapp_fork_repo(self, mock_fork_repo):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        mock_response = Mock()
        mock_response.status_code = 202  # Mocking a successful fork
        mock_fork_repo.return_value = mock_response

        with app.test_request_context('/fork_repo', method='POST',
                                      data={'userName': 'test_user', 'repoName': 'test_repo'}):
            session['github_token'] = 'testToken123'
            response = fork_repository()
            self.assertEqual(response, "Repository forked successfully!")

    @patch('app.gits_checkbranch.check_branch_exists')
    def testapp_check_branch(self, mock_check_branch):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        mock_response = Mock()
        mock_response.status_code = 200  # Mocking branch existence
        mock_check_branch.return_value = mock_response

        with app.test_request_context('/check_branch', method='POST',
                                      data={'userName': 'test_user', 'repoName': 'test_repo',
                                            'branchName': 'test_branch'}):
            session['github_token'] = 'testToken123'
            response = check_branch()
            self.assertIn("Branch test_branch in the test_repo exists!", response)

    @patch('app.gits_createbranch.create_branch')
    def testapp_create_branch(self, mock_create_branch):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        mock_response = Mock()
        mock_response.status_code = 201  # Mocking successful branch creation
        mock_create_branch.return_value = mock_response

        with app.test_request_context('/create_branch', method='POST', data={'userName': 'test_user', 'repoName': 'test_repo', 'baseBranch': 'master', 'newBranch': 'feature'}):
            session['github_token'] = 'testToken123'
            response = create_branch()
            self.assertIn("Branch feature in the repo test_repo created successfully!", response)

    @patch('app.gits_branch.get_github_branches')
    def testapp_get_branches(self, mock_get_branches):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'name': 'main'}, {'name': 'develop'}]
        mock_get_branches.return_value = mock_response

        with app.test_request_context('/get_branches', method='POST',
                                      data={'repoOwner': 'test_owner', 'repoName': 'test_repo'}):
            session['github_token'] = 'testToken123'
            response = get_branches()
            self.assertEqual(response, ['main', 'develop'])

    @patch('app.gits_countcommit.count_commits_in_github_repo')
    def testapp_commit_count(self, mock_count_commits):
        app = Flask(__name__)
        mock_count_commits.return_value = 5

        with app.test_request_context('/commit_count', method='POST', data={'repoURL': 'https://example.com/repo.git'}):
            response = src.app.get_commit_count()
            self.assertIn("The total number of commits in the given repo is 5", response)


    @patch('app.gits_status.get_git_status')
    def testapp_git_status(self, mock_get_status):
        app = Flask(__name__)
        mock_get_status.return_value = "On branch main"

        with app.test_request_context('/git_status', method='POST', data={'repoPath': '/path/to/repo'}):
            response = src.app.get_git_status_route()
            self.assertIn("Git Status:\nOn branch main", response)

    @patch('app.gits_status.get_git_status')
    def testapp_git_status(self, mock_get_status):
        app = Flask(__name__)
        mock_get_status.return_value = "On branch main"

        with app.test_request_context('/git_status', method='POST', data={'repoPath': '/path/to/repo'}):
            response = src.app.get_git_status_route()
            self.assertIn("Git Status:\nOn branch main", response)


    @patch('app.gits_log.get_git_log')
    def testapp_git_log(self, mock_get_log):
        app = Flask(__name__)
        mock_get_log.return_value = "commit abc123"

        with app.test_request_context('/git_log', method='POST', data={'repoPath': '/path/to/repo'}):
            response = src.app.get_git_log_route()
            self.assertIn("Git log:\ncommit abc123", response)

    @patch('app.gits_merge.merge_github_branch')
    def testapp_merge_branch(self, mock_merge_branch):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        mock_merge_branch.return_value = "Merge successful"

        with app.test_request_context('/merge_branch', method='POST', data={'repoOwner': 'test_owner', 'repoName': 'test_repo', 'branchName': 'feature'}):
            session['github_token'] = 'testToken123'
            response = src.app.merge_branch()
            self.assertEqual(response, "Merge successful")

    @patch('app.gits_commit.commit')
    def testapp_commit_diff(self, mock_commit):
        app = Flask(__name__)
        mock_result = Mock()
        mock_result.returncode = 0
        mock_commit.return_value = mock_result

        with app.test_request_context('/commit_diff', method='POST', data={'localPath': '/path/to/repo', 'branchName': 'feature', 'filename': 'file.txt', 'commit_msg': 'Test commit'}):
            response = src.app.commit_diff()
            self.assertEqual(response, "Given files committed successfully!")

    @patch('app.gits_fork.fork_repo')
    def testapp_fork_repo_failure(self, mock_fork_repo):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        mock_response = Mock()
        mock_response.status_code = 404  # Simulating a failure, e.g., repository not found
        mock_fork_repo.return_value = mock_response

        with app.test_request_context('/fork_repo', method='POST',
                                      data={'userName': 'test_user', 'repoName': 'nonexistent_repo'}):
            session['github_token'] = 'testToken123'
            response = fork_repository()
            self.assertIn("Error forking repository. Error message:", response)

    @patch('app.gits_checkbranch.check_branch_exists')
    def testapp_check_branch_failure(self, mock_check_branch):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        mock_response = Mock()
        mock_response.status_code = 404  # Simulating a failure, e.g., branch not found
        mock_check_branch.return_value = mock_response

        with app.test_request_context('/check_branch', method='POST',
                                      data={'userName': 'test_user', 'repoName': 'test_repo',
                                            'branchName': 'nonexistent_branch'}):
            session['github_token'] = 'testToken123'
            response = check_branch()
            self.assertIn("Error!! Error message:", response)

    @patch('app.gits_createbranch.create_branch')
    def testapp_create_branch_failure(self, mock_create_branch):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        mock_response = Mock()
        mock_response.status_code = 409  # Simulating a conflict, e.g., branch already exists
        mock_create_branch.return_value = mock_response

        with app.test_request_context('/create_branch', method='POST',
                                      data={'userName': 'test_user', 'repoName': 'test_repo', 'baseBranch': 'master',
                                            'newBranch': 'existing_branch'}):
            session['github_token'] = 'testToken123'
            response = create_branch()
            self.assertIn("Error!! Error message:", response)

    @patch('app.gits_branch.get_github_branches')
    def testapp_get_branches_failure(self, mock_get_branches):
        app = Flask(__name__)
        app.secret_key = 'test_secret_key'
        mock_response = Mock()
        mock_response.status_code = 404  # Simulating a failure, e.g., repository not found
        mock_get_branches.return_value = mock_response

        with app.test_request_context('/get_branches', method='POST',
                                      data={'repoOwner': 'test_owner', 'repoName': 'nonexistent_repo'}):
            session['github_token'] = 'testToken123'
            response = get_branches()
            self.assertIn("Error: Unable to fetch branches - Status Code 404", response)



    @patch('app.gits_status.get_git_status')
    def testapp_git_status_failure(self, mock_get_status):
        app = Flask(__name__)
        mock_get_status.side_effect = Exception("Error getting status")  # Simulating an exception

        with app.test_request_context('/git_status', method='POST', data={'repoPath': '/nonexistent/path'}):
            response = src.app.get_git_status_route()
            self.assertIn("Error: Error getting status", response)

    @patch('app.gits_log.get_git_log')
    def testapp_git_log_failure(self, mock_get_log):
        app = Flask(__name__)
        mock_get_log.side_effect = Exception("Error getting log")  # Simulating an exception

        with app.test_request_context('/git_log', method='POST', data={'repoPath': '/nonexistent/path'}):
            response = src.app.get_git_log_route()
            self.assertIn("Error: Error getting log", response)



    @patch('app.gits_commit.commit')
    def testapp_commit_diff_failure(self, mock_commit):
        app = Flask(__name__)
        mock_result = Mock()
        mock_result.returncode = 1  # Simulating a failure
        mock_result.stderr = "Error committing files"
        mock_commit.return_value = mock_result

        with app.test_request_context('/commit_diff', method='POST',
                                      data={'localPath': '/nonexistent/path', 'branchName': 'feature',
                                            'filename': 'file.txt', 'commit_msg': 'Test commit'}):
            response = src.app.commit_diff()
            self.assertIn("Error commiting files. Error message: Error committing files", response)

    @patch('requests.get')
    def test_count_commits_good(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"sha": "commit1"}, {"sha": "commit2"}]
        mock_get.return_value = mock_response
        repo_url = "https://github.com/owner/repo"
        commit_count = count_commits_in_github_repo(repo_url)
        self.assertEqual(commit_count, "2")

    @patch('requests.get')
    def test_count_commits_request_bad(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")
        repo_url = "https://github.com/owner/repo"
        commit_count = count_commits_in_github_repo(repo_url)
        self.assertEqual(commit_count, "Error fetching commit count")
    
    @patch('requests.get')
    @patch('requests.post')
    def test_merge_branch_success(self, mock_post, mock_get):
        commit_sha_response = Mock()
        commit_sha_response.status_code = 200
        commit_sha_response.json.return_value = {'object': {'sha': 'commit_sha'}}
        mock_get.return_value = commit_sha_response

        merge_response = Mock()
        merge_response.status_code = 201
        mock_post.return_value = merge_response

        repository_owner = 'owner'
        repository_name = 'repo'
        branch_name = 'test-branch'
        access_token = 'test_access_token'

        result = merge_github_branch(repository_owner, repository_name, branch_name, access_token)

        self.assertEqual(result, "Branch 'test-branch' merged successfully.")

    @patch('requests.get')
    def test_get_commit_sha_failure(self, mock_get):
        commit_sha_response = Mock()
        commit_sha_response.status_code = 404
        commit_sha_response.text = "Commit SHA not found"
        mock_get.return_value = commit_sha_response

        repository_owner = 'owner'
        repository_name = 'repo'
        branch_name = 'test-branch'
        access_token = 'test_access_token'

        result = merge_github_branch(repository_owner, repository_name, branch_name, access_token)
        print(result)
        self.assertEqual(result, "Failed to get the latest commit SHA. Status code: 404\nCommit SHA not found")

    @patch('requests.get')
    @patch('requests.post')
    def test_merge_branch_failure(self, mock_post, mock_get):
        commit_sha_response = Mock()
        commit_sha_response.status_code = 200
        commit_sha_response.json.return_value = {'object': {'sha': 'commit_sha'}}
        mock_get.return_value = commit_sha_response

        merge_response = Mock()
        merge_response.status_code = 400
        merge_response.text = "Merge failed"
        mock_post.return_value = merge_response

        repository_owner = 'owner'
        repository_name = 'repo'
        branch_name = 'test-branch'
        access_token = 'test_access_token'

        result = merge_github_branch(repository_owner, repository_name, branch_name, access_token)

        self.assertEqual(result, "Failed to merge branch 'test-branch'. Status code: 400\nMerge failed")

    @patch('subprocess.run')
    def test_commit_success(self, mock_subprocess_run):
        mock_subprocess_run.return_value.returncode = 0
        mock_subprocess_run.return_value.stdout = b'Commit successful\n'
        
        dir_path = '/path/to/the/repo'
        branch = 'main'
        files = 'file1.txt file2.txt'
        commit_msg = 'Commit message'
        result = commit(dir_path, branch, files, commit_msg)
     
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b'Commit successful\n')
    
        mock_subprocess_run.assert_called_with(['git', 'commit', '-m', commit_msg], cwd=dir_path, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
    @patch('requests.get')
    def test_get_github_branches_success(self, mock_get):
        owner = "test_owner"
        repo = "test_repo"
        github_token = "test_token"

        expected_response_data = [{"name": "branch1"}, {"name": "branch2"}]
        mock_response = Mock()
        mock_response.json.return_value = expected_response_data
        mock_response.status_code = 200

        mock_get.return_value = mock_response
        response = get_github_branches(owner, repo, github_token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response_data)

    @patch('requests.get')
    def test_get_github_branches_exception(self, mock_get):
        owner = "test_owner"
        repo = "test_repo"
        github_token = "test_token"

        mock_get.side_effect = Exception("Simulated Exception")

        response = get_github_branches(owner, repo, github_token)

        self.assertFalse(response)

    @patch('requests.get')
    def test_get_github_diff_success(self, mock_get):
        mock_commit_response = Mock()
        mock_commit_response.status_code = 200
        mock_commit_response.json.return_value = {
            'sha': 'testsha',
        }

        mock_diff_response = Mock()
        mock_diff_response.status_code = 200
        mock_diff_response.json.return_value = {
            'files': ['file1', 'file2'],
        }

        mock_get.side_effect = [mock_commit_response, mock_diff_response]

        owner = 'testowner'
        repo = 'testrepo'
        branch = 'main'
        github_token = 'test_token'

        result = get_github_diff(owner, repo, branch, github_token)

        self.assertEqual(result, ['file1', 'file2'])

    @patch('requests.get')
    def test_get_github_diff_exception(self, mock_get):
        mock_get.side_effect = Exception("Test exception")

        owner = 'testowner'
        repo = 'testrepo'
        branch = 'main'
        github_token = 'test_token'

        result = get_github_diff(owner, repo, branch, github_token)

        self.assertEqual(result, "ERROR: Test exception")

    @patch('requests.get')
    def test_get_github_diff_commit_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        owner = 'testowner'
        repo = 'testrepo'
        branch = 'main'
        github_token = 'test_token'

        result = get_github_diff(owner, repo, branch, github_token)

        self.assertEqual(result, "Error: Unable to fetch the latest commit - Status Code 404")

    @patch('requests.get')
    def test_get_github_diff_differror(self, mock_get):
        mock_commit_response = Mock()
        mock_commit_response.status_code = 200
        mock_commit_response.json.return_value = {
            'sha': 'testsha',
        }
        
        mock_diff_response = Mock()
        mock_diff_response.status_code = 404

        mock_get.side_effect = [mock_commit_response, mock_diff_response]

        owner = 'testowner'
        repo = 'testrepo'
        branch = 'main'
        github_token = 'test_token'

        result = get_github_diff(owner, repo, branch, github_token)

        self.assertEqual(result, "Error: Unable to fetch the difference - Status Code 404")

    @patch('subprocess.run')
    @patch('gits_push.commit')
    def test_push_success(self, mock_commit, mock_subprocess_run):
        PAT = 'tes_pat_token'
        user_name = 'test_username'
        dir_path = '/path/to/the/repo'
        repo_name = 'test_repo'
        branch = 'main'
        files = 'file1.txt file2.txt'
        commit_msg = 'Test commit'

        expected_command = ['git', 'push', f'https://{PAT}@github.com/{user_name}/{repo_name}.git']

        expected_push_response = subprocess.CompletedProcess(
            args=expected_command,
            returncode=0,
            stdout=b'Push successful',
            stderr=b''
        )
        mock_subprocess_run.return_value = expected_push_response
        push_response = push(PAT, user_name, dir_path, repo_name, branch, files, commit_msg)
        self.assertEqual(push_response, expected_push_response)

if __name__ == '__main__':
    unittest.main()
