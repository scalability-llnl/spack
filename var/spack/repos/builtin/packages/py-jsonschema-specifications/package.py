# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonschemaSpecifications(PythonPackage):
    """The JSON Schema meta-schemas and vocabularies, exposed as a Registry."""

    homepage = "https://jsonschema-specifications.readthedocs.io/"
    pypi = "jsonschema_specifications/jsonschema_specifications-2023.12.1.tar.gz"

    maintainers("wdconinc")

    license("MIT", checked_by="wdconinc")

    version("2023.12.1", sha256="48a76787b3e70f5ed53f1160d2b81f586e4ca6d1548c5de7085d1682674764cc")

    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")

    depends_on("py-referencing@0.31.0:", type=("build", "run"))
    depends_on("py-importlib-resources@1.4.0:", type=("build", "run"), when="^python@:3.8")
