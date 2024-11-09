# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Diffmark(AutotoolsPackage):
    """Diffmark is a DSL for transforming one string to another."""

    homepage = "https://github.com/vbar/diffmark"
    git = "https://github.com/vbar/diffmark.git"

    license("diffmark")

    version("master", branch="master")

    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("libxml2")
