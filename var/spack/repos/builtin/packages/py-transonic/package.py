# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTransonic(PythonPackage):
    """Make your Python code fly at transonic speeds!"""

    pypi = "transonic/transonic-0.7.2.tar.gz"

    maintainers("paugier")

    license("BSD-3-Clause", checked_by="paugier")

    version("0.7.2", sha256="d0c39c13b535df4f121a8a378efc42e3d3bf4e49536d131e6d26e9fe7d5a5bf4")
    version("0.7.1", sha256="dcc59f1936d09129c800629cd4e6812571a74afe40dadd8193940b545e6ef03e")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-pdm-backend", type="build")

    with default_args(type="run"):
        depends_on("py-numpy")
        depends_on("py-beniget@0.4")
        depends_on("py-gast@0.5")
        depends_on("py-autopep8")
