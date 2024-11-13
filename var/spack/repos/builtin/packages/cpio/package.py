# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Cpio(AutotoolsPackage, GNUMirrorPackage):
    """GNU cpio copies files into or out of a cpio or tar archive and the file system.
    The archive can be another file on the disk, a magnetic tape, or a pipe.
    """

    homepage = "https://www.gnu.org/software/cpio/"
    gnu_mirror_path = "cpio/cpio-2.13.tar.gz"

    executables = ["^cpio$"]

    license("GPL-3.0-or-later")

    version("2.15", sha256="efa50ef983137eefc0a02fdb51509d624b5e3295c980aa127ceee4183455499e")
    version("2.14", sha256="145a340fd9d55f0b84779a44a12d5f79d77c99663967f8cfa168d7905ca52454")
    version("2.13", sha256="e87470d9c984317f658567c03bfefb6b0c829ff17dbf6b0de48d71a4c8f3db88")

    depends_on("c", type="build")  # generated

    build_directory = "spack-build"

    def patch(self):
        """Fix mutiple definition of char *program_name for gcc@10: and clang"""
        filter_file(r"char \*program_name;", "", "src/global.c")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"\(GNU cpio\)\s+(\S+)", output)
        return match.group(1) if match else None

    def flag_handler(self, name, flags):
        spec = self.spec

        if name == "cflags":
            if spec.satisfies("%intel@:17"):
                flags.append("-no-gcc")

            elif spec.satisfies("%clang") or spec.satisfies("%fj"):
                flags.append("--rtlib=compiler-rt")

        return (flags, None, None)
