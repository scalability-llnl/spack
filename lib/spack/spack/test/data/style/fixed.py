# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys


def this_is_a_function():
    """This is a docstring."""

    def this_should_be_offset():
        sys.stdout.write(os.name)
