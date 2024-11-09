# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCheetah3(PythonPackage):
    """Cheetah3 is a template engine and code generation tool."""

    pypi = "Cheetah3/Cheetah3-3.2.6.tar.gz"

    license("MIT")

    version("3.2.6", sha256="f1c2b693cdcac2ded2823d363f8459ae785261e61c128d68464c8781dba0466b")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-markdown@2.0.1:", type=("build", "run"))
