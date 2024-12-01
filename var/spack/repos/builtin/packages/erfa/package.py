# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Erfa(AutotoolsPackage):
    """ERFA (Essential Routines for Fundamental Astronomy)
    is a C library containing key algorithms for astronomy."""

    homepage = "https://github.com/liberfa/erfa"
    url = "https://github.com/liberfa/erfa/releases/download/v1.7.0/erfa-1.7.0.tar.gz"

    version("2.0.0", sha256="75cb0a2cc1561d24203d9d0e67c21f105e45a70181d57f158e64a46a50ccd515")
    version("1.7.0", sha256="f0787e30e848750c0cbfc14827de6fc7f69a2d5ef0fc653504e74b8967a764e0")
    version("1.4.0", sha256="035b7f0ad05c1191b8588191ba4b19ba0f31afa57ad561d33bd5417d9f23e460")

    depends_on("c", type="build")  # generated
