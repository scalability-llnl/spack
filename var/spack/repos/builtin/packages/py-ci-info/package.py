# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCiInfo(PythonPackage):
    """Continuous Integration Information.

    A Python implementation of watson/ci-info. Get details about the current
    Continuous Integration environment.
    """

    homepage = "https://github.com/mgxd/ci-info"
    pypi = "ci-info/ci-info-0.2.0.tar.gz"

    license("MIT")

    version("0.3.0", sha256="1fd50cbd401f29adffeeb18b0489e232d16ac1a7458ac6bc316deab6ae535fb0")
    version("0.2.0", sha256="dd70632c977feb8797b1e633507166b64ad5f57183cebb2b0ea56934abba4616")

    depends_on("python@3.7:", when="@0.3:", type=("build", "run"))
    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
