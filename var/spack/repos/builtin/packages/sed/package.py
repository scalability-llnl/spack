# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Sed(AutotoolsPackage, GNUMirrorPackage):
    """GNU implementation of the famous stream editor."""

    homepage = "https://www.gnu.org/software/sed/"
    gnu_mirror_path = "sed/sed-4.8.tar.xz"

    license("GPL-3.0-or-later")

    version("4.9", sha256="6e226b732e1cd739464ad6862bd1a1aba42d7982922da7a53519631d24975181")
    version("4.8", sha256="f79b0cfea71b37a8eeec8490db6c5f7ae7719c35587f21edb0617f370eeff633")
    version("4.2.2", sha256="f048d1838da284c8bc9753e4506b85a1e0cc1ea8999d36f6995bcb9460cddbd7")

    depends_on("c", type="build")  # generated

    # Avoid symlinking GNUMakefile to GNUMakefile
    build_directory = "spack-build"

    executables = ["^sed$"]

    tags = ["build-tools"]

    def url_for_version(self, version):
        if Version("4.2") <= version < Version("4.3.0"):
            self.gnu_mirror_path = "sed/sed-{0}.tar.bz2".format(version)
        elif version < Version("4.2"):
            self.gnu_mirror_path = "sed/sed-{0}.tar.gz".format(version)
        return super().url_for_version(version)

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        version_regexp = r"{:s} \(GNU sed\) (\S+)".format(exe)
        match = re.search(version_regexp, output)
        return match.group(1) if match else None

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%oneapi@2023.0.0:"):
                flags.append("-Wno-error=incompatible-function-pointer-types")
        return (flags, None, None)
