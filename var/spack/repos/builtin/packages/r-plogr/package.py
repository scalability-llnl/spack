# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPlogr(RPackage):
    """The 'plog' C++ Logging Library.

    A simple header-only logging library for C++. Add 'LinkingTo: plogr' to
    'DESCRIPTION', and '#include <plogr.h>' in your C++ modules to use it."""

    cran = "plogr"

    license("MIT")

    version("0.2.0", sha256="0e63ba2e1f624005fe25c67cdd403636a912e063d682eca07f2f1d65e9870d29")
    version("0.1-1", sha256="22755c93c76c26252841f43195df31681ea865e91aa89726010bd1b9288ef48f")
