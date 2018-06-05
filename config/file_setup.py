import subprocess
import os
from typing import *

__compiled = False


def __get_typescript_files() -> List[str]:

    # Get the root directory
    curr_dir = os.path.dirname(os.path.abspath(__file__ + "\\.."))

    # For each typescript file, append to the list of files.
    file_paths = []
    for root, dirs, files in os.walk(curr_dir):
        for file in files:
            if file.endswith(".ts"):
                file_paths.append(os.path.join(root, file))

    # Return the list of files.
    return file_paths


def compile_typescript():

    global __compiled
    if not __compiled:
        print("Compiling Typescript files to Javascript")
        subprocess.call(["tsc"] + __get_typescript_files(), shell=True)
        print("Finished compiling")

        __compiled = True
