# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesUrllib3(PythonPackage):
    """Typing stubs for urllib3."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-urllib3/types-urllib3-1.26.24.tar.gz"

    version(
        "1.26.25.14", sha256="229b7f577c951b8c1b92c1bc2b2fdb0b49847bd2af6d1cc2a2e3dd340f3bda8f"
    )
    version("1.26.24", sha256="a1b3aaea7dda3eb1b51699ee723aadd235488e4dc4648e030f09bc429ecff42f")

    depends_on("py-setuptools", type="build")
