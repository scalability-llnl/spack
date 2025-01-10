# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGbrd(RPackage):
    """Utilities for processing Rd objects and files.

    Provides utilities for processing Rd objects and files. Extract argument
    descriptions and other parts of the help pages of functions."""

    cran = "gbRd"

    version("0.4.12", sha256="48cd1d2a845f4b54c307473d2fa07a4ef6a644272f91c6a953844e66cd832338")
    version("0.4-11", sha256="0251f6dd6ca987a74acc4765838b858f1edb08b71dbad9e563669b58783ea91b")
