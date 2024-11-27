# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jose(AutotoolsPackage):
    """This package contains a C library for performing JOSE operations."""

    homepage = "https://github.com/latchset/jose/"
    url = "https://github.com/latchset/jose/releases/download/v10/jose-10.tar.bz2"

    license("Apache-2.0")

    version("10", sha256="5c9cdcfb535c4d9f781393d7530521c72b1dd81caa9934cab6dd752cc7efcd72")
    version("9", sha256="64262b1344d92fc183f70ca93db6100cd97b3dfa7cddea1e08e8588e6cd681eb")
    version("8", sha256="24e3d71e3da5a7913ab3c299381d76dfde488d91cb108b1a9527454bf1e9dc51")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("jansson@2.10:")
    depends_on("zlib-api")
    depends_on("openssl@1.0.2:")
