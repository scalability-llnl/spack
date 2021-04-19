# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Retry decorators for web requests
"""

import time
import llnl.util.tty as tty


def retry(function):
    """
    Retry decorator with Exponential backoff.
    """
    def retry_function(*args, **kwargs):
        attempts = 4
        delay = 2
        while attempts:
            try:
                return function(*args, **kwargs)
            except Exception as e:
                tty.info("%s, retrying in %s seconds" % (str(e), delay))
                time.sleep(delay)
                attempts -= 1
                delay *= 2
        return function(*args, **kwargs)
    return retry_function
