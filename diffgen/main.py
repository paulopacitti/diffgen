from typing_extensions import Annotated
import typer
import config
from llm import LLM
from rich import print

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
typer.core.rich = None
app = typer.Typer(context_settings=CONTEXT_SETTINGS)


@app.command()
def commit():
    """
    Generate a commit message.

    Message will be generated based on the changes added to the staging area.
    """
    print(llm_client.generate_commit_message())


@app.command()
def pr(from_branch: Annotated[str, typer.Option()], to_branch: Annotated[str, typer.Option()]):
    """
    Generate a pull request description.
    """
    print(llm_client.generate_pr_description(from_branch, to_branch))


if __name__ == "__main__":
    config_file = config.load_config()
    llm_client = LLM(**config_file)
    app(prog_name="diffgen")
