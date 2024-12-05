# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UfoFilters(CMakePackage):
    """The UFO data processing framework is a C library suited to build general
    purpose streams data processing on heterogeneous architectures such as
    CPUs, GPUs or clusters. This package contains filter plugins."""

    homepage = "https://ufo.kit.edu"
    url = "https://github.com/ufo-kit/ufo-filters/archive/v0.14.1.tar.gz"

    version("0.14.1", sha256="084d7cdef59205e1a048e5c142be1ffeaacedc42965824b642e8302ef30ebb13")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("ufo-core")
