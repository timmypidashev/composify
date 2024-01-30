"""
Composify build system
"""

import os
import pty
import curses
import docker
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
        await cls.log.debug(f"Building {image_name}...")
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
        dockerfile = f"-f {image_data['location']}.{env}"
        build_context = f"{image_data['location']}/."
        environment_flags = None # TODO
        build_command = f"docker buildx build {image} {dockerfile} {build_context} {flags} {environment_flags}"

        client = docker.from_env()
        dind_image = "docker:dind"
        volumes = {f"{image_name}": {"bind": f"/{image_name}", "mode": "rw"}} # this might have unintended edge cases later...

        # Check if the DinD image is already present
        try:
            client.images.get(dind_image)
        
        except docker.errors.ImageNotFound:
            # TODO: Doesnt pull properly, fix client environment
            # Pull the DinD image if not present
            await cls.log.info(f"Pulling Docker-in-Docker image: {dind_image}")
            client.images.pull(dind_image)
            await cls.log.info(f"Image {dind_image} pulled successfully.")

        # Create a Docker container for DinD
        dind_container = client.containers.create(
            dind_image,
            detach=True,
            privileged=True,  # Needed for DinD
            volumes=volumes,
        )

        # Start the DinD container
        dind_container.start()

        # Build execution
        try:
            build_command = ["docker", "buildx", "build", image, dockerfile, build_context, *flags, environment_flags]
            process = client.containers.run(
                dind_image,
                command=build_command,
                detach=True,
                privileged=True,
                volumes={f"{image_name}": {"bind": f"/{image_name}", "mode": "rw"}},
                stdout=True,
                stderr=True,
            )

            # Capture and print the build logs
            for log_line in dind_container.logs(stream=True, follow=True):
                print(log_line.decode().strip())

        finally:
            # Stop and remove the DinD container
            dind_container.stop()
            dind_container.remove()
