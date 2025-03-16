import diffgen.git as git
from diffgen.config import CONFIG_FILE_PATH
import litellm
from litellm import completion
from rich import print

litellm.global_disable_no_log_param = True


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
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.extra_headers = custom_headers
        self.max_retries = max_retries
        self.model = model

    def call(self, system_prompt="", user_prompt="") -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        try:
            response = completion(
                api_key=self.api_key,
                base_url=self.base_url,
                extra_headers=self.extra_headers,
                max_retries=self.max_retries,
                messages=messages,
                model=self.model,
                stream=False,
                timeout=self.timeout,
            )
            return response.choices[0].message.content.strip()
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
        system_prompt = """"
            # Generate Commit Messages in Conventional Commits Format
            
            Create structured, human-readable commit messages following the Conventional Commits specification.

            ## Instructions:

            1. Analyze the provided changes or description of the commit.
            2. Generate a commit message in the following format:

            ```
            <type>(<scope>): <description>

            [optional body]

            [optional footer(s)]
            ```

            3. Ensure the message adheres to these rules:
            - Type: Use one of the predefined types:
              - `feat`: A new feature.
              - `fix`: A bug fix.
              - `docs`: Documentation changes.
              - `style`: Code formatting changes (no functional impact).
              - `refactor`: Code changes that neither fix bugs nor add features.
              - `test`: Adding or updating tests.
              - `chore`: Maintenance tasks (e.g., build process updates).
            - Scope: Specify the area of the codebase affected (optional).
            - Description: Write a concise summary of what was changed (imperative mood, e.g., "Add feature X").
            - Body: Provide additional details about the change (optional).
            - Footer: Include breaking changes or references to issues (optional).
            5. No need to use phrases like "this commit..." or "these changes...". Just cite the changes and implications of them directly.
            4. RETURN THE OUTPUT AND NOTHING MORE.

            ## Example Output:

            ```
            feat(auth): Add user login functionality

            Introduces user login functionality, allowing users to authenticate using their credentials.  
            Includes validation and error handling for failed login attempts.
            BREAKING CHANGE: Updated authentication API
            ```
        """
        user_prompt = diff

        return self.call(system_prompt, user_prompt)

    def generate_pr_description(self, from_branch, to_branch) -> str | None:
        diff = git.get_branches_diff(from_branch, to_branch)
        if not diff:
            print(
                rf"[yellow]No commits between {from_branch} and {to_branch}, can't generate PR description.[/]"
            )
            exit(1)
        system_prompt = """
            Based on this git diff, please generate a PR description in markdown (no code formatting necessary). The headers should be 'Context', 'Changes' and 'Testing'. I want just the PR description, nothing else.
        """
        user_prompt = diff

        return self.call(system_prompt, user_prompt)
