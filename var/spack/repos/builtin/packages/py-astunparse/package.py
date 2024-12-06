# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyAstunparse(PythonPackage):
    """An AST unparser for Python.

    This is a factored out version of unparse found in the Python source
    distribution; under Demo/parser in Python 2 and under Tools/parser in
    Python 3."""

    pypi = "astunparse/astunparse-1.6.2.tar.gz"

    license("PSF-2.0")

    version("1.6.3", sha256="5ad93a8456f0d084c3456d059fd9a92cce667963232cbf763eac3bc5b7940872")
    version("1.6.2", sha256="dab3e426715373fd76cd08bb1abe64b550f5aa494cf1e32384f26fd60961eb67")

    depends_on("py-setuptools", type="build")
    depends_on("py-wheel@0.23.0:0", type=("build", "run"))
    depends_on("py-six@1.6.1:1", type=("build", "run"))
