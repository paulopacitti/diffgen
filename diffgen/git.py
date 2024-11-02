import subprocess

def is_git_repository():
    command = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], stdout=subprocess.PIPE)
    output = command.stdout.decode("utf-8")
    return output.strip() == "true"

def get_staging_area_diff():
    command = subprocess.run(["git", "diff", "--cached"], stdout=subprocess.PIPE)
    output = command.stdout.decode("utf-8")
    if not output:
        return None
    return output

def get_branches_diff(from_branch, to_branch):
    command = subprocess.run(["git", "diff", from_branch, to_branch], stdout=subprocess.PIPE)
    output = command.stdout.decode("utf-8")
    if not output:
        return None
    return output