# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RktCextLib(RacketPackage):
    """Racket library for running a C compiler/linker."""

    git = "ssh://git@github.com/racket/cext-lib.git"

    maintainers("elfprince13")

    version("8.3", commit="cc22e2456df881a9008240d70dd9012ef37395f5")  # tag = 'v8.3'

    depends_on("rkt-base@8.3", type=("build", "run"), when="@8.3")
    depends_on("rkt-compiler-lib@8.3", type=("build", "run"), when="@8.3")
    depends_on("rkt-dynext-lib@8.3", type=("build", "run"), when="@8.3")
    depends_on("rkt-scheme-lib@8.3", type=("build", "run"), when="@8.3")

    racket_name = "cext-lib"
    subdirectory = racket_name
