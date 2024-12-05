# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyabel(PythonPackage):
    """A Python package for forward and inverse Abel transforms."""

    homepage = "https://github.com/PyAbel/PyAbel"
    pypi = "PyAbel/PyAbel-0.9.0.tar.gz"

    maintainers("valmar")

    license("MIT")

    version("0.9.0", sha256="4052143de9da19be13bb321fb0524090ffc8cdc56e0e990e5d6f557f18109f08")

    depends_on("py-setuptools@44.0:", type="build")
    depends_on("py-numpy@1.16:", type=("build", "run"))
    depends_on("py-scipy@1.2:", type=("build", "run"))
    depends_on("py-six@1.10.0:", type=("build", "run"))
