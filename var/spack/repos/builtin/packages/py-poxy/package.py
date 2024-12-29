# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoxy(PythonPackage):
    """Documentation generator for C++"""

    homepage = "https://github.com/marzer/poxy"
    pypi = "poxy/poxy-0.18.0.tar.gz"

    license("MIT", checked_by="pranav-sivaraman")

    version("0.18.0", sha256="f5da8ff04ec08859bfd1c8ec6ef61b70e3af630915a4cce6a3e377eec3bcd3d4")

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.7:")
        depends_on("py-misk@0.8.1:")
        depends_on("py-beautifulsoup4")
        depends_on("py-jinja2")
        depends_on("py-pygments")
        depends_on("py-html5lib")
        depends_on("py-lxml")
        depends_on("py-tomli")
        depends_on("py-schema")
        depends_on("py-requests")
        depends_on("py-trieregex")
        depends_on("py-colorama")

    conflicts("py-schema@=0.7.5")
