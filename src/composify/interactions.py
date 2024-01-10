"""
Composify user interactions
"""

import inquirer
from blessed import Terminal
import re
import os
import sys

from . import log

class InquirerTheme(inquirer.themes.Theme):
    """
    Theming for inquirer cli menu.
    """
    term = Terminal()

    def __init__(self):
        super().__init__()
        self.Question.mark_color = self.term.yellow
        self.Question.brackets_color = self.term.bright_green
        self.Question.default_color = self.term.yellow
        self.List.selection_color = self.term.bright_green
        self.List.selection_cursor = "❯"
        self.List.unselected_color = self.term.normal


class Interaction:
    """
    Command line interface interactions.
    """
    log = log.Logger("interactions")

    def __init__(self):
        pass

    @classmethod
    async def init(cls, user_input, defaults):
        await cls.log.debug("Initializing project")
        await cls.check_for_git()

        questions = [
            inquirer.Text("project_name",
                message="Project name",
                default="test",
                validate = lambda _, x: re.match('^[a-zA-Z0-9_-]+$', x),
            ),
        ]

        user_input = inquirer.prompt(questions, theme=InquirerTheme())
        return user_input

    @classmethod
    async def check_for_git(cls):
        """
        Get the directory from which the script was called
        and check to make sure its a git repository.
        """
        current_directory = os.getcwd()

        if os.path.isdir(os.path.join(current_directory, ".git")):
            await cls.log.debug("Check for git version control passed")

        else:
            await cls.log.error("not a git repo")
