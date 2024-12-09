# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xproperty(CMakePackage):
    """C++ library providing traitlets-style properties"""

    homepage = "https://github.com/jupyter-xeus/xproperty"
    url = "https://github.com/jupyter-xeus/xproperty/archive/0.11.0.tar.gz"
    git = "https://github.com/jupyter-xeus/xproperty.git"

    maintainers("tomstitt")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("0.11.0", sha256="bf86a11c6758308aa0aa0f64d8dd24cd3e9d78378467b74002f552bfb75fc0eb")

    depends_on("cxx", type="build")  # generated

    depends_on("xtl@0.7.0:0.7", when="@0.11.0:")

    # C++14 support
    conflicts("%gcc@:4.8")
    conflicts("%clang@:3.3")
