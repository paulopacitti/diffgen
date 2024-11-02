import git
from openai import OpenAI


class LLM:
    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: str="",
        timeout=None,
        custom_headers=None,
        max_retries=3,
    ):
        self.client = OpenAI(
            base_url=base_url,
            api_key="",
            timeout=timeout,
            default_headers=custom_headers,
            max_retries=max_retries,
        )
        self.model = model

    def generate_commit_message(self) -> str | None:
        diff = git.get_staging_area_diff()
        if not diff:
            return None
        system_prompt = (
            "Based on this git diff, please generate a pull request description: "
        )
        user_prompt = diff
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
