# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySspilib(PythonPackage):
    """SSPI API bindings for Python."""

    homepage = "https://github.com/jborean93/sspilibi"
    pypi = "sspilib/sspilib-0.1.0.tar.gz"

    maintainers("wdconinc")

    license("MIT", checked_by="wdconinc")

    version("0.1.0", sha256="58b5291553cf6220549c0f855e0e6973f4977375d8236ce47bb581efb3e9b1cf")

    depends_on("py-setuptools@61:", type="build")
    depends_on("py-cython@3", type=("build", "run"))
