# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGbrd(RPackage):
    """Provides utilities for processing Rd objects and files. Extract argument
    descriptions and other parts of the help pages of functions."""

    homepage = "https://cloud.r-project.org/package=gbRd"
    url      = "https://cloud.r-project.org/src/contrib/gbRd_0.4-11.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gbRd"

    version('0.4-11', sha256='0251f6dd6ca987a74acc4765838b858f1edb08b71dbad9e563669b58783ea91b')
