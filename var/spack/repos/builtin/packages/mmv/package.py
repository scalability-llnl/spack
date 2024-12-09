# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Mmv(MakefilePackage):
    """Move/Copy/Append/Link multiple files mmv is a program to
    move/copy/append/link multiple files according to a set of wildcard
    patterns. This multiple action is performed safely, i.e. without any
    unexpected deletion of files due to collisions of target names with
    existing filenames or with other target names."""

    homepage = "https://packages.debian.org/source/buster/mmv"
    url = "https://deb.debian.org/debian/pool/main/m/mmv/mmv_1.01b.orig.tar.gz"

    version("1.01b", sha256="0399c027ea1e51fd607266c1e33573866d4db89f64a74be8b4a1d2d1ff1fdeef")

    depends_on("c", type="build")  # generated

    patch("better-diagnostics-for-directories-584850.diff")
    patch("format-security.diff")
    patch("man-page-examples.diff")
    patch("man-page-fixes.diff")
    patch("man-page-warning-149873.diff")
    patch("patches-as-of-mmv-1.01b-15.diff")
    patch("utime.diff")

    def build(self, spec, prefix):
        cc = Executable(self.compiler.cc)
        cc("-DIS_SYSV", "-DHAS_DIRENT", "-DHAS_RENAME", "-O2", "-o", "mmv", "mmv.c")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("mmv", prefix.bin)
        os.symlink(join_path(prefix.bin, "mmv"), "mad")
        os.symlink(join_path(prefix.bin, "mmv"), "mcp")
        os.symlink(join_path(prefix.bin, "mmv"), "mln")
        mkdirp(prefix.man1)
        install("mmv.1", prefix.man1)
        os.symlink(join_path(prefix.man1, "mmv.1"), "mad.1")
        os.symlink(join_path(prefix.man1, "mmv.1"), "mcp.1")
        os.symlink(join_path(prefix.man1, "mmv.1"), "mln.1")
