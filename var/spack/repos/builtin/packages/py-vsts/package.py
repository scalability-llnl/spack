# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyVsts(PythonPackage):
    """Python wrapper around the VSTS APIs."""

    homepage = "https://github.com/Microsoft/vsts-python-api"
    pypi = "vsts/vsts-0.1.25.tar.gz"

    license("MIT")

    version("0.1.25", sha256="da179160121f5b38be061dbff29cd2b60d5d029b2207102454d77a7114e64f97")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.6.0:0.6", type=("build", "run"))
