# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Breakdancer(CMakePackage):
    """BreakDancer-1.3.6, released under GPLv3, is a perl/Cpp package that
    provides genome-wide detection of structural variants from next generation
    paired-end sequencing reads. It includes two complementary programs.
    BreakDancerMax predicts five types of structural variants: insertions,
    deletions, inversions, inter- and intra-chromosomal translocations from
    next-generation short paired-end sequencing reads using read pairs that are
    mapped with unexpected separation distances or orientation.
    BreakDancerMini focuses on detecting small indels (usually between 10bp and
    100bp) using normally mapped read pairs.."""

    homepage = "https://gmt.genome.wustl.edu/packages/breakdancer"
    url = "https://github.com/genome/breakdancer/archive/v1.4.5.tar.gz"

    version("1.4.5", sha256="5d74f3a90f5c69026ebb4cf4cb9ccc51ec8dd49ac7a88595a1efabd5a73e92b6")
    version(
        "master",
        submodules="true",
        git="https://github.com/genome/breakdancer.git",
        preferred=True,
    )

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")

    depends_on("ncurses", type="link")

    depends_on("perl-statistics-descriptive", type="run")
    depends_on("perl-math-cdf", type="run")
    depends_on("perl-gdgraph", type="run")
    depends_on("perl-gdgraph-histogram", type="run")
    depends_on("perl-list-moreutils", type="run")
    depends_on("perl-exporter-tiny", type="run")

    # TODO: remove git submodules, and depend on boost & samtools

    parallel = False

    def setup_run_environment(self, env):
        # get the perl tools in the path
        env.prepend_path("PATH", self.prefix.lib)

    @run_before("cmake")
    def edit(self):
        # perl tools end up in a silly lib subdirectory, fixing that
        filter_file(
            r"set\(SUPPORT_LIBDIR lib\/breakdancer-max\$ \
                    \{EXE_VERSION_SUFFIX\}\)",
            "set(SUPPORT_LIBDIR lib)",
            join_path(self.stage.source_path, "perl", "CMakeLists.txt"),
        )
