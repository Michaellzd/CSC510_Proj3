import subprocess


def get_git_status(repo_path='.'):
    """
    Get the Git status of a local repository.

    repo_path: Path to the Git repository (default is the current directory).
    """
    command = ['git', 'status']
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        return result.stdout.decode().strip()
    else:
        return f"Error getting Git status. Return code: {result.returncode}\n{result.stderr.decode()}"


