# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Meraculous(CMakePackage, SourceforgePackage):
    """Meraculous is a while genome assembler for Next Generation Sequencing
    data geared for large genomes."""

    homepage = "http://jgi.doe.gov/data-and-tools/meraculous/"
    sourceforge_mirror_path = "meraculous20/Meraculous-v2.2.4.tar.gz"
    git = "https://bitbucket.org/berkeleylab/genomics-meraculous2.git"

    license("BSD-3-Clause-LBNL")

    version("2.2.5.1", branch="release-2.2.5.1")
    version("2.2.4", sha256="3b4b8848232be902af9ebc77b38b83bcc531f12120115be089bdd6371ad2bf5b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("perl", type=("build", "run"))
    depends_on("boost@1.5.0:")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("gnuplot@3.7:")
    depends_on("perl-log-log4perl", type=("build", "run"))

    conflicts("%gcc@6.0.0:", when="@2.2.4")

    def patch(self):
        edit = FileFilter("CMakeLists.txt")
        edit.filter(r"-static-libstdc\+\+", "")

    def setup_run_environment(self, env):
        env.set("MERACULOUS_ROOT", self.prefix)
        env.prepend_path("PERL5LIB", self.prefix.lib)
