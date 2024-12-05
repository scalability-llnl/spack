# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SkilionOnedrive(MakefilePackage):
    """A complete tool to interact with OneDrive on Linux,
    developed by Skilion, following the UNIX philosophy."""

    homepage = "https://github.com/skilion/onedrive"
    url = "https://github.com/skilion/onedrive/archive/v1.1.1.tar.gz"

    license("GPL-3.0-or-later")

    version("1.1.1", sha256="fb51c81ec95c28f3fe3b29e3b7f915e30161bd5f4b14bb53ae5c2233cc1e92e9")

    depends_on("dmd")
    depends_on("curl")
    depends_on("sqlite")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        # Generate the version file
        makefile.filter(".git/HEAD .git/index", "", string=True)
        makefile.filter("$(shell git describe --tags)", "{0}".format(spec.version), string=True)
        # Patch sqlite.d https://github.com/skilion/onedrive/issues/392
        sqlited = FileFilter("src/sqlite.d")
        sqlited.filter("std.c.stdlib", "core.stdc.stdlib", string=True)

    def build(self, spec, prefix):
        make("onedrive", "DESTDIR={0}".format(prefix), "PREFIX=/")

    def install(self, spec, prefix):
        make("install", "DESTDIR={0}".format(prefix), "PREFIX=/")
