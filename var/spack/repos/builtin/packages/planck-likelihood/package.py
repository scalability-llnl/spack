# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PlanckLikelihood(Package):
    """2015 Cosmic Microwave Background (CMB) spectra and likelihood code"""

    homepage = (
        "https://wiki.cosmos.esa.int/planckpla2015/index.php/CMB_spectrum_%26_Likelihood_Code"
    )
    url = "https://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Code-v2.0.R2.00.tar.bz2"

    version(
        "2.00",
        sha256="c1efa208175b2751e75b2ad1c026dae744a7dd279eb74baa5db3098bc9c971bb",
        url="https://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Code-v2.0.R2.00.tar.bz2",
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("lensing-ext", default=False, description="Provide lensing-ext data")
    variant("plik-DS", default=False, description="Provide plik-DS data")
    variant("plik-HM-ext", default=False, description="Provide plik-HM-ext data")
    variant("plik-unbinned", default=False, description="Provide plik-unbinned data")

    patch("fortran.patch")
    patch("make.patch")
    patch("arm.patch", when="target=aarch64:")

    resource(
        name="baseline",
        url="https://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-baseline_R2.00.tar.gz",
        sha256="7c62c5afc105bff28c2da3eddb870b8180536d30e31c4d419b307ad3996e17ab",
        destination=".",
    )
    resource(
        name="lensing-ext",
        url="https://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-extra-lensing-ext.R2.00.tar.gz",
        sha256="0c017984bfd12315b94958f48f8e61e625361a84066838976f676fb5c2e76dbc",
        destination=".",
        when="+lensing-ext",
    )
    resource(
        name="plik-DS",
        url="https://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-extra-plik-DS.R2.00.tar.gz",
        sha256="f6b5ec6b284ea71008f071503faf8319dac48c3ea7fb13f5e5cbd23fff3efd84",
        destination=".",
        when="+plik-DS",
    )
    resource(
        name="plik-HM-ext",
        url="https://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-extra-plik-HM-ext.R2.00.tar.gz",
        sha256="b5b8ead297b31f9b2e4913b54b1d3bbe272075f85ce2ca9bf5d99dbbe1559f77",
        destination=".",
        when="+plik-HM-ext",
    )
    resource(
        name="plik-unbinned",
        url="https://irsa.ipac.caltech.edu/data/Planck/release_2/software/COM_Likelihood_Data-extra-plik-unbinned.R2.00.tar.gz",
        sha256="69cdfee40d63a8b60b1f715d4e276d76693ec1a6f1b2658abac2b8d7dff4fa44",
        destination=".",
        when="+plik-unbinned",
    )

    depends_on("blas")
    depends_on("cfitsio +shared")
    depends_on("lapack")

    # Note: Could also install Python bindings

    parallel = False

    def install(self, spec, prefix):
        # Configure

        # Don't hide build commands
        filter_file("^\t@", "\t", "Makefile")

        makeflags = [
            f"PREFIX={prefix}",
            "COLORS=0",
            f"CFITSIOPATH={spec['cfitsio'].prefix}",
            "CC=cc",
            "FC=fc",
            "IFORTLIBPATH=",
            "IFORTRUNTIME=-lintlc -limf -lsvml -liomp5 -lifportmt -lifcoremt",
            "GFORTRANLIBPATH=",
            "GFORTRANRUNTIME=-lgfortran -lgomp",
            "LAPACKLIBPATH=",
            f"LAPACK={(spec['lapack'].libs + spec['blas'].libs).ld_flags}",
            f"COPENMP={self.compiler.openmp_flag}",
            f"FOPENMP={self.compiler.openmp_flag}",
        ]

        # Build
        make(*makeflags)

        # Install
        make("install", *makeflags)
        fix_darwin_install_name(prefix.lib)
        dirs = ["plc_2.0"]
        if "+lensing-ext" in spec:
            dirs.append("lensing_ext")
        if "+plik-DS" in spec:
            dirs.append("plik_DS")
        if "+plik-HM-ext" in spec:
            dirs.append("plik_HM_ext")
        if "+plik-unbinned" in spec:
            dirs.append("plik_unbinned")
        for dir in dirs:
            install_tree(dir, join_path(prefix, "share", "clik", dir))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("CLIK_PATH", self.prefix)
        env.set("CLIK_DATA", self.prefix.share.clik)
        env.set("CLIK_PLUGIN", "rel2015")

    def setup_run_environment(self, env):
        env.set("CLIK_PATH", self.prefix)
        env.set("CLIK_DATA", self.prefix.share.clik)
        env.set("CLIK_PLUGIN", "rel2015")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        prefix = self.prefix
        clik_example_c = Executable(join_path(prefix.bin, "clik_example_C"))
        with working_dir("spack-check", create=True):
            clik_example_c(
                join_path(
                    prefix,
                    "share",
                    "clik",
                    "plc_2.0",
                    "hi_l",
                    "plik",
                    "plik_dx11dr2_HM_v18_TT.clik",
                )
            )
