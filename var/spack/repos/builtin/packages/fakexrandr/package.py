# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fakexrandr(MakefilePackage):
    """This is a tool to cheat an X11 server to believe that there are more
    monitors than there actually are."""

    homepage = "https://github.com/phillipberndt/fakexrandr"
    git = "https://github.com/phillipberndt/fakexrandr.git"

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    depends_on("libxrandr")
    depends_on("libxinerama")
    depends_on("libx11")
    depends_on("python", type=("build", "run"))

    def edit(self, spec, prefix):
        # Installation instructions involve running `configure` script,
        # but this script just writes a `config.h` file like below.
        version = spec["libxrandr"].version
        with open("config.h", "w") as config:
            config.write(
                """
#define XRANDR_MAJOR {0}
#define XRANDR_MINOR {1}
#define XRANDR_PATCH {2}
#define REAL_XRANDR_LIB "{3}"
#define FAKEXRANDR_INSTALL_DIR "{4}"
""".format(
                    version[0], version[1], version[2], spec["libxrandr"].libs[0], prefix.lib
                )
            )

        # Also need to hack Makefile
        makefile = FileFilter("Makefile")
        makefile.filter("PREFIX=/usr", "PREFIX=" + prefix)
        makefile.filter("-fPIC", self.compiler.cc_pic_flag)

        # And tool used to generate skeleton
        filter_file("gcc", spack_cc, "make_skeleton.py")

        # remove 'ldconfig' on all platforms
        makefile.filter("ldconfig", "")

    # In Makefile, install commands check the target dir.
    # If it does not exist, process will stop.
    @run_before("install")
    def make_target_dir(self):
        mkdirp(self.prefix.lib)
        mkdirp(self.prefix.bin)
