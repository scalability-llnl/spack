# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class NosourceBundle(BundlePackage):
    """Simple bundle package with one dependency"""

    homepage = "http://www.example.com"

    version("1.0")

    depends_on("dependency-install")
