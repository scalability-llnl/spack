# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyProjectq(PythonPackage):
    """
    ProjectQ is an open-source software framework for quantum computing started
    at ETH Zurich. It allows users to implement their quantum programs in
    Python using a powerful and intuitive syntax. ProjectQ can then translate
    these programs to any type of back-end, be it a simulator run on a
    classical computer of an actual quantum chip.
    """

    # Homepage and git repository
    homepage = "https://projectq.ch"
    git = "https://github.com/projectq-framework/projectq.git"

    license("Apache-2.0")

    # Versions
    version("develop", branch="develop")
    version("0.3.6", commit="fa484fe037a3a1772127bbd00fe4628ddba34611")

    depends_on("cxx", type="build")  # generated

    # Dependencies
    depends_on("py-setuptools", type=("build"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    # conflict with pybind11@2.2.0 -> see requirements.txt
    depends_on("py-pybind11@1.7:2.1,2.2.1:", type=("build", "run"))
