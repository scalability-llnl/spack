# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBeartype(PythonPackage):
    """Unbearably fast near-real-time hybrid runtime-static type-checking in pure Python."""

    homepage = "https://beartype.readthedocs.io/"
    pypi = "beartype/beartype-0.15.0.tar.gz"

    license("MIT")

    version("0.16.2", sha256="47ec1c8c3be3f999f4f9f829e8913f65926aa7e85b180d9ffd305dc78d3e7d7b")
    version("0.15.0", sha256="2af6a8d8a7267ccf7d271e1a3bd908afbc025d2a09aa51123567d7d7b37438df")

    # See PYTHON_VERSION_MIN in beartype/meta.py
    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@:49,50.1:", type="build")
