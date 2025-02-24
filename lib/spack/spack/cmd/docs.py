# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import webbrowser

description = "open spack documentation in a web browser"
section = "help"
level = "short"


def docs(parser, args):
    webbrowser.open("https://spack.readthedocs.io")
