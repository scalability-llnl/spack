# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDocopt(PythonPackage):
    """Command-line interface description language."""

    homepage = "http://docopt.org/"
    pypi = "docopt/docopt-0.6.2.tar.gz"

    license("MIT")

    version("0.6.2", sha256="49b3a825280bd66b3aa83585ef59c4a8c82f2c8a522dbe754a8bc8d08c85c491")

    depends_on("py-setuptools", type="build")
