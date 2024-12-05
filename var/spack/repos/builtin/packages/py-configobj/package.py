# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConfigobj(PythonPackage):
    """Config file reading, writing and validation."""

    homepage = "https://github.com/DiffSK/configobj"
    pypi = "configobj/configobj-5.0.6.tar.gz"

    version("5.0.6", sha256="a2f5650770e1c87fb335af19a9b7eb73fc05ccf22144eb68db7d00cd2bcb0902")
    version("4.7.2", sha256="515ff923462592e8321df8b48c47e3428f8d406ee22b8de77bef969d1af11171")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
