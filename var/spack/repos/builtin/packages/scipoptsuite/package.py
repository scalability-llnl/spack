# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class Scipoptsuite(CMakePackage):
    """The SCIP Optimization Suite is a toolbox for generating and
    solving mixed integer nonlinear programs, in particular mixed
    integer linear programs, and constraint integer programs

    Note: A manual download is required for SCIP.  Spack will search
    your current directory for the download file.  Alternatively,
    add this file to a mirror so that Spack can find it.  For
    instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://scipopt.org"
    url = "file://{0}/scipoptsuite-7.0.1.tgz".format(os.getcwd())
    manual_download = True

    version("7.0.1", sha256="971962f2d896b0c8b8fa554c18afd2b5037092685735d9494a05dc16d56ad422")

    depends_on("gmp")
    depends_on("zlib-api")
    depends_on("readline")
    depends_on("ncurses")
