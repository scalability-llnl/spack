# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyprof2html(PythonPackage):
    """Python cProfile and hotshot profile's data to HTML Converter"""

    pypi = "pyprof2html/pyprof2html-0.3.1.tar.gz"

    license("BSD-3-Clause")

    version("0.3.1", sha256="db2d37e21d8c76f2fd25fb1ba9273c9b3ff4a98a327e37d943fed1ea225a6720")

    patch("version_0.3.1.patch", when="@0.3.1")

    depends_on("py-setuptools", type="build")
    depends_on("py-jinja2", type=("build", "run"))
