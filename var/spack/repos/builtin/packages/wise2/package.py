# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Wise2(MakefilePackage):
    """The Wise2 package is now a rather stately bioinformatics package that
    has be around for a while. Its key programs are genewise, a program
    for aligning proteins or protein HMMs to DNA, and dynamite a rather
    cranky "macro language" which automates the production of dynamic
    programming."""

    homepage = "https://www.ebi.ac.uk/~birney/wise2/"
    url = "https://www.ebi.ac.uk/~birney/wise2/wise2.4.1.tar.gz"

    maintainers("snehring")

    version("2.4.1", sha256="240e2b12d6cd899040e2efbcb85b0d3c10245c255f3d07c1db45d0af5a4d5fa1")

    depends_on("gettext")
    depends_on("glib")
    depends_on("libiconv")
    depends_on("pcre2")

    build_directory = "src"

    build_targets = ["all"]

    def edit(self, spec, prefix):
        glib_include_include = join_path(
            spec["glib"].prefix.include, "glib-" + str(spec["glib"].version[0]) + ".0"
        )
        glib_lib_include = join_path(
            spec["glib"].prefix.lib, "glib-" + str(spec["glib"].version[0]) + ".0", "include"
        )
        glib_lib = spec["glib"].prefix.lib
        glib_config_files = ["src/makefile", "src/network/makefile", "src/models/makefile"]
        for f in glib_config_files:
            filter_file(
                "`glib-config --cflags`",
                f"-I{glib_include_include} -I{glib_lib_include}",
                f,
                string=True,
            )
            filter_file("`glib-config --libs`", f"-L{glib_lib} -lglib-2.0", f, string=True)
        filter_file('"glib.h"', "<glib.h>", "src/dynlibsrc/subseqhash.h", string=True)
        filter_file("getline", "getlineseq", "src/HMMer2/sqio.c", string=True)
        filter_file("isnumber", "isdigit", "src/models/phasemodel.c", string=True)
        filter_file(r".*welcome.csh.*", "", "src/makefile")

    def install(self, spec, prefix):
        with working_dir("src"):
            install_tree("bin", prefix.bin)
        mkdirp(prefix.share.wise2)
        install_tree("wisecfg", prefix.share.wise2)
