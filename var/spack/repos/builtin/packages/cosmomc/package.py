# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import fnmatch
import os

from spack.package import *


class Cosmomc(Package):
    """CosmoMC is a Fortran 2008 Markov-Chain Monte-Carlo (MCMC) engine
    for exploring cosmological parameter space, together with
    Fortran and python code for analysing Monte-Carlo samples and
    importance sampling (plus a suite of scripts for building grids
    of runs, plotting and presenting results)."""

    homepage = "https://cosmologist.info/cosmomc/"
    url = "https://github.com/cmbant/CosmoMC/archive/Nov2016.tar.gz"

    version("2016.11", sha256="b83edbf043ff83a4dde9bc14c56a09737dbc41ffe247a8e9c9a26892ed8745ba")
    version("2016.06", sha256="23fa23eef40846c17d3740be63a7fefde13880cbb81545a44d14034277d9ffc0")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    def url_for_version(self, version):
        names = {"2016.11": "Nov2016", "2016.06": "June2016"}
        return "https://github.com/cmbant/CosmoMC/archive/%s.tar.gz" % names[str(version)]

    variant("mpi", default=True, description="Enable MPI support")
    variant("planck", default=False, description="Enable Planck Likelihood code and baseline data")
    variant("python", default=True, description="Enable Python bindings")

    extends("python", when="+python")

    depends_on("mpi", when="+mpi")
    depends_on("planck-likelihood", when="+planck")
    depends_on("py-matplotlib", type=("build", "run"), when="+python")
    depends_on("py-numpy", type=("build", "run"), when="+python")
    depends_on("py-pandas", type=("build", "run"), when="+python")
    depends_on("py-scipy", type=("build", "run"), when="+python")
    depends_on("py-six", type=("build", "run"), when="+python")
    depends_on("python @2.7:2,3.4:", type=("build", "run"), when="+python")

    patch("Makefile.patch")
    patch("errorstop.patch")

    parallel = False

    def install(self, spec, prefix):
        # Clean up environment to avoid configure problems
        os.environ.pop("LINKMPI", "")
        os.environ.pop("NERSC_HOST", "")
        os.environ.pop("NONCLIKLIKE", "")
        os.environ.pop("PICO", "")
        os.environ.pop("PRECISION", "")
        os.environ.pop("RECOMBINATION", "")
        os.environ.pop("WMAP", "")

        # Set up Planck data if requested
        clikdir = join_path("data", "clik")
        try:
            os.remove(clikdir)
        except OSError:
            pass
        if spec.satisfies("+planck"):
            os.symlink(join_path(os.environ["CLIK_DATA"], "plc_2.0"), clikdir)
        else:
            os.environ.pop("CLIK_DATA", "")
            os.environ.pop("CLIK_PATH", "")
            os.environ.pop("CLIK_PLUGIN", "")

        # Choose compiler
        # Note: Instead of checking the compiler vendor, we should
        # rewrite the Makefile to use Spack's options all the time
        if spec.satisfies("%gcc"):
            if not spec.satisfies("%gcc@6:"):
                raise InstallError(
                    "When using GCC, " "CosmoMC requires version gcc@6: for building"
                )
            choosecomp = "ifortErr=1"  # choose gfortran
        elif spec.satisfies("%intel"):
            if not spec.satifies("%intel@14:"):
                raise InstallError(
                    "When using the Intel compiler, "
                    "CosmoMC requires version intel@14: for building"
                )
            choosecomp = "ifortErr=0"  # choose ifort
        else:
            raise InstallError("Only GCC and Intel compilers are supported")

        # Configure MPI
        if spec.satisfies("+mpi"):
            wantmpi = "BUILD=MPI"
            mpif90 = "MPIF90C=%s" % spec["mpi"].mpifc
        else:
            wantmpi = "BUILD=NOMPI"
            mpif90 = "MPIF90C="

        # Choose BLAS and LAPACK
        lapack = "LAPACKL=%s" % (spec["lapack"].libs + spec["blas"].libs).ld_flags

        # Build
        make(choosecomp, wantmpi, mpif90, lapack)

        # Install
        mkdirp(prefix.bin)
        install("cosmomc", prefix.bin)
        root = join_path(prefix.share, "cosmomc")
        mkdirp(root)
        entries = [
            "batch1",
            "batch2",
            "batch3",
            "camb",
            "chains",
            "clik_latex.paramnames",
            "clik_units.paramnames",
            "cosmomc.cbp",
            "data",
            "distgeneric.ini",
            "distparams.ini",
            "disttest.ini",
            "docs",
            "job_script",
            "job_script_MOAB",
            "job_script_SLURM",
            "paramnames",
            "params_generic.ini",
            "planck_covmats",
            "scripts",
            # don't copy 'source'
            "test.ini",
            "test_pico.ini",
            "test_planck.ini",
            "tests",
        ]
        if spec.satisfies("+python"):
            entries += ["python"]
        for entry in entries:
            if os.path.isfile(entry):
                install(entry, root)
            else:
                install_tree(entry, join_path(root, entry))
        for dirpath, dirnames, filenames in os.walk(prefix):
            for filename in fnmatch.filter(filenames, "*~"):
                os.remove(os.path.join(dirpath, filename))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        prefix = self.prefix
        spec = self.spec

        os.environ.pop("LINKMPI", "")
        os.environ.pop("NERSC_HOST", "")
        os.environ.pop("NONCLIKLIKE", "")
        os.environ.pop("PICO", "")
        os.environ.pop("PRECISION", "")
        os.environ.pop("RECOMBINATION", "")
        os.environ.pop("WMAP", "")

        os.environ.pop("COSMOMC_LOCATION", "")
        os.environ.pop("PLC_LOCATION", "")

        os.environ.pop("CLIKPATH", "")
        os.environ.pop("PLANCKLIKE", "")

        exe = spec["cosmomc"].command.path
        args = []
        if spec.satisfies("+mpi"):
            # Add mpirun prefix
            args = ["-np", "1", exe]
            exe = join_path(spec["mpi"].prefix.bin, "mpiexec")
        cosmomc = Executable(exe)
        with working_dir("spack-check", create=True):
            for entry in ["camb", "chains", "data", "paramnames", "planck_covmats"]:
                os.symlink(join_path(prefix.share, "cosmomc", entry), entry)
            inifile = join_path(prefix.share, "cosmomc", "test.ini")
            cosmomc(*(args + [inifile]))
            if spec.satisfies("+planck"):
                inifile = join_path(prefix.share, "cosmomc", "test_planck.ini")
                cosmomc(*(args + [inifile]))
