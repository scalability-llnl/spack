# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpdlog(PythonPackage):
    """The py-spdlog package provides a Python wrapper
    to the C++ spdlog library."""

    homepage = "https://github.com/bodgergely/spdlog-python"
    pypi = "spdlog/spdlog-2.0.0.tar.gz"
    git = "https://github.com/bodgergely/spdlog-python.git"

    # NOTE: Righ now py-spdlog works with a git submodule containing a copy
    # of spdlog. Ideally we would want to install spdlog ourselves and make
    # this package depend on it. There is an issue for that on the py-spdlog
    # github repository: https://github.com/bodgergely/spdlog-python/issues/19

    license("MIT")

    version("master", branch="master", submodules=True)
    version("2.0.0", sha256="b8d3732839850da414a47e91547ee1246f0690cb83f43f11a1fbaec40b7b968c")

    depends_on("cxx", type="build")  # generated

    depends_on("py-pybind11@2.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pytest-runner", type="build")
