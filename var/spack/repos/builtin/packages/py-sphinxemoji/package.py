# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxemoji(PythonPackage):
    """An extension to use emoji codes in your Sphinx documentation!"""

    homepage = "https://sphinxemojicodes.readthedocs.io"
    pypi = "sphinxemoji/sphinxemoji-0.2.0.tar.gz"
    license("BSD-3-Clause")

    version("0.2.0", sha256="27861d1dd7c6570f5e63020dac9a687263f7481f6d5d6409eb31ecebcc804e4c")

    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx@1.8:", type=("build", "run"))
