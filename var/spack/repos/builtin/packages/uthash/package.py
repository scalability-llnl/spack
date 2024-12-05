# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Uthash(Package):
    """C macros for hash tables and more."""

    homepage = "https://troydhanson.github.io/uthash/"
    url = "https://github.com/troydhanson/uthash/archive/refs/tags/v2.3.0.tar.gz"

    license("BSD-2-Clause")

    version("2.3.0", sha256="e10382ab75518bad8319eb922ad04f907cb20cccb451a3aa980c9d005e661acc")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        for header in find(join_path(self.stage.source_path, "src"), "*.h"):
            install(header, prefix.include)
