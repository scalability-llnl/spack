# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMffpy(PythonPackage):
    """Reader and Writer for Philips' MFF file format."""

    homepage = "https://github.com/BEL-Public/mffpy"
    pypi = "mffpy/mffpy-0.6.3.tar.gz"

    license("Apache-2.0")

    version("0.6.3", sha256="fceaf59f5fccb26b6e8a0363579d27e53db547493af353737a24983d95dc012d")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pytz@2019.2:", type=("build", "run"))
    depends_on("py-numpy@1.15.1:", type=("build", "run"))
    depends_on("py-deprecated@1.2.12:", type=("build", "run"))
