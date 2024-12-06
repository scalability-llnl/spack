# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribJquery(PythonPackage):
    """A sphinx extension which ensure that jQuery is installed with Sphinx."""

    homepage = "https://github.com/sphinx-contrib/jquery"
    pypi = "sphinxcontrib-jquery/sphinxcontrib-jquery-2.0.0.tar.gz"

    version("4.1", sha256="1620739f04e36a2c779f1a131a2dfd49b2fd07351bf1968ced074365933abc7a")
    version("2.0.0", sha256="8fb65f6dba84bf7bcd1aea1f02ab3955ac34611d838bcc95d4983b805b234daa")

    depends_on("py-flit-core@3.7:", when="@3:", type="build")
    depends_on("py-sphinx@1.8:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-setuptools@65:", when="@:3", type=("build", "run"))
