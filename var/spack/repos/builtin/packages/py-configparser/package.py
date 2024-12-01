# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConfigparser(PythonPackage):
    """This library brings the updated configparser from Python 3.5 to
    Python 2.6-3.5."""

    homepage = "https://docs.python.org/3/library/configparser.html"
    pypi = "configparser/configparser-3.5.0.tar.gz"

    license("MIT")

    version("5.2.0", sha256="1b35798fdf1713f1c3139016cfcbc461f09edbf099d1fb658d4b7479fcaa3daa")
    version("3.5.1", sha256="f41e19cb29bebfccb1a78627b3f328ec198cc8f39510c7c55e7dfc0ab58c8c62")
    version("3.5.0", sha256="5308b47021bc2340965c371f0f058cc6971a04502638d4244225c49d80db273a")

    depends_on("python@3.6:", type=("build", "run"), when="@5.2.0:")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@34.4:", type="build", when="@3.5.1:")
    depends_on("py-setuptools@56:", type="build", when="@5.2.0:")
    depends_on("py-setuptools-scm@3.4.1:+toml", type="build", when="@5.2.0:")
