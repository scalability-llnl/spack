# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Pdt(AutotoolsPackage):
    """Program Database Toolkit (PDT) is a framework for analyzing source
    code written in several programming languages and for making rich
    program knowledge accessible to developers of static and dynamic
    analysis tools. PDT implements a standard program representation,
    the program database (PDB), that can be accessed in a uniform way
    through a class library supporting common PDB operations.

    """

    maintainers("wspear", "eugeneswalker", "khuck", "sameershende")
    homepage = "https://www.cs.uoregon.edu/research/pdt/home.php"
    url = "https://www.cs.uoregon.edu/research/paracomp/pdtoolkit/Download/pdtoolkit-3.25.1.tar.gz"

    tags = ["e4s"]

    license("GPL-2.0-only")

    version("3.25.2", sha256="01c2d403bc6672b2b264a182c325806541066c5ed5713878eb598f5506428cbe")
    version("3.25.1", sha256="0b6f8a6b8769c181b2ae6cae7298f04b8e3e3d68066f598ed24574e19500bc97")
    version("3.25", sha256="1037628d854edfeded3d847150d3e8fbd3774e8146407ce32f5021c80f6299be")
    version("3.24", sha256="4a2bb31f3f7f2e52ed49d9b7189ade05170a4386ef76771280a06e8b3ca97ab2")
    version("3.23", sha256="c17fca2f9126e10b4922b54e737a39c081b2dcf99bf20062c203247e05ecb850")
    version("3.22.1", sha256="215a3684bfe0df8ca673b09ee1efcdb5388ab5f45130dd67a00ef1041bfb5818")
    version("3.22", sha256="3a539c04b6d1b7b77b31999a7936717dfccda138b318756e306415e3af17dd8b")
    version("3.21", sha256="582f14347b4dd7a6f9bc2f41b3b62a6b40079c0a3127109c2c0c953e3c922401")
    version("3.20", sha256="561c3559fba7c3d053df3b98f75f3c2087c64a6d51204b40825a1737677f780b")
    version("3.19", sha256="d57234077e2e999f2acf9860ea84369a4694b50cc17fa6728e5255dc5f4a2160")
    version("3.18.1", sha256="d06c2d1793fadebf169752511e5046d7e02cf3fead6135a35c34b1fee6d6d3b2")

    depends_on("cxx", type="build")  # generated

    variant("pic", default=False, description="Builds with pic")

    patch("cray_configure.patch", when="%cce")

    def patch(self):
        spec = self.spec
        if spec.satisfies("%clang") or spec.satisfies("%apple-clang"):
            filter_file(r"PDT_GXX=g\+\+ ", r"PDT_GXX=clang++ ", "ductape/Makefile")

    def configure(self, spec, prefix):
        options = ["-prefix=%s" % prefix]
        if self.compiler.name == "xl":
            options.append("-XLC")
        elif self.compiler.name == "intel":
            options.append("-icpc")
        elif self.compiler.name == "oneapi":
            if spec.satisfies("@3.25.2:"):
                options.append("-icpx")
            else:
                options.append("-icpc")
        elif self.compiler.name == "pgi":
            options.append("-pgCC")
        elif self.compiler.name == "gcc":
            options.append("-GNU")
        elif self.compiler.name in ["clang", "apple-clang", "aocc"]:
            options.append("-clang")
        elif self.compiler.name == "cce":
            options.append("-CC")
        else:
            raise InstallError("Unknown/unsupported compiler family: " + self.compiler.name)

        if "+pic" in spec:
            options.append("-useropt=" + self.compiler.cxx_pic_flag)

        configure(*options)

    @run_after("install")
    def link_arch_dirs(self):
        # Link arch-specific directories into prefix
        for dir in os.listdir(self.prefix):
            path = join_path(self.prefix, dir)
            if not os.path.isdir(path) or os.path.islink(path):
                continue
            for d in ("bin", "lib"):
                src = join_path(path, d)
                dst = join_path(self.prefix, d)
                if os.path.isdir(src) and not os.path.exists(dst):
                    os.symlink(join_path(dir, d), dst)
