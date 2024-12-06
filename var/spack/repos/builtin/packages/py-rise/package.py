# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRise(PythonPackage):
    """Reveal.js - Jupyter/IPython Slideshow Extension"""

    homepage = "https://rise.readthedocs.io/"
    pypi = "rise/rise-5.6.1.tar.gz"

    license("BSD-3-Clause")

    version("5.6.1", sha256="1343f068d01adc4dd0226d9b278ce93fc92f365d827431a57e8d5679eb39f4d6")

    depends_on("python@2.7.0:2.7,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-notebook@5.5.0:", type=("build", "run"))
