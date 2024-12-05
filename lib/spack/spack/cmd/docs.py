# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import webbrowser

description = "open spack documentation in a web browser"
section = "help"
level = "short"


def docs(parser, args):
    webbrowser.open("https://spack.readthedocs.io")
