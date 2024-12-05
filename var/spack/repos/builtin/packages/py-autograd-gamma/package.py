# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAutogradGamma(PythonPackage):
    """autograd compatible approximations to the derivatives of the
    Gamma-family of functions."""

    homepage = "https://github.com/CamDavidsonPilon/autograd-gamma"
    pypi = "autograd-gamma/autograd-gamma-0.4.3.tar.gz"

    license("MIT")

    version("0.4.3", sha256="2cb570cbb8da61ede937ccc004d87d3924108f754b351a86cdd2ad31ace6cdf6")

    depends_on("py-setuptools", type="build")
    depends_on("py-autograd@1.2.0:", type=("build", "run"))
    depends_on("py-scipy@1.2.0:", type=("build", "run"))
