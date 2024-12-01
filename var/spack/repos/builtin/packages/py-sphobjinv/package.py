# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphobjinv(PythonPackage):
    """Sphinx objects.inv Inspection/Manipulation Tool."""

    homepage = "https://github.com/bskinn/sphobjinv"
    pypi = "sphobjinv/sphobjinv-2.3.1.tar.gz"

    version("2.3.1", sha256="1442a47fc93587a0177be95346904e388ef85a8366f90a1835a7c3eeeb122eb7")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-attrs@19.2:", type=("build", "run"))
    depends_on("py-certifi", type=("build", "run"))
    depends_on("py-jsonschema@3.0:", type=("build", "run"))
