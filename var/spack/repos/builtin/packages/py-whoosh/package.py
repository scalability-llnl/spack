# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWhoosh(PythonPackage):
    """Fast, pure-Python full text indexing, search, and spell checking library."""

    homepage = "https://whoosh.readthedocs.io"
    pypi = "Whoosh/Whoosh-2.7.4.tar.gz"

    license("BSD-2-Clause-FreeBSD")

    version("2.7.4", sha256="7ca5633dbfa9e0e0fa400d3151a8a0c4bec53bd2ecedc0a67705b17565c31a83")

    depends_on("py-setuptools", type="build")
