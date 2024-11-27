# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeprecation(PythonPackage):
    """The deprecation library provides a deprecated decorator and a
    fail_if_not_removed decorator for your tests."""

    homepage = "https://deprecation.readthedocs.io/"
    pypi = "deprecation/deprecation-2.0.7.tar.gz"

    license("Apache-2.0")

    version("2.1.0", sha256="72b3bde64e5d778694b0cf68178aed03d15e15477116add3fb773e581f9518ff")
    version("2.0.7", sha256="c0392f676a6146f0238db5744d73e786a43510d54033f80994ef2f4c9df192ed")

    depends_on("py-setuptools", type="build")
    depends_on("py-packaging", type=("build", "run"))
