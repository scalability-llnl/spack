# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.filesystem as fs
import llnl.util.tty as tty

from spack.package import *


class Octopus(AutotoolsPackage, CudaPackage):
    """A real-space finite-difference (time-dependent) density-functional
    theory code."""

    homepage = "https://octopus-code.org/"
    url = "https://octopus-code.org/download/6.0/octopus-6.0.tar.gz"
    git = "https://gitlab.com/octopus-code/octopus"

    maintainers("fangohr", "RemiLacroix-IDRIS", "iamashwin99")

    license("Apache-2.0")

    version("14.1", sha256="6955f4020e69f038650a24509ff19ef35de4fd34e181539f92fa432db9b66ca7")
    version("14.0", sha256="3cf6ef571ff97cc2c226016815d2ac4aa1e00ae3fb0cc693e0aff5620b80373e")
    version("13.0", sha256="b4d0fd496c31a9c4aa4677360e631765049373131e61f396b00048235057aeb1")
    version("12.2", sha256="e919e07703696eadb4ba59352d7a2678a9191b4586cb9da538661615e765a5a2")
    version("12.1", sha256="e2214e958f1e9631dbe6bf020c39f1fe4d71ab0b6118ea9bd8dc38f6d7a7959a")
    version("12.0", sha256="70beaf08573d394a766f10346a708219b355ad725642126065d12596afbc0dcc")
    version("11.4", sha256="73bb872bff8165ddd8efc5b891f767cb3fe575b5a4b518416c834450a4492da7")
    version("11.3", sha256="0c98417071b5e38ba6cbdd409adf917837c387a010e321c0a7f94d9bd9478930")
    version("11.1", sha256="d943cc2419ca409dda7459b7622987029f2af89984d0d5f39a6b464c3fc266da")
    version("10.5", sha256="deb92e3491b0c6ac5736960d075b44cab466f528b69715ed44968ecfe2953ec4")
    version("10.4", sha256="4de9dc6f5815a45e43320e4abc7ef3e501e34bc327441376ea20ca1a992bdb72")
    version("10.3", sha256="4633490e21593b51b60a8391b8aa0ed17fa52a3a0030630de123b67a41f88b33")
    version("10.2", sha256="393e2ba7b18af1b736ad6deb339ba0cef18c6417671da7a6f1fcc3a5d8f7586b")
    version("10.1", sha256="b6a660a99ed593c1d491e2d11cfff9ce87f0d80d527d9ff47fd983533d45adc6")
    version("10.0", sha256="ccf62200e3f37911bfff6d127ebe74220996e9c09383a10b1420c81d931dcf23")
    version("7.3", sha256="ad843d49d4beeed63e8b9a2ca6bfb2f4c5a421f13a4f66dc7b02f6d6a5c4d742")
    version("6.0", sha256="4a802ee86c1e06846aa7fa317bd2216c6170871632c9e03d020d7970a08a8198")
    version("5.0.1", sha256="3423049729e03f25512b1b315d9d62691cd0a6bd2722c7373a61d51bfbee14e0")

    version("develop", branch="main")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Build with MPI support")
    variant("scalapack", default=False, when="+mpi", description="Compile with Scalapack")
    variant("berkeleygw", default=False, description="Compile with BerkeleyGW")
    variant("metis", default=False, description="Compile with METIS")
    variant("parmetis", default=False, when="+mpi", description="Compile with ParMETIS")
    variant("netcdf", default=False, description="Compile with Netcdf")
    variant(
        "sparskit",
        default=False,
        description="Compile with Sparskit - A Basic Tool Kit for Sparse Matrix Computations",
    )
    variant("arpack", default=False, description="Compile with ARPACK")
    variant("cgal", default=False, description="Compile with CGAL library support")
    variant("pfft", default=False, when="+mpi", description="Compile with PFFT")
    variant(
        "nfft",
        default=False,
        description="Compile with NFFT - Nonequispaced Fast Fourier Transform library",
    )
    # poke here refers to https://gitlab.e-cam2020.eu/esl/poke
    # variant('poke', default=False,
    #         description='Compile with poke (not available in spack yet)')
    variant("python", default=False, description="Activates Python support")
    variant("likwid", default=False, description="Compile with likwid")
    variant("libvdwxc", default=False, description="Compile with libvdwxc")
    variant("libyaml", default=False, description="Compile with libyaml")
    variant("elpa", default=False, description="Compile with ELPA")
    variant("etsf-io", default=False, description="Compile with etsf-io")
    variant("nlopt", default=False, description="Compile with nlopt")
    variant(
        "pnfft",
        default=False,
        when="+pfft",
        description="Compile with PNFFT - Parallel Nonequispaced FFT library",
    )
    variant("debug", default=False, description="Compile with debug flags")

    depends_on("autoconf", type="build", when="@develop")
    depends_on("automake", type="build", when="@develop")
    depends_on("libtool", type="build", when="@develop")
    depends_on("m4", type="build", when="@develop")
    depends_on("mpi", when="+mpi")

    depends_on("blas")
    depends_on("gsl@1.9:")
    depends_on("lapack")

    # The library of exchange and correlation functionals.
    depends_on("libxc@2:2", when="@:5")
    depends_on("libxc@2:3", when="@6:7")
    depends_on("libxc@2:4", when="@8:9")
    depends_on("libxc@5.1.0:", when="@10:")
    depends_on("libxc@5.1.0:", when="@develop")
    depends_on("netcdf-fortran", when="+netcdf")  # NetCDF fortran lib without mpi variant
    with when("+mpi"):  # list all the parallel dependencies
        depends_on("fftw@3:+mpi+openmp", when="@8:9")  # FFT library
        depends_on("fftw-api@3:", when="@10:")
        depends_on("fftw+mpi+openmp", when="^[virtuals=fftw-api] fftw")
        depends_on("libvdwxc+mpi", when="+libvdwxc")
        depends_on("arpack-ng+mpi", when="+arpack")
        depends_on("elpa+mpi", when="+elpa")
        depends_on("netcdf-c+mpi", when="+netcdf")  # Link dependency of NetCDF fortran lib
        with when("+berkeleygw"):
            # From octopus@14:, upstream switched support from BerkeleyGW@2.1 to @3.0:
            # see https://gitlab.com/octopus-code/octopus/-/merge_requests/2257
            # BerkeleyGW 2.1 is the last supported version until octopus@14
            depends_on("berkeleygw@3:+mpi", when="@14:")
            depends_on("berkeleygw@2.1+mpi", when="@:13")

    with when("~mpi"):  # list all the serial dependencies
        depends_on("fftw@3:+openmp~mpi", when="@8:9")  # FFT library
        depends_on("fftw-api@3:", when="@10:")
        depends_on("fftw~mpi+openmp", when="^[virtuals=fftw-api] fftw")
        depends_on("libvdwxc~mpi", when="+libvdwxc")
        depends_on("arpack-ng~mpi", when="+arpack")
        depends_on("elpa~mpi", when="+elpa")
        depends_on("netcdf-c~~mpi", when="+netcdf")  # Link dependency of NetCDF fortran lib
        with when("+berkeleygw"):
            depends_on("berkeleygw@3:~~mpi", when="@14:")
            depends_on("berkeleygw@2.1~~mpi", when="@:13")

    depends_on("etsf-io", when="+etsf-io")
    depends_on("py-numpy", when="+python")
    depends_on("py-mpi4py", when="+python")
    depends_on("metis@5:+int64", when="+metis")
    depends_on("parmetis+int64", when="+parmetis")
    depends_on("scalapack", when="+scalapack")
    depends_on("sparskit", when="+sparskit")
    depends_on("cgal", when="+cgal")
    depends_on("pfft", when="+pfft")
    depends_on("nfft@3.2.4", when="+nfft")
    depends_on("likwid", when="+likwid")
    depends_on("libyaml", when="+libyaml")
    depends_on("pnfft", when="+pnfft")
    depends_on("nlopt", when="+nlopt")

    # optional dependencies:
    # TODO: etsf-io, sparskit,
    # feast, libfm, pfft, isf, pnfft, poke

    def configure_args(self):
        spec = self.spec
        lapack = spec["lapack"].libs
        blas = spec["blas"].libs
        args = []
        args.extend(
            [
                "--prefix=%s" % prefix,
                "--with-blas=%s" % blas.ld_flags,
                "--with-lapack=%s" % lapack.ld_flags,
                "--with-gsl-prefix=%s" % spec["gsl"].prefix,
                "--with-libxc-prefix=%s" % spec["libxc"].prefix,
                "--enable-openmp",
            ]
        )
        if "+mpi" in self.spec:  # we build with MPI
            args.extend(
                [
                    "--enable-mpi",
                    "CC=%s" % self.spec["mpi"].mpicc,
                    "FC=%s" % self.spec["mpi"].mpifc,
                ]
            )
        else:
            args.extend(["CC=%s" % self.compiler.cc, "FC=%s" % self.compiler.fc])

        if "^fftw" in spec:
            args.append("--with-fftw-prefix=%s" % spec["fftw"].prefix)
        elif spec["fftw-api"].name in INTEL_MATH_LIBRARIES:
            # As of version 10.0, Octopus depends on fftw-api instead
            # of FFTW. If FFTW is not in the dependency tree, then
            # it ought to be MKL as it is currently the only providers
            # available for fftw-api.
            args.append("FCFLAGS_FFTW=-I%s" % spec["mkl"].prefix.include.fftw)
        else:
            # To be foolproof, fail with a proper error message
            # if neither FFTW nor MKL are in the dependency tree.
            tty.die(
                'Unsupported "fftw-api" provider, '
                "currently only FFTW and MKL are supported.\n"
                "Please report this issue on Spack's repository."
            )
        if "+metis" in spec:
            args.append("--with-metis-prefix=%s" % spec["metis"].prefix)
        if "+parmetis" in spec:
            args.append("--with-parmetis-prefix=%s" % spec["parmetis"].prefix)
        if "+netcdf" in spec:
            args.extend(
                [
                    "--with-netcdf-prefix=%s" % spec["netcdf-fortran"].prefix,
                    "--with-netcdf-include=%s" % spec["netcdf-fortran"].prefix.include,
                ]
            )
        if "+arpack" in spec:
            arpack_libs = spec["arpack-ng"].libs.joined()
            args.append("--with-arpack={0}".format(arpack_libs))
            if "+mpi" in spec["arpack-ng"]:
                args.append("--with-parpack={0}".format(arpack_libs))

        if "+scalapack" in spec:
            args.extend(
                [
                    f"--with-blacs={spec['scalapack'].libs.ld_flags}",
                    f"--with-scalapack={spec['scalapack'].libs.ld_flags}",
                ]
            )

        if "+cgal" in spec:
            # Boost is a dependency of CGAL, and is not picked up by the configure script
            # unless specified explicitly with `--with-boost` option.
            args.append("--with-cgal-prefix=%s" % spec["cgal"].prefix)
            args.append("--with-boost=%s" % spec["boost"].prefix)

        if "+likwid" in spec:
            args.append("--with-likwid-prefix=%s" % spec["likwid"].prefix)

        if "+pfft" in spec:
            args.append("--with-pfft-prefix=%s" % spec["pfft"].prefix)

        if "+nfft" in spec:
            args.append("--with-nfft=%s" % spec["nfft"].prefix)

        # if '+poke' in spec:
        #     args.extend([
        #         '--with-poke-prefix=%s' % spec['poke'].prefix,
        #     ])
        if "+pnfft" in spec:
            args.append("--with-pnfft-prefix=%s" % spec["pnfft"].prefix)

        if "+libvdwxc" in spec:
            args.append("--with-libvdwxc-prefix=%s" % spec["libvdwxc"].prefix)

        if "+libyaml" in spec:
            args.append("--with-libyaml-prefix=%s" % spec["libyaml"].prefix)

        if "+elpa" in spec:
            args.append("--with-elpa-prefix=%s" % spec["elpa"].prefix)

        if "+nlopt" in spec:
            args.append("--with-nlopt-prefix=%s" % spec["nlopt"].prefix)

        if "+cuda" in spec:
            args.append("--enable-cuda")

        if "+python" in spec:
            args.append("--enable-python")

        if "+sparskit" in spec:
            args.append(
                "--with-sparskit=%s" % os.path.join(self.spec["sparskit"].prefix.lib, "libskit.a")
            )
        if "+etsf-io" in spec:
            args.append("--with-etsf-io-prefix=%s" % spec["etsf-io"].prefix)
        # --with-pfft-prefix=${prefix} --with-mpifftw-prefix=${prefix}
        # --with-berkeleygw-prefix=${prefix}
        if "+berkeleygw" in spec:
            args.append("--with-berkeleygw-prefix=%s" % spec["berkeleygw"].prefix)

        # When preprocessor expands macros (i.e. CFLAGS) defined as quoted
        # strings the result may be > 132 chars and is terminated.
        # This will look to a compiler as an Unterminated character constant
        # and produce Line truncated errors. To overcome this, add flags to
        # let compiler know that the entire line is meaningful.
        # TODO: For the lack of better approach, assume that clang is mixed
        # with GNU fortran.
        if spec.satisfies("%apple-clang") or spec.satisfies("%clang") or spec.satisfies("%gcc"):
            # In case of GCC version 10, we will have errors because of
            # argument mismatching. Need to provide a flag to turn this into a
            # warning and build sucessfully
            # We can disable variable tracking at assignments introduced in GCC10
            # for debug variant to decrease compile time.

            # Set optimization level for all flags
            opt_level = "-O2"
            fcflags = f"FCFLAGS={opt_level} -ffree-line-length-none"
            cxxflags = f"CXXFLAGS={opt_level}"
            cflags = f"CFLAGS={opt_level}"

            # Add extra flags for gcc 10 or higher
            gcc10_extra = (
                "-fallow-argument-mismatch -fallow-invalid-boz"
                if spec.satisfies("%gcc@10:")
                else ""
            )
            # Add debug flag if needed
            if spec.satisfies("+debug"):
                fcflags += " -g"
                cxxflags += " -g"
                cflags += " -g"
                gcc10_extra += (
                    "-fno-var-tracking-assignments" if spec.satisfies("%gcc@10:") else ""
                )

            args.append(f"{fcflags} {gcc10_extra}")
            args.append(f"{cxxflags} {gcc10_extra}")
            args.append(f"{cflags} {gcc10_extra}")

        # for octopus 14.1 and above autotools is deprecated in favour of cmake
        # inorder to continue using autotools we pass `--enable-silent-deprecation`
        if spec.satisfies("@14.1:"):
            args.append("--enable-silent-deprecation")

        # Disable flags
        #
        # disable gdlib explicitly to avoid
        # autotools picking gdlib up from the system
        args.append("--disable-gdlib")

        return args

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def benchmark_tests_after_install(self):
        """Function stub to run tests after install if desired
        (for example through `spack install --test=root octopus`)
        """
        self.test_version()
        self.test_example()
        self.test_he()

    def test_version(self):
        """Check octopus can execute (--version)"""
        # Example output:
        #
        # spack-v0.17.2$ octopus --version
        # octopus 11.3 (git commit )

        exe = which(self.spec.prefix.bin.octopus)
        out = exe("--version", output=str.split, error=str.split)
        assert "octopus " in out

    def test_recipe(self):
        """run recipe example"""

        # Octopus expects a file with name `inp` in the current working
        # directory to read configuration information for a simulation run from
        # that file. We copy the relevant configuration file in a dedicated
        # subfolder for the test.
        #
        # As we like to be able to run these tests also with the
        # `spack install --test=root` command, we cannot rely on
        # self.test_suite.current_test_data_dir, and need to copy the test
        # input files manually (see below).

        expected = [
            "Running octopus",
            "CalculationMode = recipe",
            "DISCLAIMER: The authors do not " "guarantee that the implementation",
            "recipe leads to an edible dish, " 'for it is clearly "system-dependent".',
            "Calculation ended on",
        ]

        with working_dir("example-recipe", create=True):
            print("Current working directory (in example-recipe)")
            fs.copy(join_path(os.path.dirname(__file__), "test", "recipe.inp"), "inp")
            exe = which(self.spec.prefix.bin.octopus)
            out = exe(output=str.split, error=str.split)
            check_outputs(expected, out)

    def test_he(self):
        """run He example"""

        # Octopus expects a file with name `inp` in the current working
        # directory to read configuration information for a simulation run from
        # that file. We copy the relevant configuration file in a dedicated
        # subfolder for the test.
        #
        # As we like to be able to run these tests also with the
        # `spack install --test=root` command, we cannot rely on
        # self.test_suite.current_test_data_dir, and need to copy the test
        # input files manually (see below).

        expected = [
            "Running octopus",
            "Info: Starting calculation mode.",
            "CalculationMode = gs",
            """Species "helium" is a user-defined potential.""",
            "Info: Writing states.",
            "Calculation ended on",
        ]

        with working_dir("example-he", create=True):
            print("Current working directory (in example-he)")
            fs.copy(join_path(os.path.dirname(__file__), "test", "he.inp"), "inp")
            exe = which(self.spec.prefix.bin.octopus)
            out = exe(output=str.split, error=str.split)
            check_outputs(expected, out)
