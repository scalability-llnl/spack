# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaskPaginate(PythonPackage):
    """Simple paginate for flask (study from will_paginate). Use bootstrap css
    framework, supports bootstrap2&3 and foundation."""

    homepage = "https://github.com/lixxu/flask-paginate"
    pypi = "flask-paginate/flask-paginate-2022.1.8.tar.gz"

    maintainers("meyersbs")

    license("BSD-3-Clause")

    version("2022.1.8", sha256="a32996ec07ca004c45b768b0d50829728ab8f3986c0650ef538e42852c7aeba2")

    # From setup.py:
    depends_on("py-setuptools", type="build")
    depends_on("py-flask", type=("build", "run"))
