# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBlessings(PythonPackage):
    """A nicer, kinder way to write to the terminal"""

    homepage = "https://github.com/erikrose/blessings"
    pypi = "blessings/blessings-1.6.tar.gz"

    license("MIT")

    version("1.6", sha256="edc5713061f10966048bf6b40d9a514b381e0ba849c64e034c4ef6c1847d3007")

    # Needs 2to3
    depends_on("py-setuptools@:57", type="build")
