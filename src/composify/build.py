"""
Composify build system
"""

import os
import curses
import asyncio
import subprocess
from halo import Halo
from pygments import highlight
from pygments.lexers import DockerLexer
from pygments.formatters import TerminalFormatter

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
    async def build(cls, project, image_name, image_details):
        command = f"docker buildx build -t proxy:dev -f proxy/Dockerfile.dev ./proxy/. --no-cache"
        #result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        #await cls.log.info(result)

        #spinner = Halo(text="Building...", spinner="dots")
        #spinner.start()

        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line-buffered
            universal_newlines=True
        )

        try:
            while process.poll() is None:
                line = process.stdout.readline()

                if line:
                    cls.clear_line()
                    print(line, end='', flush=True)

                    await asyncio.sleep(0.1)

            # Print any remaining output after the process is complete
            remaining_output = process.stdout.read()
            if remaining_output:
                cls.clear_line()
                print(remaining_output, end='', flush=True)

                await asyncio.sleep(0.1)

        finally:
            process.stdout.close()
            process.wait()

    @staticmethod
    def clear_line():
        print("\033[2K\r", end='')



    @staticmethod
    def clear_line():
        print("\033[K", end='')

