# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fleur(Package):
    """FLEUR (Full-potential Linearised augmented plane wave in EURope)
    is a code family for calculating groundstate as well as excited-state properties
    of solids within the context of density functional theory (DFT)."""

    homepage = "https://www.flapw.de/MaX-5.1"
    git = "https://iffgit.fz-juelich.de/fleur/fleur.git"

    license("MIT")

    version("develop", branch="develop")
    version("5.1", tag="MaX-R5.1", commit="a482abd9511b16412c2222e2ac1b1a303acd454b")
    version("5.0", tag="MaX-R5", commit="f2df362c3dad6ef39938807ea14e4ec4cb677723")
    version("4.0", tag="MaX-R4", commit="ea0db7877451e6240124e960c5546318c9ab3953")
    version("3.1", tag="MaX-R3.1", commit="f6288a0699604ad9e11efbfcde824b96db429404")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI support")
    variant("hdf5", default=False, description="Enable HDF5 support")
    variant("scalapack", default=False, description="Enable SCALAPACK")
    variant(
        "fft",
        default="internal",
        values=("internal", "mkl", "fftw"),
        description="Enable the use of Intel MKL FFT/FFTW provider",
    )
    variant("elpa", default=False, description="Enable ELPA support")
    variant("magma", default=False, description="Enable Magma support")
    variant("external_libxc", default=False, description="Enable external libxc support")
    variant("spfft", default=False, description="Enable spfft support")
    variant("wannier90", default=False, description="Enable wannier90 support")
    variant("openmp", default=False, description="Enable OpenMP support.")
    variant(
        "build_type",
        default="RelWithDebInfo",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    depends_on("cmake", type="build")
    depends_on("python@3:", type="build")
    depends_on("blas")
    depends_on("lapack")
    depends_on("libxml2")
    depends_on("mpi", when="+mpi")
    depends_on("intel-mkl", when="fft=mkl")
    depends_on("fftw-api", when="fft=fftw")
    depends_on("scalapack", when="+scalapack")
    depends_on("libxc", when="+external_libxc")
    depends_on("hdf5+hl+fortran", when="+hdf5")
    depends_on("magma+fortran", when="+magma")
    depends_on("wannier90", when="+wannier90")
    depends_on("spfft+fortran~openmp", when="+spfft~openmp")
    depends_on("spfft+fortran+openmp", when="+spfft+openmp")
    depends_on("elpa~openmp", when="+elpa~openmp")
    depends_on("elpa+openmp", when="+elpa+openmp")

    conflicts("%intel@:16.0.4", msg="ifort version <16.0 will most probably not work correctly")
    conflicts("%gcc@:6.3.0", msg="gfortran is known to work with versions newer than v6.3")
    conflicts(
        "%pgi@:18.4.0",
        msg="You need at least PGI version 18.4 \
                   but might still run into some problems.",
    )
    conflicts("~scalapack", when="+elpa", msg="ELPA requires scalapack support")
    conflicts("@:5.0", when="fft=fftw", msg="FFTW interface is supported from Fleur v5.0")
    conflicts("@:5.0", when="+wannier90", msg="wannier90 is supported from Fleur v5.0")
    conflicts("@:4.0", when="+spfft", msg="SpFFT is supported from Fleur v4.0")
    conflicts("@:4.0", when="+external_libxc", msg="External libxc is supported from Fleur v4.0")

    def setup_build_environment(self, env):
        spec = self.spec

        if spec.satisfies("+mpi"):
            env.set("CC", spec["mpi"].mpicc, force=True)
            env.set("FC", spec["mpi"].mpifc, force=True)
            env.set("CXX", spec["mpi"].mpicxx, force=True)

    @run_before("install")
    def configure(self):
        spec = self.spec
        sh = which("bash")

        options = {
            "-link": [],
            "-libdir": [],
            "-includedir": [],
            # "-flags": []
        }

        options["-link"].append(spec["blas"].libs.link_flags)
        options["-libdir"].append(spec["blas"].prefix.lib)
        options["-includedir"].append(spec["blas"].prefix.include)

        options["-link"].append(spec["lapack"].libs.link_flags)
        options["-libdir"].append(spec["lapack"].prefix.lib)
        options["-includedir"].append(spec["lapack"].prefix.include)

        options["-link"].append(spec["libxml2"].libs.link_flags)
        options["-libdir"].append(spec["libxml2"].prefix.lib)
        options["-includedir"].append(spec["libxml2"].prefix.include)
        options["-includedir"].append(join_path(spec["libxml2"].prefix.include, "libxml2"))

        if spec.satisfies("fft=mkl"):
            options["-link"].append(spec["intel-mkl"].libs.link_flags)
            options["-libdir"].append(spec["intel-mkl"].prefix.lib)
            options["-includedir"].append(spec["intel-mkl"].prefix.include)
        if spec.satisfies("fft=fftw"):
            options["-link"].append(spec["fftw-api"].libs.link_flags)
            options["-libdir"].append(spec["fftw-api"].prefix.lib)
            options["-includedir"].append(spec["fftw-api"].prefix.include)
        if spec.satisfies("+scalapack"):
            options["-link"].append(spec["scalapack"].libs.link_flags)
            options["-libdir"].append(spec["scalapack"].prefix.lib)
        if spec.satisfies("+external_libxc"):
            # Workaround: The fortran library is called libxcf90.a/so
            #    but spec['wannier90'].libs.link_flags return -lxc
            options["-link"].append("-lxcf90")
            options["-libdir"].append(spec["libxc"].prefix.lib)
            options["-includedir"].append(spec["libxc"].prefix.include)
        if spec.satisfies("+hdf5"):
            options["-link"].append(spec["hdf5"].libs.link_flags)
            options["-libdir"].append(spec["hdf5"].prefix.lib)
            options["-includedir"].append(spec["hdf5"].prefix.include)
        if spec.satisfies("+magma"):
            options["-link"].append(spec["magma"].libs.link_flags)
            options["-libdir"].append(spec["magma"].prefix.lib)
            options["-includedir"].append(spec["magma"].prefix.include)
        if spec.satisfies("+wannier90"):
            # Workaround: The library is not called wannier90.a/so
            #    for this reason spec['wannier90'].libs.link_flags fails!
            options["-link"].append("-lwannier")
            options["-libdir"].append(spec["wannier90"].prefix.lib)
        if spec.satisfies("+spfft"):
            options["-link"].append(spec["spfft"].libs.link_flags)
            # Workaround: The library is installed in /lib64 not /lib
            options["-libdir"].append(spec["spfft"].prefix.lib + "64")
            # Workaround: The library needs spfft.mod in include/spfft path
            options["-includedir"].append(join_path(spec["spfft"].prefix.include, "spfft"))
        if spec.satisfies("+elpa"):
            options["-link"].append(spec["elpa"].libs.link_flags)
            options["-libdir"].append(spec["elpa"].prefix.lib)
            # Workaround: The library needs elpa.mod in include/elpa_%VERS/modules
            options["-includedir"].append(spec["elpa"].prefix.include)
            options["-includedir"].append(spec["elpa"].headers.include_flags[2:])
            options["-includedir"].append(
                join_path(spec["elpa"].headers.include_flags[2:], "modules")
            )

        args = []
        args.append("-link")
        args.append(" ".join(options["-link"]))
        args.append("-libdir")
        args.append(" ".join(options["-libdir"]))
        args.append("-includedir")
        args.append(" ".join(options["-includedir"]))

        sh("configure.sh", *args)

    def install(self, spec, prefix):
        with working_dir("build"):
            make()
            mkdirp(prefix.bin)
            if spec.satisfies("+mpi"):
                install("fleur_MPI", prefix.bin)
            else:
                install("fleur", prefix.bin)
            install("inpgen", prefix.bin)
