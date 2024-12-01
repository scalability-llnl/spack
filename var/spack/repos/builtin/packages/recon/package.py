# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink

from spack.package import *


class Recon(MakefilePackage):
    """RECON: a package for automated de novo identification of repeat families
    from genomic sequences."""

    homepage = "http://eddylab.org/software/recon/"
    url = "http://eddylab.org/software/recon/RECON1.05.tar.gz"

    license("GPL-2.0-only")

    version("1.05", sha256="4d4f76f439bcffd50380cffc41a80dc15fa4a80f38a04234e24da893ed7c025a")

    depends_on("c", type="build")  # generated

    variant("repeatmasker", default=False, description="Use RepeatMasker developer patches (1.08)")

    patch("repeatmasker_recon.patch", when="+repeatmasker")

    build_directory = "src"

    depends_on("perl", type="run")

    @property
    def install_targets(self):
        return ["install", "BINDIR=%s" % self.prefix.bin]

    # edit the recon.pl script with the prefix as mentioned in the README
    def edit(self, spec, prefix):
        filter_file('$path = ""', '$path = "%s"' % prefix.bin, "scripts/recon.pl", string=True)

    # recon's makefile is very basic -- the target directory must
    # already exist to properly install
    @run_before("install")
    def prepare_bin(self):
        mkdirp(prefix.bin)

    # finally, install the scripts dir as well
    # and link the recon command into bin.
    @run_after("install")
    def finalize(self):
        install_tree("scripts", prefix.scripts)
        symlink(join_path(prefix.scripts, "recon.pl"), join_path(prefix.bin, "recon"))
