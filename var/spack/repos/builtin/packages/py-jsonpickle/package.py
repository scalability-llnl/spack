# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJsonpickle(PythonPackage):
    """Python library for serializing any arbitrary object graph into JSON."""

    homepage = "https://github.com/jsonpickle/jsonpickle"
    pypi = "jsonpickle/jsonpickle-1.4.1.tar.gz"

    license("BSD-3-Clause")

    version("2.2.0", sha256="7b272918b0554182e53dc340ddd62d9b7f902fec7e7b05620c04f3ccef479a0e")
    version("2.0.0", sha256="0be49cba80ea6f87a168aa8168d717d00c6ca07ba83df3cec32d3b30bfe6fb9a")
    version("1.4.1", sha256="e8d4b7cd0bd6826001a74377df1079a76ad8bae0f909282de2554164c837c8ba")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@42:", type="build", when="@2.0.0:")
    depends_on("py-setuptools-scm@3.4.1:+toml", type="build")
    depends_on("py-importlib-metadata", when="^python@:3.7", type=("build", "run"))
