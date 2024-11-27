# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydevtool(PythonPackage):
    """CLI dev tools powered by pydoit."""

    homepage = "https://github.com/pydoit/pydevtool"
    pypi = "pydevtool/pydevtool-0.3.0.tar.gz"

    license("MIT")

    version("0.3.0", sha256="25e3ba4f3d33ccac33ee2b9775995848d49e9b318b7a146477fb5d52f786fc8a")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-doit@0.36:", type=("build", "run"))
