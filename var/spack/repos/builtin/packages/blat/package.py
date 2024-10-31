# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Blat(Package):
    """BLAT (BLAST-like alignment tool) is a pairwise sequence
    alignment algorithm."""

    homepage = "https://genome.ucsc.edu/FAQ/FAQblat.html"
    url = "https://genome-test.gi.ucsc.edu/~kent/src/blatSrc35.zip"
    maintainers("snehring")

    version("37", sha256="88ee2b272d42ab77687c61d200b11f1d58443951069feb7e10226a2509f84cf2")
    version("35", sha256="06d9bcf114ec4a4b21fef0540a0532556b6602322a5a2b33f159dc939ae53620")

    depends_on("libpng")
    depends_on("uuid", when="@37:")
    depends_on("mysql-client", when="@37:")

    @when("@37")
    def patch(self):
        filter_file(r",src\/hg\/", ",NOMATCHME", "inc/userApp.mk")

    def flag_handler(self, name, flags):
        if self.spec.satisfies("@35") and name.lower() == "cflags":
            flags.append("-fcommon")
        return (flags, None, None)

    def setup_build_environment(self, env):
        env.set("MACHTYPE", "x86_64")

    def install(self, spec, prefix):
        filter_file("CC=.*", "CC={0}".format(spack_cc), "inc/common.mk")
        mkdirp(prefix.bin)
        make("BINDIR=%s" % prefix.bin)
