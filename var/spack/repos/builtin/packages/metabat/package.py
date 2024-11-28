# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Metabat(CMakePackage):
    """MetaBAT, an efficient tool for accurately reconstructing single
    genomes from complex microbial communities."""

    homepage = "https://bitbucket.org/berkeleylab/metabat"
    url = "https://bitbucket.org/berkeleylab/metabat/get/v2.12.1.tar.gz"

    license("BSD-3-Clause-LBNL")

    version("2.15", sha256="550487b66ec9b3bc53edf513d00c9deda594a584f53802165f037bde29b4d34e")
    version("2.14", sha256="d43d5e91afa8f2d211a913739127884669516bfbed870760597fcee2b513abe2")
    version("2.13", sha256="aa75a2b62ec9588add4c288993821bab5312a83b1259ff0d508c215133492d74")
    version(
        "2.12.1",
        sha256="e3aca0656f56f815135521360dc56667ec26af25143c3a31d645fef1a96abbc2",
        deprecated=True,
    )
    version(
        "2.11.2",
        sha256="9baf81b385e503e71792706237c308a21ff9177a3211c79057dcecf8434e9a67",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("cmake", type="build", when="@2.13:")
    depends_on("boost@1.55.0:", type=("build", "run"))

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, type=("build", "run"))
    depends_on("perl", type="run")
    depends_on("zlib-api", type="link")
    depends_on("ncurses", type="link")

    def setup_build_environment(self, env):
        env.set("BOOST_ROOT", self.spec["boost"].prefix)

    def install_args(self, spec, prefix):
        return ["PREFIX={0}".format(prefix)]

    @run_after("build")
    def fix_perl_scripts(self):
        filter_file(r"#!/usr/bin/perl", "#!/usr/bin/env perl", "aggregateBinDepths.pl")

        filter_file(r"#!/usr/bin/perl", "#!/usr/bin/env perl", "aggregateContigOverlapsByBin.pl")
