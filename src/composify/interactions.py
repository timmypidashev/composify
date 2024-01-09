"""
Composify user interactions
"""

import inquirer
import re
import os

from . import log

log = log.Logger("interactions")

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
