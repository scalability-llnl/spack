# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPeriodictable(PythonPackage):
    """nose extends the test loading and running features of unittest,
    making it easier to write, find and run tests."""

    pypi = "periodictable/periodictable-1.4.1.tar.gz"

    version("1.5.0", sha256="b020c04c6765d21903e4604a76ca33cda98677003fe6eb48ed3690cfb03253b2")
    version("1.4.1", sha256="f42e66f6efca33caec4f27dad8d6a6d4e59da147ecf5adfce152cb84e7bd160b")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pyparsing", type=("build", "run"))
