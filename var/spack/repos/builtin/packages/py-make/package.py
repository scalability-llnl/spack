# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMake(PythonPackage):
    """Create project layout from jinja2 templates"""

    homepage = "https://github.com/fholmer/make"
    git = "https://github.com/fholmer/make.git"

    version("0.1.6.post2", commit="ce2ef5834837a35dba5f2bea8866b61c8907c83a")
    version("0.1.6", commit="c6e2615d01d8d5f58181e39d0f594fe5baae3c5f")

    depends_on("py-setuptools", type="build")
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-jinja2-time", type=("build", "run"))
