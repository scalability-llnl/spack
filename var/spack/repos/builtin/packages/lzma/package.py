# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lzma(AutotoolsPackage):
    """LZMA Utils are legacy data compression software with high compression
    ratio. LZMA Utils are no longer developed, although critical bugs may be
    fixed as long as fixing them doesn't require huge changes to the code.

    Users of LZMA Utils should move to XZ Utils. XZ Utils support the legacy
    .lzma format used by LZMA Utils, and can also emulate the command line
    tools of LZMA Utils. This should make transition from LZMA Utils to XZ
    Utils relatively easy."""

    homepage = "https://tukaani.org/lzma/"
    url = "https://tukaani.org/lzma/lzma-4.32.7.tar.gz"

    license("LGPL-2.1-or-later")

    version("4.32.7", sha256="9f337a8c51e5ded198d1032f5087ba3fe438f2a54e9df419e513a151775b032c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
