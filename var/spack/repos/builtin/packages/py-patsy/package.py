# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPatsy(PythonPackage):
    """A Python package for describing statistical models and for
    building design matrices."""

    homepage = "https://github.com/pydata/patsy"
    pypi = "patsy/patsy-0.5.2.tar.gz"

    license("PSF-2.0")

    version("0.5.3", sha256="bdc18001875e319bc91c812c1eb6a10be4bb13cb81eb763f466179dca3b67277")
    version("0.5.2", sha256="5053de7804676aba62783dbb0f23a2b3d74e35e5bfa238b88b7cbf148a38b69d")
    version("0.5.1", sha256="f115cec4201e1465cd58b9866b0b0e7b941caafec129869057405bfe5b5e3991")
    version(
        "0.4.1",
        sha256="dc1cc280045b0e6e50c04706fd1e26d2a00ea400aa112f88e8142f88b0b7d3d4",
        url="https://pypi.io/packages/source/p/patsy/patsy-0.4.1.zip",
    )
    variant("splines", default=False, description="Offers spline related functions")

    depends_on("py-setuptools", type="build")

    depends_on("py-six", type=("build", "run"))
    depends_on("py-numpy@1.4:", type=("build", "run"), when="@0.5.1:")
    depends_on("py-numpy", type=("build", "run"))

    depends_on("py-scipy", type=("build", "run"), when="+splines")
