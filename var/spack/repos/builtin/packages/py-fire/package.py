# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFire(PythonPackage):
    """Python Fire is a library for automatically generating command line
    interfaces (CLIs) with a single line of code."""

    homepage = "https://github.com/google/python-fire"
    pypi = "fire/fire-0.2.1.tar.gz"

    license("Apache-2.0")

    version("0.4.0", sha256="c5e2b8763699d1142393a46d0e3e790c5eb2f0706082df8f647878842c216a62")
    version("0.3.1", sha256="9736a16227c3d469e5d2d296bce5b4d8fa8d7851e953bda327a455fc2994307f")
    version("0.3.0", sha256="96c372096afcf33ddbadac8a7ca5b7e829e8d7157d0030bd964bf959afde5c2c")
    version("0.2.1", sha256="6865fefc6981a713d2ce56a2a2c92c56c729269f74a6cddd6f4b94d16ae084c9")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("py-termcolor", type=("build", "run"))
