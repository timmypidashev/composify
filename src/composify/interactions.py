"""
Composify user interactions
"""

import inquirer
from git import Repo
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
        # Question
        self.Question.mark_color = self.term.yellow
        self.Question.brackets_color = self.term.bright_green
        self.Question.default_color = self.term.yellow

        # List
        self.List.selection_color = self.term.bright_green
        self.List.selection_cursor = "❯"
        self.List.unselected_color = self.term.normal

        # Checkbox
        self.Checkbox.selection_color = self.term.cyan
        self.Checkbox.selection_icon = ">"
        self.Checkbox.selected_icon = "[X]"
        self.Checkbox.selected_color = self.term.yellow + self.term.bold
        self.Checkbox.unselected_color = self.term.normal
        self.Checkbox.unselected_icon = "[ ]"
        self.Checkbox.locked_option_color = self.term.gray50


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
        await cls.check_for_git(user_input)
        dev_file, prod_file = await cls.check_for_compose()
                                                  
        questions = [
            inquirer.Text("project_name",
                message="Project name",
                default=os.path.basename(os.getcwd()),
                validate = lambda _, x: re.match('^[a-zA-Z0-9_-]+$', x),
            ),
            inquirer.Text("compose_dev_file",
                message="Current compose dev environment filename",
                default=dev_file,
            ),
        ]

        user_input = inquirer.prompt(questions, theme=InquirerTheme())
        return user_input

    @classmethod
    async def check_for_git(cls, user_input):
        """
        Get the directory from which the script was called
        and check to make sure its a git repository.
        """
        # NOTE: The '.dev' directory is created in 'example' by the
        # logger class before interactions is instanced, so as a bonus 
        # there is no reason for the '.dev' dir to be kept in version control.

        current_directory = os.getcwd()

        if not user_input["dev"]:
            if os.path.isdir(os.path.join(current_directory, ".git")):
                await cls.log.debug("Check for git version control passed")

        elif user_input["dev"]:
            if os.path.exists(".dev"): 
                await cls.log.debug("Check for git version control passed")
        
        else:
            await cls.log.error("Project must be a git repository!")
            sys.exit()

    @classmethod
    async def check_for_compose(cls):
        """
        Returns any .yml or .yaml files with compose in the file descriptor
        and classifying them under dev or prod respectively. Faults to None if 
        nothing is found.
        """
        current_directory = os.getcwd()
        dev_file = None
        prod_file = None

        for filename in os.listdir(current_directory):
            if "compose" in filename.lower() and (filename.endswith((".yml", ".yaml"))):
                base_name = os.path.splitext(filename)[0]

                if any(keyword in base_name.lower() for keyword in ["dev", "development"]) and dev_file is None:
                    dev_file = filename
                elif any(keyword in base_name.lower() for keyword in ["prod", "production"]) and prod_file is None:
                    prod_file = filename

        return dev_file, prod_file
