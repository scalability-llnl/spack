# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Unifdef(MakefilePackage):
    """The unifdef utility selectively processes conditional C preprocessor #if
    and #ifdef directives. It removes from a file both the directives and the
    additional text that they delimit, while otherwise leaving the file
    alone."""

    homepage = "https://dotat.at/prog/unifdef/"
    url = "https://dotat.at/prog/unifdef/unifdef-2.11.tar.xz"

    maintainers("matthiasdiener")

    license("BSD-2-Clause AND BSD-3-Clause", checked_by="tgamblin")

    version("2.12", sha256="43ce0f02ecdcdc723b2475575563ddb192e988c886d368260bc0a63aee3ac400")
    version("2.11", sha256="828ffc270ac262b88fe011136acef2780c05b0dc3c5435d005651740788d4537")

    depends_on("c", type="build")  # generated

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter(r"\$\{HOME\}", prefix)
