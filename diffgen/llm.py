import git
from config import CONFIG_FILE_PATH
from openai import OpenAI
from rich import print


class LLM:
    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: str = "",
        timeout=None,
        custom_headers=None,
        max_retries=3,
    ):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            default_headers=custom_headers,
            max_retries=max_retries,
        )
        self.model = model

    def call(self, system_prompt="", user_prompt="") -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(
                rf"""[red]LLM call failed with {e.__class__.__name__}: {e}. 
Make sure your config is correctly set up. ({CONFIG_FILE_PATH})[/]"""
            )
            exit(1)

    def generate_commit_message(self) -> str | None:
        diff = git.get_staging_area_diff()
        if not diff:
            print("[yellow]There's nothing in the staging area, no files to commit.[/]")
            exit(1)
        system_prompt = "Based on this git diff, please generate a commit message. I want just the commit message, nothing more."
        user_prompt = diff

        return self.call(system_prompt, user_prompt)

    def generate_pr_description(self, from_branch, to_branch) -> str | None:
        diff = git.get_branches_diff(from_branch, to_branch)
        if not diff:
            print(
                rf"[yellow]No commits between {from_branch} and {to_branch}, can't generate PR description.[/]")
            exit(1)
        system_prompt = "Based on this git diff, please generate a PR description in markdown (no code formatting necessary). The headers should be 'Context', 'Changes' and 'Testing'. I want just the PR description, nothing else."
        user_prompt = diff

        return self.call(system_prompt, user_prompt)
