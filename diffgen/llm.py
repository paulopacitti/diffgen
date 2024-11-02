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

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
        )
        return response.choices[0].message.content

    def generate_commit_message(self) -> str | None:
        diff = git.get_staging_area_diff()
        if not diff:
            print("There's nothing in the staging, no files to commit")
            return None
        system_prompt = "Based on this git diff, please generate a commit message. I want just the commit message, nothing more."
        user_prompt = diff

        try:
            return self.call(system_prompt, user_prompt)
        except Exception as e:
            print(
                rf"""[red]LLM call failed with {e.__class__.__name__}: {e}. 
Make sure your config is correctly set up. ({CONFIG_FILE_PATH})[/]"""
            )
            exit(1)
