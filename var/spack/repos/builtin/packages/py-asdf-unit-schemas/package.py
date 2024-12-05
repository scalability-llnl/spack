# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsdfUnitSchemas(PythonPackage):
    """ASDF schemas for units"""

    homepage = "https://asdf-unit-schemas.readthedocs.io"
    pypi = "asdf_unit_schemas/asdf_unit_schemas-0.1.0.tar.gz"

    maintainers("lgarrison")

    license("BSD-3-Clause")

    version("0.1.0", sha256="42b78d67213efe4ffd4529fb0e58d9c7a0dab5cbf8839b230f1bc0a446bff999")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4: +toml", type="build")

    depends_on("py-asdf-standard@1.0.1:", type=("build", "run"))
    depends_on("py-importlib-resources@3:", type=("build", "run"), when="^python@:3.8")
