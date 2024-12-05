# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Roary(Package):
    """Rapid large-scale prokaryote pan genome analysis"""

    homepage = "https://github.com/sanger-pathogens/Roary"
    url = "https://github.com/sanger-pathogens/Roary/archive/refs/tags/v3.13.0.tar.gz"

    license("GPL-3.0-or-later")

    version("3.13.0", sha256="375f83c8750b0f4dea5b676471e73e94f3710bc3a327ec88b59f25eae1c3a1e8")

    variant("kraken", default=False, description="Enable kraken support")

    depends_on("bedtools2", type="run")
    depends_on("blast-plus", type="run")
    depends_on("cdhit", type="run")
    depends_on("fasttree~openmp", type="run")
    depends_on("kraken", type="run", when="+kraken")
    depends_on("mafft", type="run")
    depends_on("mcl+blast", type="run")
    depends_on("parallel", type="run")
    depends_on("perl@5.8:", type="run")
    depends_on("perl-array-utils", type="run")
    depends_on("perl-bioperl", type="run")
    depends_on("perl-devel-overloadinfo", type="run")
    depends_on("perl-digest-md5-file", type="run")
    depends_on("perl-exception-class", type="run")
    depends_on("perl-file-find-rule", type="run")
    depends_on("perl-file-grep", type="run")
    depends_on("perl-file-slurper", type="run")
    depends_on("perl-file-which", type="run")
    depends_on("perl-graph-readwrite", type="run")
    depends_on("perl-graph", type="run")
    depends_on("perl-log-log4perl", type="run")
    depends_on("perl-moose", type="run")
    depends_on("perl-perlio-utf8-strict", type="run")
    depends_on("perl-text-csv", type="run")
    depends_on("perl-xml-parser", type="run")
    depends_on("perl-xml-writer", type="run")
    depends_on("prank", type="run")
    depends_on("r-ggplot2", type="run")
    depends_on("r", type="run")
    # roary2svg dependencies
    depends_on("perl-data-dumper", type="run")
    depends_on("perl-list-moreutils", type="run")
    depends_on("perl-svg", type="run")
    # roary_plots dependencies
    depends_on("python", type="run")
    depends_on("py-biopython", type="run")
    depends_on("py-numpy", type="run")
    depends_on("py-pandas", type="run")
    depends_on("py-matplotlib", type="run")
    depends_on("py-seaborn", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", join_path(prefix, "contrib", "roary2svg"))
        env.prepend_path("PATH", join_path(prefix, "contrib", "roary_plots"))
        env.prepend_path("PERL5LIB", self.prefix.lib)

    @run_after("install")
    def modify_roary_pm(self):
        with working_dir(join_path(prefix.lib, "Bio")):
            filter_file("use Bio::Perl", "use BioPerl", "Roary.pm", string=True)
