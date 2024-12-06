# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPkginfo(PythonPackage):
    """Query metadatdata from sdists / bdists / installed packages."""

    homepage = "https://code.launchpad.net/~tseaver/pkginfo/trunk"
    pypi = "pkginfo/pkginfo-1.5.0.1.tar.gz"

    license("MIT")

    version("1.9.6", sha256="8fd5896e8718a4372f0ea9cc9d96f6417c9b986e23a4d116dda26b62cc29d046")
    version("1.8.3", sha256="a84da4318dd86f870a9447a8c98340aa06216bfc6f2b7bdc4b8766984ae1867c")
    version("1.7.1", sha256="e7432f81d08adec7297633191bbf0bd47faf13cd8724c3a13250e51d542635bd")
    version("1.5.0.1", sha256="7424f2c8511c186cd5424bbf31045b77435b37a8d604990b79d4e70d741148bb")

    depends_on("py-setuptools", type="build")
