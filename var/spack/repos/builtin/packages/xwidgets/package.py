# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xwidgets(CMakePackage):
    """A C++ backend for Jupyter interactive widgets"""

    homepage = "https://github.com/jupyter-xeus/xwidgets"
    url = "https://github.com/jupyter-xeus/xwidgets/archive/0.25.0.tar.gz"
    git = "https://github.com/jupyter-xeus/xwidgets.git"

    maintainers("tomstitt")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("0.25.0", sha256="7b6d36999e3b926c40389167c48b33f234a075365f089f89571b33a160421d8e")

    depends_on("cxx", type="build")  # generated

    depends_on("xtl@0.7.0:0.7", when="@0.25.0:")
    depends_on("xproperty@0.11.0:0.11", when="@0.25.0:")
    depends_on("xeus@1.0:1", when="@0.25.0:")
    depends_on("nlohmann-json@3.6.1:3", when="@0.25.0:")
