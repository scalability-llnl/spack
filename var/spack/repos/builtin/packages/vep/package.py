# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vep(Package):
    """
    Ensembl Variant Effect Predictor (VEP) determines the effect of your variants
    (SNPs, insertions, deletions, CNVs or structural variants) on genes, transcripts,
    and protein sequence, as well as regulatory regions.
    (Requires addtional data available via the `vep-cache` package)
    """

    homepage = "https://useast.ensembl.org/info/docs/tools/vep/index.html"
    url = "https://github.com/Ensembl/ensembl-vep/archive/release/111.zip"

    maintainers("teaguesterling")

    license("APACHE-2.0", checked_by="teaguesterling")

    version("112.0", sha256="46dd08838fd94ecbfaa931266c78570748a3cb39668b6e43c3608e6cd0aff93f")
    version("111.0", sha256="9cb326a1fa0054ce1a417f8fd4f2325ba605c40ec10eefbf87f461c264a89407")
    version("110.0", sha256="391a1fe50139064c1044c09e013bb21437933d677537b5d3336807f3b131fb51")

    variant("vep_installer", default=False, description="Install dependencies with VEP installer")
    variant("utility_scripts", default=True, description="Install utility scripts")

    # Optional dependencies
    variant("json", default=True, description="Include requirements for JSON support")
    variant("nearest", default=True, description="Include requirements for 'nearest'")
    variant("gzip", default=True, description="Include requirements for gzip support")

    # Bundled versions
    variant("bundled_bioperl", default=False, description="Build with bundled BioPerl")
    variant("bundled_htslib", default=False, description="Build with bundled HTSLib")

    extends("perl")

    with default_args(type="build"):
        depends_on("gcc", when="+vep_installer")
        depends_on("gmake")

    with default_args(type=("build", "run")):
        depends_on("perl@5.10:")
        depends_on("perl-archive-zip")
        depends_on("perl-dbd-mysql")
        depends_on("perl-dbi")
        depends_on("perl-bio-db-hts")
        depends_on("perl-json", when="+json")
        depends_on("perl-set-intervaltree", when="+nearest")
        depends_on("perl-perlio-gzip", when="+gzip")
        depends_on("perl-bioperl@1.6:", when="~bundled_bioperl")
        depends_on("htslib@1.9:", when="~bundled_htslib")

    # This is a workaround for the VEP installer which downloads
    # and manually installs dependent packages
    with default_args(type=("build", "run"), when="~vep_installer"):
        for ver in ["110", "111", "112"]:
            depends_on(f"perl-bio-ensembl@{ver}", when=f"@{ver}")
            depends_on(f"perl-bio-ensembl-variation@{ver}", when=f"@{ver}")
            depends_on(f"perl-bio-ensembl-funcgen@{ver}", when=f"@{ver}")
            depends_on(f"perl-bio-ensembl-io@{ver}", when=f"@{ver}")

    # These should probably move futher up the dependency stack
    conflicts("zlib-ng", when="+gzip")
    conflicts("zlib-ng", when="+bundled_htslib")

    @property
    def vep_lib_path(self):
        return self.prefix.lib.perl5

    @property
    def vep_share_path(self):
        return self.prefix.share.vep

    @property
    def vep_scripts_path(self):
        return self.vep_share_path.scripts

    @property
    def vep_installer_path(self):
        return f"{self.vep_scripts_path.INSTALL}.pl"

    def setup_run_environment(self, env):
        env.set("VEP_HOME", self.home)
        if self.spec.satisfies("+bundled_htslib"):
            env.prepend_path("PATH", self.vep_lib_path.htslib)

    def installer_args(self):
        auto = "a"
        args = ["--DESTDIR", f"{self.vep_lib_path}", "--NO_UPDATE", "--NO_TEST"]
        if self.spec.satisfies("~bundled_htslib"):
            args += ["--NO_HTSLIB"]
        if self.spec.satisfies("~bundled_bioperl"):
            args += ["--NO_BIOPERL"]
        args += ["--AUTO", auto]
        return args

    def install(self, spec, prefix):
        mkdirp(self.prefix.bin)
        mkdirp(self.vep_lib_path)
        mkdirp(self.vep_share_path)
        mkdirp(self.vep_scripts_path)

        # Add the VEP perl modules and executable
        install_tree("modules", self.vep_lib_path)
        install("vep", prefix.bin.vep)

        # We save this so it can be used later to update caches
        # and use to do the rest of the install, if requested
        install("INSTALL.pl", self.vep_installer_path)

        # This is required for any cache updating via the installer
        install("convert_cache.pl", self.vep_scripts_path)

        # Resolve dependencies via VEP installer if desired
        if spec.satisfies("+vep_installer"):
            # If we don't do this a bunch of perl libs will be missing
            # Run the customer VEP installer/downloader, which downloads
            # copies a bunch of additional perl modules
            installer = which(self.vep_installer_path)
            installer(*self.installer_args())

        # Manually install auxilary scripts if requested
        if self.spec.satisfies("+utility_scripts"):
            install("filter_vep", prefix.bin.filter_vep)
            install("haplo", prefix.bin.haplo)
            install("variant_recoder", prefix.bin.variant_recoder)
