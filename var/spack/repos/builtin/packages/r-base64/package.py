# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBase64(RPackage):
    """Base64 Encoder and Decoder.

    Compatibility wrapper to replace the orphaned package by Romain Francois.
    New applications should use the 'openssl' or 'base64enc' package
    instead."""

    cran = "base64"

    license("MIT")

    version("2.0.1", sha256="4d22687c0195c2049e0af2c613b1ebcb908037010ad6e550bf47d69e842535f1")
    version("2.0", sha256="8e259c2b12446197d1152b83a81bab84ccb5a5b77021a9b5645dd4c63c804bd1")

    depends_on("r-openssl", type=("build", "run"))
