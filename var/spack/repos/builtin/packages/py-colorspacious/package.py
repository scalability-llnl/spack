# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColorspacious(PythonPackage):
    """A powerful, accurate, and easy-to-use Python library for doing colorspace
    conversions.
    """

    homepage = "https://github.com/njsmith/colorspacious"
    pypi = "colorspacious/colorspacious-1.1.2.tar.gz"

    license("MIT")

    version("1.1.2", sha256="5e9072e8cdca889dac445c35c9362a22ccf758e97b00b79ff0d5a7ba3e11b618")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
