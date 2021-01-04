#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""utils module ."""

# IMPORT 
import sys
import os
import logging
import subprocess
import traceback

__all__ = ["log_Init",
           "printException",
           "runCommand"]

# Global Variables 
logger = logging.getLogger(__name__)

DEF_INDENT = " " * 16

# Global Functions 

def logInit(level=None):
    """Method to set up logging."""
    if level == 'info':
        logging.basicConfig(level=logging.INFO,
                            format='[%(levelname)-4s] %(message)s')
        logging.root.handlers[0].setLevel(logging.INFO)
    elif level == 'debug':
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)-15s - [%(levelname)-4s] %(message)s')
        logging.root.handlers[0].setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR,
                            format='%(asctime)-15s - [%(levelname)-4s] %(message)s')
        logging.root.handlers[0].setLevel(logging.ERROR)


def printException(message=None, exit=True):
    """
    To handle the printing of the error message when one occurred. Particularly
    useful when catching errors and want to add debug informations on the same
    time.
    """
    # get the traceback
    trace = traceback.format_exc()

    # if not message provided, get the traceback of errors to be a little more
    # useful for the developer
    if message is not None:
        mess = "\n".join([trace, message])
    else:
        # else use message provided by developer
        mess = trace

    # show error in the logger
    logger.error(mess)

    if exit:
        sys.exit(1)

    # return the message
    return mess


def runCommand(cmd, env=None, shell=False):
    """Run a command with subprocess."""
    logger = logging.getLogger(__name__)

    try:
        logger.info(" ".join(cmd))
        res = subprocess.Popen(cmd, env=env, shell=shell,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    except TypeError as e:
        logger.error(e)
    except OSError as e:
        logger.error(e)
    except subprocess.TimeoutExpired as e:
        logger.error("TIME OUT EXPIRED:  %i SEC.", e.timeout)

    return res

# _________________ Main ____________________________
if __name__ == "__main__":
    print("utils module")
