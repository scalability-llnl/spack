# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEeglabio(PythonPackage):
    """I/O support for EEGLAB files in Python."""

    homepage = "https://github.com/jackz314/eeglabio"
    pypi = "eeglabio/eeglabio-0.0.2.post4.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.0.2.post4", sha256="64ccaca0ec1b0aa78ca6569ed3581ea601dec51ae6a3b2971e9dc82f54d95f39"
    )

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
