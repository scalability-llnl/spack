# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySimplekml(PythonPackage):
    """simplekml is a python package which enables you to generate KML with as
    little effort as possible.
    """

    homepage = "https://readthedocs.org/projects/simplekml/"
    pypi = "simplekml/simplekml-1.3.1.tar.gz"

    license("GPL-3.0-only")

    version("1.3.6", sha256="cda687be2754395fcab664e908ebf589facd41e8436d233d2be37a69efb1c536")
    version("1.3.5", sha256="657b4e20177299a4e80bacfafff1f91102010bc23dc0ce7a7ae43bdd4246049e")
    version("1.3.1", sha256="30c121368ce1d73405721730bf766721e580cae6fbb7424884c734c89ec62ad7")

    depends_on("python@2.6:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
