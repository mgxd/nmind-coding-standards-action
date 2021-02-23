#!/usr/bin/env python
"""
Inspects a repository for NMinD compatibility. This script can check:
1) Presence of a license
2) Presence of a README
3) GitHub issues enabled / presence of an external issue tracker
4) Coding style (if language was provided)
"""

import click
from pathlib import Path

__version__ = "0.0.1"
CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


def check_license(repo: Path) -> bool:
    import requests


def check_readme(repo: Path) -> bool:
    import requests


def check_issues(repo: str, alt_issues: str = None) -> bool:
    # TODO: Query repo with GH API
    import requests


def check_style(repo: Path, language: str) -> bool:
    linters = {
        "python": f"flake8 {str(repo)}",
    }
    lint_cmd = linters.get(language)
    if lint_cmd is None:
        raise NotImplementedError(
            f"Checking coding style for {language} is not yet supported."
        )

    from shutil import which
    import subprocess as sp

    lint_prog = lint_cmd.split(" ")[0]
    if which(lint_prog) is None:
        raise RuntimeError(f"Linter {lint_prog} was not found on the system.")

    proc = sp.run([lint_cmd], stdout=sp.PIPE, stderr=sp.PIPE)
    return bool(proc.returncode)


# CLI
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, prog_name="nmind-code")
def cli():
    """Command-line interface for NMinD."""
    pass


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument(
    "command",
    type=click.Choice(("license", "readme", "issues", "style"), case_sensitive=False),
)
@click.option("--repo", help="Repository in GitHub notation (owner/repository)")
@click.option("--language", help="Language to check style")
@click.option(
    "--local-path",
    file_ok=False,
    type=click.Path,
    default=Path(),
    show_default=True,
    help="Local path to repository",
)
@click.option(
    "--alt-issues", default=None, help="Alternate site for user questions / bug reports"
)
def check(command, repo, language, local_path, alt_issues):
    if command == "license":
        return check_license(local_path)
    if command == "readme":
        return check_readme(local_path)
    if command == "issues":
        return check_issues(repo, alt_issues)
    if command == "style":
        return check_style(local_path, language)
    raise NotImplementedError(f"Command {command} not available")


if __name__ == "__main__":
    check()
