# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RktSchemeLib(RacketPackage):
    """Legacy Scheme Library."""

    git = "ssh://git@github.com/racket/scheme-lib.git"

    maintainers("elfprince13")

    version("8.3", commit="a36e729680818712820ee5269f5208c3c0715a6a")  # tag='v8.3'
    depends_on("rkt-base@8.3", type=("build", "run"), when="@8.3")

    racket_name = "scheme-lib"
    subdirectory = None
