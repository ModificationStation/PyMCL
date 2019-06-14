"""
This script is simply a wrapper.
It overrides global variables and makes it easy for me to keep using my old code until the eventual rewrite.
"""

print("Starting wrapper...")

import sys
import getopt
import config
import os
import utils

helpText = """Usage: pymcl (params)

Accepted params:
    -h: Shows this.
    -p, --parentdir <path>: Use the directory specified.
    -e, --export: Starts PyMCL in export mode."""


def main(argv):
    parentDir = None
    exportMode = False

    try:
        opts, args = getopt.getopt(argv, "hp:e", ["parentdir=", "export"])
    except getopt.GetoptError:
        utils.logger.info(helpText)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            utils.logger.info(helpText)
            sys.exit()
        if opt in ("-p", "--parentdir"):
            utils.logger.info("Setting parent directory to \"" + os.path.abspath(arg) + "\".")
            parentDir = os.path.abspath(arg)
        if opt in ("-e", "--export"):
            utils.logger.info("Starting in export mode.")
            exportMode = True
        else:
            utils.logger.info("Starting in launcher mode.")

    if os.path.exists("stay.here"):
        if config.OS == "Darwin":
            config.MC_DIR = os.getcwd() + "/PyMCL"
        else:
            config.MC_DIR = os.getcwd() + "/.PyMCL"

    if parentDir:
        if not os.path.exists(parentDir):
            if config.OS == "Darwin":
                utils.logger.info("Do you want to create \"" + parentDir + "/PyMCL\"? (y/N)")
            else:
                utils.logger.info("Do you want to create \"" + parentDir + "/.PyMCL\"? (y/N)")
            if not str(input(": ")).lower() in ("y", "yes"):
                exit()
        parentDir = parentDir.strip("/").strip("\\")
        if config.OS == "Darwin":
            config.MC_DIR = parentDir + "/PyMCL"
        else:
            config.MC_DIR = parentDir + "/.PyMCL"

    if exportMode:
        utils.logger.info("Starting exporter...")
        import exportlauncher
    else:
        utils.logger.info("Starting launcher...")
        import mainlauncher


if __name__ == "__main__":
    utils.logger.info("Wrapper started!")

    main(sys.argv[1:])
