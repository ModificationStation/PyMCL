"""
This script is simply a wrapper.
It overrides global variables and makes it easy for me to keep using my old code until the eventual rewrite.
"""

import sys
import getopt
import config
import os

helpText = """Usage: pymcl (params)

Accepted params:
    -h: Shows this.
    -d, --dir <path>: Use the directory specified.
    -e, --export: Starts PyMCL in export mode."""


def main(argv):
    parentDir = None
    exportMode = False

    try:
        opts, args = getopt.getopt(argv, "hp:e", ["parentdir=", "export"])
    except getopt.GetoptError:
        print(helpText)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(helpText)
            sys.exit()
        elif opt in ("-p", "--parentdir"):
            parentDir = arg
        elif opt in ("-e", "--export"):
            exportMode = True

    if os.path.exists("stay.here"):
        if config.OS == "Darwin":
            config.MC_DIR = os.getcwd() + "/PyMCL"
        else:
            config.MC_DIR = os.getcwd() + "/.PyMCL"

    if parentDir:
        if not os.path.exists(parentDir):
            if config.OS == "Darwin":
                print("Do you want to create \"" + parentDir + "/.PyMCL\"? (y/N)")
            else:
                print("Do you want to create \"" + parentDir + "/.PyMCL\"? (y/N)")
            if not input(": ").lower() == ("y", "yes"):
                exit()
        if parentDir.endswith("/") or parentDir.endswith("\\"):
            parentDir = parentDir[:1]
        if config.OS == "Darwin":
            config.MC_DIR = parentDir + "/PyMCL"
        else:
            config.MC_DIR = parentDir + "/.PyMCL"

    print(config.MC_DIR)

    if exportMode:
        import exportlauncher
    else:
        import mainlauncher


if __name__ == "__main__":

    main(sys.argv[1:])
