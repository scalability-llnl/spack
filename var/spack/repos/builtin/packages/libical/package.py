# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libical(CMakePackage):
    """Libical - an implementation of iCalendar protocols and data formats."""

    homepage = "https://github.com/libical/libical"
    url = "https://github.com/libical/libical/archive/v3.0.8.tar.gz"

    license("LGPL-2.1-only OR MPL-2.0")

    version("3.0.18", sha256="72b7dc1a5937533aee5a2baefc990983b66b141dd80d43b51f80aced4aae219c")
    version("3.0.17", sha256="bcda9a6db6870240328752854d1ea475af9bbc6356e6771018200e475e5f781b")
    version("3.0.11", sha256="1e6c5e10c5a48f7a40c68958055f0e2759d9ab3563aca17273fe35a5df7dbbf1")
    version("3.0.8", sha256="09fecacaf75ba5a242159e3a9758a5446b5ce4d0ab684f98a7040864e1d1286f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1.0:", type="build")
    depends_on("perl", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("glib@2.32:")
    depends_on("icu4c")
    depends_on("libxml2@2.7.3:")

    def cmake_args(self):
        return [self.define("ENABLE_GTK_DOC", "OFF")]
