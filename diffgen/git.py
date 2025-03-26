import tempfile
import subprocess


def is_git_repository():
    command = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"], stdout=subprocess.PIPE
    )
    output = command.stdout.decode("utf-8")
    return output.strip() == "true"


def get_staging_area_diff():
    command = subprocess.run(["git", "diff", "--cached"], stdout=subprocess.PIPE)
    output = command.stdout.decode("utf-8")
    if not output:
        return None
    return output


def get_branches_diff(from_branch, to_branch):
    command = subprocess.run(
        ["git", "diff", to_branch, from_branch], stdout=subprocess.PIPE
    )
    output = command.stdout.decode("utf-8")
    if not output:
        return None
    return output


def commit_editor_prefill(message: str):
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
        temp_file.write(message)
        temp_file.flush()
        subprocess.run(["git", "commit", "--edit", "--file", temp_file.name])


def get_current_branch():
    command = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE
    )
    output = command.stdout.decode("utf-8")
    return output.strip()
