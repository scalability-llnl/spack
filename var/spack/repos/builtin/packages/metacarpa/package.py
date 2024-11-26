# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Metacarpa(MakefilePackage):
    """
    METACARPA is designed for meta-analysing genetic
    association studies with overlapping or related samples,
    when details of the overlap or relatedness are unknown.
    It implements and expands a method first described by Province and Borecki.
    """

    homepage = "https://www.sanger.ac.uk/tool/metacarpa/"
    url = "https://github.com/hmgu-itg/metacarpa/archive/refs/tags/1.0.1.tar.gz"

    version("1.0.1", sha256="7d8fc774a88bf75a53ef8f74462924abba9b99fccbaa9979654c01e4379fab91")

    depends_on("cxx", type="build")  # generated

    depends_on("boost@1.60.0")
    depends_on(Boost.with_default_variants)
    depends_on("cmake")
    build_system = "Makefile"
    build_directory = "src"

    def edit(self, spec, prefix):
        makefile = FileFilter("src/Makefile")
        makefile.filter(r"^IDIR.*", "IDIR=" + spec["boost"].prefix.include)
        makefile.filter(r"^LDIR.*", "LDIR=" + spec["boost"].prefix.lib)

    def install(self, spec, prefix):
        mkdirp(prefix.src)

        install_tree("src", prefix.src)

        mkdirp(prefix.bin)

        install("src/metacarpa", prefix.bin)
