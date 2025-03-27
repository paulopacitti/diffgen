# diffgen

Universal code changes descrition generation. To be use everywhere, from GitHub repos to Linux Kernel mailing list.

```sh
$ diffgen -h


Usage: diffgen [OPTIONS] COMMAND [ARGS]...

Options:
--install-completion Install completion for the current shell.
--show-completion Show completion for the current shell, to copy it or
customize the installation.
-h, --help Show this message and exit.

Commands:
commit Generate a commit message.
pr Generate a pull request description.

```

## Installation

1. Python 3.10 or later required
2. `pip install git+https://github.com/paulopacitti/diffgen.git`
3. `diffgen init`

A new file `$HOME/.config/diffgen/config.json` will be created. Insert the LLM API key, url... Any [litellm](https://docs.litellm.ai/docs/providers) supported model is accepted.

## Example usage
