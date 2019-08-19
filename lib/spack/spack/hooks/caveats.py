# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty


def post_install(spec):
    """Print caveats after the install"""
    c = spec.package.caveats()
    if c:
        tty.warn("Caveats:\n{0}".format(c))
