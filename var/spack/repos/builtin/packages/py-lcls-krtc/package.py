# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLclsKrtc(PythonPackage):
    """Very small utility class for using Kerberos authentication with Python requests."""

    pypi = "lcls-krtc/lcls-krtc-0.2.0.tar.gz"

    maintainers("valmar")

    license("MIT")

    version("0.2.0", sha256="20e6327d488d23e29135be44504bf7df72e4425a518f4222841efcd2cd2985f9")

    depends_on("py-setuptools", type="build")
    depends_on("py-pykerberos", type=("build", "run"))
