# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMdaXdrlib(PythonPackage):
    """A stand-alone XDRLIB module extracted from CPython 3.10.8"""

    homepage = "https://github.com/MDAnalysis/mda-xdrlib"
    pypi = "mda_xdrlib/mda_xdrlib-0.2.0.tar.gz"

    maintainers("RMeli")

    license("0BSD")

    version("0.2.0", sha256="f26f7158a83c32b96d15b530fce2cbc1190c4b7024e41faa4ab3e3db74e272af")

    depends_on("py-setuptools@61.2:", type="build")
    depends_on("py-tomli", when="^python@:3.10", type="build")
