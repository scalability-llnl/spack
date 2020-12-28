# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTeachingdemos(RPackage):
    """TeachingDemos: Demonstrations for Teaching and Learning.

    Demonstration functions that can be used in a classroom to demonstrate
    statistical concepts, or on your own to better understand the concepts
    or the programming."""

    homepage = "https://cloud.r-project.org/package=TeachingDemos"
    url      = "https://cloud.r-project.org/src/contrib/TeachingDemos_2.10.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/TeachingDemos"

    version('2.10', sha256='2ef4c2e36ba13e32f66000e84281a3616584c86b255bca8643ff3fe4f78ed704')
