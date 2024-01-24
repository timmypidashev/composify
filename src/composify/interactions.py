"""
Composify user interactions
"""

from __future__ import unicode_literals
import inquirer
from git import Repo
from blessed import Terminal
from halo import Halo
import hashlib
import uuid
import re
import os
import sys
import yaml

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
    spinner = Halo(text="", color="green", spinner="dots")

    def __init__(self, user_input, defaults, db):
        self.user_input = user_input
        self.defaults = defaults
        self.db = db

    @classmethod
    async def init(cls, instance):
        await cls.log.debug("Initializing project")
        await cls.check_for_git(instance)
        
        # TODO: Integrate project hash with project.yml as a sort of lock!
        if os.path.exists("./project.yml"):
            await cls.log.error("Project already initialized in this repository!")
            sys.exit()
        
        dev_file, prod_file = await cls.check_for_compose()
                                                  
        questions = [
            inquirer.Text("project_name",
                message="Project name",
                default=os.path.basename(os.getcwd()),
                validate = lambda _, x: re.match('^[a-zA-Z0-9_-]+$', x),
            ),
            inquirer.Text("project_description",
                message="Project description",
                validate = lambda _, x: x.strip() != "",
            ),
            inquirer.Text("compose_dev_file",
                message="Current compose dev environment file",
                default=dev_file,
                validate=lambda _, x: re.match('^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*(\.yml|\.yaml)$', x) is not None and x.strip() != "",
            ),
            inquirer.Text("compose_prod_file",
                message="Current compose prod environment file",
                default=prod_file,
                validate=lambda _, x: re.match('^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*(\.yml|\.yaml)$', x) is not None and x.strip() != "",
            ),
        ]

        user_answers = inquirer.prompt(questions, theme=InquirerTheme())

        cls.spinner.start()
        cls.spinner.text = "Initializing project"

        # commit details to db
        await instance.db.execute(
            "INSERT into projects (PROJECT, HASH, DESCRIPTION) VALUES (?, ?, ?)",
            user_answers["project_name"],
            hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:8],
            user_answers["project_description"]
        )
        await instance.db.commit()

        # create project.yml file
        # TODO: Generate a project.toml based on already existing docker compose configs if any.
        with open("./project.yml", "w") as project_file:
            data = {
                "project": {
                    "name": user_answers["project_name"],
                    "version": "0.0.0",
                    "description": user_answers["project_description"],
                    "license": "MIT"
                },
                "containers": {
                    "example": {
                        "version": "0.0.0",
                        "description": "An example container setup"
                    }
                }
            }
            for block_name, block_content in data.items():
                yaml.dump({block_name: block_content}, project_file, default_flow_style=False, sort_keys=False)
                if block_name != list(data.keys())[-1]:
                    project_file.write("\n")

        cls.spinner.text = "Initialized project"
        cls.spinner.succeed()

    @classmethod
    async def build(cls, instance):
        pass

    @classmethod
    async def run(cls, instance):
        pass

    @classmethod
    async def bump(cls, instance):
        pass

    @classmethod 
    async def push(cls, instance):
        pass

    @classmethod
    async def check_for_git(cls, instance):
        """
        Get the directory from which the script was called
        and check to make sure its a git repository.
        """
        # NOTE: The '.dev' directory is created in 'example' by the
        # logger class before interactions is instanced, so as a bonus 
        # there is no reason for the '.dev' dir to be kept in version control.

        current_directory = os.getcwd()

        if not instance.user_input["dev"]:
            if os.path.isdir(os.path.join(current_directory, ".git")):
                await cls.log.debug("Check for git version control passed")

        elif instance.user_input["dev"]:
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
