# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCustomInherit(PythonPackage):
    """A Python package that provides customized docstring inheritance schemes
    between derived classes and their parents.
    """

    homepage = "https://github.com/rsokl/custom_inherit"
    pypi = "custom_inherit/custom_inherit-2.2.2.tar.gz"

    maintainers("snehring")

    license("MIT")

    version("2.4.1", sha256="7052eb337bcce83551815264391cc4efc2bf70b295a3c52aba64f1ab57c3a8a2")
    version("2.2.2", sha256="83c048bc3415a9e38e44e78dbe231f837aa3d4fd91b4e71443b6f6e38034f583")

    depends_on("py-setuptools", type="build")
