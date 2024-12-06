# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AttributesFooApp(BundlePackage):
    version("1.0")
    depends_on("bar")
    depends_on("baz")
