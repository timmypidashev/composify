"""
Composify user interactions
"""

import inquirer
from blessed import Terminal
import re
import os

from . import log

log = log.Logger("interactions")

term = Terminal()

class InquirerTheme(inquirer.themes.Theme):
    """
    Theming for inquirer cli menu.
    """
    def __init__(self):
        super().__init__()
        self.Question.mark_color = term.yellow
        self.Question.brackets_color = term.bright_green
        self.Question.default_color = term.yellow
        self.List.selection_color = term.bright_green
        self.List.selection_cursor = "❯"
        self.List.unselected_color = term.normal


async def init(user_input, defaults):
    await log.debug("Initializing project")

    questions = [
        inquirer.Text("project_name",
            message="Project name",
            validate = lambda _, x: re.match('^[a-zA-Z0-9_-]+$', x),
        ),
    ]

    user_input = inquirer.prompt(questions, theme=InquirerTheme())
    return user_input
