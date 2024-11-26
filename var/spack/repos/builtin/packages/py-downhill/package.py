# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDownhill(PythonPackage):
    """Stochastic optimization routines for Theano"""

    homepage = "https://github.com/lmjohns3/downhill"
    pypi = "downhill/downhill-0.4.0.tar.gz"

    license("MIT")

    version("0.4.0", sha256="074ad91deb06c05108c67d982ef71ffffb6ede2c77201abc69e332649f823b42")

    depends_on("py-setuptools", type="build")
    depends_on("py-theano", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
