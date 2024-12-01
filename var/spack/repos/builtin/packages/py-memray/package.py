# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMemray(PythonPackage):
    """A memory profiler for Python applications."""

    homepage = "https://github.com/bloomberg/memray"
    pypi = "memray/memray-1.1.0.tar.gz"

    license("Apache-2.0")

    version("1.1.0", sha256="876e46e0cd42394be48b33f81314bc946f4eb023b04bf1def084c25ccf1d2bb6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@3.7:", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"))
    depends_on("libunwind")
    depends_on("lz4")

    conflicts("platform=darwin", msg="memray only supports Linux platforms")
    conflicts("platform=windows", msg="memray only supports Linux platforms")
