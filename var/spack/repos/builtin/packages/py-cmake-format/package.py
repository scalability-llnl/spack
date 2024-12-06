# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCmakeFormat(PythonPackage):
    """cmake-format project provides Quality Assurance (QA) tools for
    cmake. Tools include cmake-annotate, cmake-format, cmake-lint,
    and ctest-to."""

    pypi = "cmake_format/cmake_format-0.6.9.tar.gz"

    version("0.6.11", sha256="aa3d0e6156bcd4ae8fbd630ccb1d4995179b37b1b31923f2eb53764104da75f3")
    version("0.6.10", sha256="82f0ef16236225cb43f45bfb6983ef7f6f72634727a1a6c26290402527bdd793")
    version("0.6.9", sha256="b2f8bf2e9c6651126f2f2954b7803222b0faf6b8649eabc4d965ea97483a4d20")

    variant("yaml", default=False, description="Support for YAML config files")
    variant("htmlgen", default=False, description="Support for HTML annotator")

    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.13.0:", type=("build", "run"))

    depends_on("py-pyyaml@5.3:", when="+yaml", type=("build", "run"))
    depends_on("py-jinja2@2.10.3", when="+htmlgen", type=("build", "run"))
