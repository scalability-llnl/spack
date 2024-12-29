# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Giflib(MakefilePackage, SourceforgePackage):
    """The GIFLIB project maintains the giflib service library, which has
    been pulling images out of GIFs since 1989."""

    homepage = "https://giflib.sourceforge.net/"
    sourceforge_mirror_path = "giflib/giflib-5.1.4.tar.gz"

    license("MIT")

    version("5.2.2", sha256="be7ffbd057cadebe2aa144542fd90c6838c6a083b5e8a9048b8ee3b66b29d5fb")
    version("5.2.1", sha256="31da5562f44c5f15d63340a09a4fd62b48c45620cd302f77a6d9acf0077879bd")
    version("5.2.0", sha256="dc7257487c767137602d86c17098ec97065a718ff568a61cfcf1a9466f197b1f")
    version(
        "5.1.4",
        sha256="df27ec3ff24671f80b29e6ab1c4971059c14ac3db95406884fc26574631ba8d5",
        extension="tar.bz2",
    )

    depends_on("c", type="build")

    depends_on("automake", type="build", when="@:5.2.0")
    depends_on("autoconf", type="build", when="@:5.2.0")
    depends_on("m4", type="build", when="@:5.2.0")
    depends_on("libtool", type="build", when="@:5.2.0")

    # https://sourceforge.net/p/giflib/bugs/133/
    patch(
        "https://sourceforge.net/p/giflib/bugs/_discuss/thread/4e811ad29b/c323/attachment/Makefile.patch",
        sha256="a94e7bdd8840a31cecacc301684dfdbf7b98773ad824aeaab611fabfdc513036",
        level=0,
        when="@5.2.0:5.2.1 platform=darwin",
    )
    patch("bsd-head.patch")

    # error: no such file or directory: 'dgif_lib.o'
    parallel = False

    def prefix_and_libversion_args(self):
        args = []
        if self.spec.satisfies("@5.2.0:"):
            args.extend(
                [
                    "PREFIX={0}".format(self.spec.prefix),
                    "LIBMAJOR={0}".format(self.spec.version.up_to(1)),
                    "LIBVER={0}".format(self.spec.version),
                ]
            )
        return args

    @property
    def build_targets(self):
        targets = ["all"] + self.prefix_and_libversion_args()
        return targets

    @property
    def install_targets(self):
        targets = ["install"] + self.prefix_and_libversion_args()
        return targets

    @property
    def libs(self):
        return find_libraries(["libgif"], root=self.prefix.lib) or find_libraries(
            ["libgif"], root=self.prefix.lib64
        )

    def check(self):
        make("check", parallel=False)

    def edit(self, spec, prefix):
        if spec.satisfies("@:5.2.0"):
            configure = Executable("./configure")
            configure("--prefix={0}".format(prefix))
        # remove call to convert in doc makefile
        with working_dir("doc"):
            filter_file("^.*convert.*-resize.*$", "", "Makefile")
