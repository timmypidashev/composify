"""
Composify build system
"""

import os
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
        await cls.log.critical(f"{project}\n{image_name}\n{image_details}")
