# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class NonExistingConditionalDep(Package):
    """Simple package with no source and one dependency"""

    homepage = "http://www.example.com"

    version("2.0")
    version("1.0")

    depends_on("dep-with-variants@999", when="@2.0")
