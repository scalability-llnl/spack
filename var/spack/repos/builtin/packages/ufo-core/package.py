# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UfoCore(CMakePackage):
    """The UFO data processing framework is a C library suited to build general
    purpose streams data processing on heterogeneous architectures such as
    CPUs, GPUs or clusters. This package contains the run-time system and
    development files."""

    homepage = "https://ufo.kit.edu"
    url = "https://github.com/ufo-kit/ufo-core/archive/v0.14.0.tar.gz"

    license("LGPL-3.0-only")

    version("0.16.0", sha256="ff895386e10920ec399b9951a231e517bd6cf5f70c3b527430c2c1fccff6f181")
    version("0.14.0", sha256="3bf0d1924d6ae3f51673cc8b0b31b17873e79f1a0129a9af54b4062b1b2b3ad7")

    depends_on("c", type="build")  # generated

    depends_on("glib")
    depends_on("json-glib")
