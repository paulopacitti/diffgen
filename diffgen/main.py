from typing_extensions import Annotated
import typer
import diffgen.config as config
import diffgen.git as git
from diffgen.llm import LLM
from rich import print

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
typer.core.rich = None
app = typer.Typer(context_settings=CONTEXT_SETTINGS)

config_file = config.load_config()
llm_client = LLM(**config_file)


@app.command()
def commit(
    context: Annotated[
        str,
        typer.Option(
            "--context", "-c", help="Custom context to enhance commit message"
        ),
    ] = "",
    edit: Annotated[
        bool,
        typer.Option("--edit", "-e", help="Open the commit message in the git editor"),
    ] = False,
    repeat: Annotated[
        bool,
        typer.Option(
            "--repeat", "-r", help="Generate multiple commit messages until satisfied"
        ),
    ] = False,
):
    """
    Generate a commit message.

    Message will be generated based on the changes added to the staging area.
    """
    if repeat:
        while True:
            commit_message = llm_client.generate_commit_message(context)
            if commit_message:
                print(commit_message)
                choice = input("\nGenerate a new message? ((y)es/(N)o): ").lower()
                if choice != "y":
                    if edit:
                        git.commit_editor_prefill(commit_message)
                        return
    else:
        commit_message = llm_client.generate_commit_message(context)
        if commit_message:
            if edit:
                git.commit_editor_prefill(commit_message)
            else:
                print(commit_message)


@app.command()
def pr(
    from_branch: Annotated[str, typer.Option()],
    to_branch: Annotated[str, typer.Option()],
):
    """
    Generate a pull request description.
    """
    print(llm_client.generate_pr_description(from_branch, to_branch))
