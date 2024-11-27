# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class NoversionBundle(BundlePackage):
    """
    Simple bundle package with no version and one dependency, which
    should be rejected for lack of a version.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"
    depends_on("dependency-install")
