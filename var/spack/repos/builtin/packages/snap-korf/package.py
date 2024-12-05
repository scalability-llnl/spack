# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SnapKorf(MakefilePackage):
    """SNAP is a general purpose gene finding program suitable for both
    eukaryotic and prokaryotic genomes."""

    homepage = "http://korflab.ucdavis.edu/software.html"
    url = "http://korflab.ucdavis.edu/Software/snap-2013-11-29.tar.gz"
    git = "https://github.com/KorfLab/SNAP.git"

    license("MIT")

    version("2021-11-04", commit="62ff3120fceccb03b5eea9d21afec3167dedfa94")
    version(
        "2013-11-29", sha256="e2a236392d718376356fa743aa49a987aeacd660c6979cee67121e23aeffc66a"
    )

    depends_on("c", type="build")  # generated

    depends_on("perl", type=("build", "run"))

    def edit(self, spec, prefix):
        if spec.satisfies("@2013-11-29%gcc@6:"):
            rstr = "\\1 -Wno-tautological-compare -Wno-misleading-indentation"
            filter_file("(-Werror)", rstr, "Zoe/Makefile")
            rstr = "\\1 -Wno-error=format-overflow -Wno-misleading-indentation"
            filter_file("(-Werror)", rstr, "Makefile")

        filter_file(r"(^const char \* zoeFunction;)", "extern \\1", "Zoe/zoeTools.h")
        filter_file(r"(^const char \* zoeConstructor;)", "extern \\1", "Zoe/zoeTools.h")
        filter_file(r"(^const char \* zoeMethod;)", "extern \\1", "Zoe/zoeTools.h")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        progs = ["snap", "fathom", "forge"]
        if spec.satisfies("@2013-11-29"):
            progs = progs + ["depend", "exonpairs", "hmm-info"]
        for p in progs:
            install(p, prefix.bin)

        install("*.pl", prefix.bin)

        install_tree("Zoe", prefix.Zoe)
        install_tree("HMM", prefix.HMM)
        install_tree("DNA", prefix.DNA)

    def setup_run_environment(self, env):
        env.set("ZOE", self.prefix)
        env.prepend_path("PATH", self.prefix)
