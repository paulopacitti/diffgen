import typer
import config
from llm import LLM
from rich import print

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])
typer.core.rich = None
app = typer.Typer(context_settings=CONTEXT_SETTINGS)


@app.command()
def commit(name: str):
    """
    Generate a commit message.

    Message will be generated based on the changes added to the staging area.
    """
    llm_client.generate_commit_message()
    print(f"Hello {name}")


@app.command()
def pr(name: str, formal: bool = False):
    """
    Generate a pull request description.
    """
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    config_file = config.load_config()
    llm_client = LLM(**config_file)
    app(prog_name="diffgen")
