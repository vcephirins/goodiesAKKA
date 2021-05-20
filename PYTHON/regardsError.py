#! /usr/bin/env python3
# coding: utf-8
"""
@author: Vincent Cephirins

regardsError classes

"""

import sys
import traceback

__author__="Vincent Cephirins"
__date__="01-MAR-2021"
__version__="1.0"

# Global variables
_debug = False
_OK = 0
_ERROR = 1
_FATAL = 2

__all__ = ["RegardsError", "RegardsNotFound", "RegardsSyntaxError"]

class RegardsError(Exception):
    """Exception raised for errors in Regards.
    """
    def __init__(self, message=None, cause=None):
        if message is None:
            self.message = traceback.format_exc().splitlines()

        self.message = message
        self.cause = cause

    def __str__(self, file=sys.stderr):
        """
        Message to display or None for system message.
        """

        if self.cause is not None:
            print(self.cause, file=file)

        return self.message



class RegardsSyntaxError(RegardsError):
    """Exception raised for syntax error to call service in Regards.
    """
    pass

class RegardsNotFound(RegardsError):
    """Exception raised for not found in Regards.
    """
    pass

