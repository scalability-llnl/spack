# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Muscle(MakefilePackage):
    """MUSCLE is one of the best-performing multiple alignment programs
    according to published benchmark tests, with accuracy and speed
    that are consistently better than CLUSTALW."""

    homepage = "https://drive5.com/muscle/"

    version("3.8.31", sha256="43c5966a82133bd7da5921e8142f2f592c2b5f53d802f0527a2801783af809ad")
    version("3.8.1551", sha256="c70c552231cd3289f1bad51c9bd174804c18bb3adcf47f501afec7a68f9c482e")

    depends_on("cxx", type="build")  # generated

    @property
    def build_directory(self):
        if self.spec.satisfies("@3.8.31"):
            return "src"
        else:
            return "."

    def url_for_version(self, version):
        fmt_new = "https://drive5.com/muscle/downloads{0}/muscle{0}_src.tar.gz"
        fmt_old = "https://drive5.com/muscle/muscle_src_{0}.tar.gz"

        if version == Version("3.8.31"):
            return fmt_new.format(version.dotted)
        else:
            return fmt_old.format(version.dotted)

    def edit(self, spec, prefix):
        mkfile_name = "Makefile"

        if self.spec.satisfies("@3.8.31"):
            mkfile_name = "mk"

        makefile = FileFilter(join_path(self.build_directory, mkfile_name))
        makefile.filter("-static", "")
        makefile.filter("-funroll-loops", "")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path(self.build_directory, "muscle"), prefix.bin)
