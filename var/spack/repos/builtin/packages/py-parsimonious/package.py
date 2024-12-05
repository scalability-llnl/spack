# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParsimonious(PythonPackage):
    """(Soon to be) the fastest pure-Python PEG parser"""

    homepage = "https://github.com/erikrose/parsimonious"
    pypi = "parsimonious/parsimonious-0.8.1.tar.gz"

    license("MIT")

    version("0.10.0", sha256="8281600da180ec8ae35427a4ab4f7b82bfec1e3d1e52f80cb60ea82b9512501c")
    version("0.8.1", sha256="3add338892d580e0cb3b1a39e4a1b427ff9f687858fdd61097053742391a9f6b")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.9.0:", when="@:0.8.1", type=("build", "run"))
    depends_on("py-regex@2022.3.15:", when="@0.10.0:", type=("build", "run"))
