# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class NosourceBundle(BundlePackage):
    """Simple bundle package with one dependency"""

    homepage = "http://www.example.com"

    version("1.0")

    depends_on("dependency-install")
