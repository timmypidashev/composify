"""
Composify build system
"""

import os
import sys
import pty
import asyncio
import subprocess

from . import log

class Environment:
    log = log.Logger("env")
    
    __slots__ = (
        "AUTHOR",
        "CONTAINER",
        "VERSION",
        "DESCRIPTION",
        "LICENSE",
        "BUILD_DATE",
        "GIT_COMMIT",
        "SOURCE",
        "URL"
    )
    
    def __init__(self):
        pass

    @classmethod
    async def export_arguments(cls, container):
        pass

class Builder:
    log = log.Logger("build")

    def __init__(self):
        pass

    @classmethod
    async def build(cls, project, user_input, image_name, image_data):
        await cls.log.info(f"Building {image_name}...")
        # NOTE: 'image' and 'container' references are used within the same context, 
        # they both mean the same thing to this build system!

        # generate the docker build command
        # NOTE: Using buildkit as a drop in replacement for legacy docker 'build'

        if user_input["dev"]:
            env = "dev"
            flags = ["--no-cache"]
        
        else:
            env = "prod"
            flags = ""

        image = f"-t {image_name}:{env}"
        dockerfile = f"-f {image_data['location'].lstrip('./')}/Dockerfile.{env}"
        build_context = f"{image_data['location']}/."
        environment_flags = None # TODO
        build_command = f"docker buildx build --load {image} {dockerfile} {build_context} {' '.join(flags)}"

        # Extremely simple build process at the moment.
        # TODO: make this build system truly concurrent.
        process = subprocess.Popen(
            build_command,
            shell=True,
            stdout=subprocess.PIPE
        )

        process.wait()

        if process.returncode == 0:
            pass

        else:
            sys.exit()

