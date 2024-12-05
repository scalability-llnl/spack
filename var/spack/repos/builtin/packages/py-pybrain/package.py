# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPybrain(PythonPackage):
    """PyBrain is the Swiss army knife for neural networking."""

    homepage = "http://pybrain.org/"

    url = "https://github.com/pybrain/pybrain/archive/refs/tags/0.3.3.tar.gz"
    git = "https://github.com/pybrain/pybrain.git"

    license("BSD-3-Clause")

    version("0.3.3.post", commit="dcdf32ba1805490cefbc0bdeb227260d304fdb42")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-scipy", type=("build", "run"))
