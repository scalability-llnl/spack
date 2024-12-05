# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Vasp(MakefilePackage, CudaPackage):
    """
    The Vienna Ab initio Simulation Package (VASP)
    is a computer program for atomic scale materials modelling,
    e.g. electronic structure calculations
    and quantum-mechanical molecular dynamics, from first principles.
    """

    homepage = "https://vasp.at"
    url = "file://{0}/vasp.5.4.4.pl2.tgz".format(os.getcwd())
    maintainers("snehring")
    manual_download = True

    version("6.4.3", sha256="fe30e773f2a3e909b5e0baa9654032dfbdeff7ec157bc348cee7681a7b6c24f4")
    version("6.3.2", sha256="f7595221b0f9236a324ea8afe170637a578cdd5a837cc7679e7f7812f6edf25a")
    version("6.3.0", sha256="adcf83bdfd98061016baae31616b54329563aa2739573f069dd9df19c2071ad3")
    version(
        "6.2.0",
        sha256="49e7ba351bd634bc5f5f67a8ef1e38e64e772857a1c02f602828898a84197e25",
        deprecated=True,
    )
    version(
        "6.1.1",
        sha256="e37a4dfad09d3ad0410833bcd55af6b599179a085299026992c2d8e319bf6927",
        deprecated=True,
    )
    version(
        "5.4.4.pl2",
        sha256="98f75fd75399a23d76d060a6155f4416b340a1704f256a00146f89024035bc8e",
        deprecated=True,
    )
    version(
        "5.4.4",
        sha256="5bd2449462386f01e575f9adf629c08cb03a13142806ffb6a71309ca4431cfb3",
        deprecated=True,
    )

    resource(
        name="vaspsol",
        git="https://github.com/henniggroup/VASPsol.git",
        tag="V1.0",
        when="+vaspsol",
    )

    variant("openmp", default=False, when="@6:", description="Enable openmp build")

    variant("scalapack", default=False, when="@:5", description="Enables build with SCALAPACK")

    variant("cuda", default=False, description="Enables running on Nvidia GPUs")
    variant("fftlib", default=True, when="@6.2: +openmp", description="Enables fftlib build")

    variant(
        "vaspsol",
        default=False,
        when="@:6.2",
        description="Enable VASPsol implicit solvation model\n"
        "https://github.com/henniggroup/VASPsol",
    )
    variant("shmem", default=True, description="Enable use_shmem build flag")
    variant("hdf5", default=False, when="@6.2:", description="Enabled HDF5 support")

    depends_on("rsync", type="build")
    depends_on("blas")
    depends_on("lapack")
    depends_on("fftw-api")
    depends_on("fftw+openmp", when="+openmp ^[virtuals=fftw-api] fftw")
    depends_on("amdfftw+openmp", when="+openmp ^[virtuals=fftw-api] amdfftw")
    depends_on("amdblis threads=openmp", when="+openmp ^[virtuals=blas] amdblis")
    depends_on("openblas threads=openmp", when="+openmp ^[virtuals=blas] openblas")
    depends_on("mpi", type=("build", "link", "run"))
    # fortran oddness requires the below
    depends_on("openmpi%aocc", when="%aocc ^[virtuals=mpi] openmpi")
    depends_on("openmpi%gcc", when="%gcc ^[virtuals=mpi] openmpi")
    depends_on("scalapack", when="+scalapack")
    # wiki (and makefiles) suggest scalapack is expected in 6:
    depends_on("scalapack", when="@6:")
    depends_on("nccl", when="@6.3: +cuda")
    depends_on("hdf5+fortran+mpi", when="+hdf5")
    # at the very least the nvhpc mpi seems required
    depends_on("nvhpc+mpi+lapack+blas", when="%nvhpc")

    conflicts(
        "%gcc@:8", msg="GFortran before 9.x does not support all features needed to build VASP"
    )
    conflicts("+vaspsol", when="+cuda", msg="+vaspsol only available for CPU")
    requires("%nvhpc", when="@6.3: +cuda", msg="vasp requires nvhpc to build the openacc build")
    # the mpi compiler wrappers in nvhpc assume nvhpc is the underlying compiler, seemingly
    conflicts("^[virtuals=mpi] nvhpc", when="%gcc", msg="nvhpc mpi requires nvhpc compiler")
    conflicts("^[virtuals=mpi] nvhpc", when="%aocc", msg="nvhpc mpi requires nvhpc compiler")
    conflicts(
        "cuda_arch=none", when="@6.3: +cuda", msg="CUDA arch required when building openacc port"
    )

    def edit(self, spec, prefix):
        cpp_options = [
            "-DMPI",
            "-DMPI_BLOCK=8000",
            "-Duse_collective",
            "-DCACHE_SIZE=4000",
            "-Davoidalloc",
            "-Duse_bse_te",
            "-Dtbdyn",
            "-Dfock_dblbuf",
        ]
        objects_lib = ["linpack_double.o"]
        llibs = list(self.compiler.stdcxx_libs)
        cflags = ["-fPIC", "-DAAD_"]
        fflags = ["-w"]
        incs = [spec["fftw-api"].headers.include_flags]

        if self.spec.satisfies("@6:"):
            cpp_options.append("-Dvasp6")

        llibs.extend([spec["blas"].libs.ld_flags, spec["lapack"].libs.ld_flags])

        fc = [spec["mpi"].mpifc]
        fcl = [spec["mpi"].mpifc]

        include_prefix = ""
        omp_flag = "-fopenmp"

        if spec.satisfies("+shmem"):
            cpp_options.append("-Duse_shmem")
            objects_lib.append("getshmem.o")

        if spec.satisfies("@:6.2"):
            include_prefix = "linux_"
        include_string = f"makefile.include.{include_prefix}"

        # gcc
        if spec.satisfies("%gcc"):
            include_string += "gnu"
            if spec.satisfies("+openmp"):
                include_string += "_omp"
            make_include = join_path("arch", include_string)
        # nvhpc
        elif spec.satisfies("%nvhpc"):
            qd_root = join_path(
                spec["nvhpc"].prefix,
                f"Linux_{spec['nvhpc'].target.family.name}",
                str(spec["nvhpc"].version.dotted),
                "compilers",
                "extras",
                "qd",
            )
            nvroot = join_path(spec["nvhpc"].prefix, f"Linux_{spec['nvhpc'].target.family.name}")
            if spec.satisfies("@6.3:"):
                cpp_options.extend(['-DHOST=\\"LinuxNV\\"', "-Dqd_emulate"])
            else:
                cpp_options.extend(['-DHOST=\\"LinuxPGI\\"', "-DPGI16", "-Dqd_emulate", "-Mfree"])

            fflags.extend(["-Mnoupcase", "-Mbackslash", "-Mlarge_arrays"])
            incs.append(f"-I{join_path(qd_root, 'include', 'qd')}")
            llibs.extend([f"-L{join_path(qd_root, 'lib')}", "-lqdmod", "-lqd"])

            if spec.satisfies("@:6.2"):
                make_include = join_path("arch", f"{include_string}pgi")
                filter_file("pgcc", spack_cc, make_include)
                filter_file("pgc++", spack_cxx, make_include, string=True)
                filter_file("pgfortran", spack_fc, make_include)
            else:
                include_string += "nvhpc"
                if spec.satisfies("+openmp"):
                    include_string += "_omp"
                if spec.satisfies("+cuda"):
                    include_string += "_acc"
            make_include = join_path("arch", include_string)
            omp_flag = "-mp"
            filter_file(r"^QD[ \t]*\??=.*$", f"QD = {qd_root}", make_include)
            filter_file("NVROOT[ \t]*=.*$", f"NVROOT = {nvroot}", make_include)
        # aocc
        elif spec.satisfies("%aocc"):
            cpp_options.extend(['-DHOST=\\"LinuxAMD\\"', "-Dshmem_bcast_buffer", "-DNGZhalf"])
            fflags.extend(["-fno-fortran-main", "-Mbackslash", "-ffunc-args-alias"])
            if spec.satisfies("@6.3.0: ^amdfftw@4.0:"):
                cpp_options.extend(["-Dfftw_cache_plans", "-Duse_fftw_plan_effort"])
            if spec.satisfies("+openmp"):
                if spec.satisfies("@6.3.2:"):
                    include_string += "aocc_ompi_aocl_omp"
                elif spec.satisfies("@=6.3.0"):
                    include_string += "gnu_ompi_aocl_omp"
                else:
                    include_string += "gnu_omp"
            else:
                if spec.satisfies("@6.3.2:"):
                    include_string += "aocc_ompi_aocl"
                elif spec.satisfies("@=6.3.0"):
                    include_string += "gnu_ompi_aocl"
                else:
                    include_string += "gnu"
            make_include = join_path("arch", include_string)
            filter_file("^CC_LIB[ ]{0,}=.*$", f"CC_LIB={spack_cc}", make_include)
            if spec.satisfies("@6:6.3.0"):
                filter_file("gcc", f"{spack_fc} -Mfree", make_include, string=True)
                filter_file(
                    "-fallow-argument-mismatch", " -fno-fortran-main", make_include, string=True
                )
        # fj
        elif spec.satisfies("@6.4.3: %fj target=a64fx"):
            include_string += "fujitsu_a64fx"
            omp_flag = "-Kopenmp"
            fc.extend(["simd_nouse_multiple_structures", "-X03"])
            fcl.append("simd_nouse_multiple_structures")
            cpp_options.append('-DHOST=\\"FJ-A64FX\\"')
            fflags.append("-Koptmsg=2")
            llibs.extend(["-SSL2BLAMP", "-SCALAPACK"])
            if spec.satisfies("+openmp"):
                include_string += "_omp"
            make_include = join_path("arch", include_string)

        else:
            if spec.satisfies("+openmp"):
                make_include = join_path("arch", f"{include_string}{spec.compiler.name}_omp")
                # if the above doesn't work, fallback to gnu
                if not os.path.exists(make_include):
                    make_include = join_path("arch", f"{include_string}.gnu_omp")
            else:
                make_include = join_path(
                    "arch", f"{include_string}{include_prefix}" + spec.compiler.name
                )
                if not os.path.exists(make_include):
                    make_include = join_path("arch", f"{include_string}.gnu")
            cpp_options.append('-DHOST=\\"LinuxGNU\\"')

        if spec.satisfies("+openmp"):
            cpp_options.extend(["-Dsysv", "-D_OPENMP"])
            llibs.extend(["-ldl", spec["fftw-api:openmp"].libs.ld_flags])
            fc.append(omp_flag)
            fcl.append(omp_flag)
        else:
            llibs.append(spec["fftw-api"].libs.ld_flags)

        if spec.satisfies("^scalapack"):
            cpp_options.append("-DscaLAPACK")
            if spec.satisfies("%nvhpc"):
                llibs.append("-Mscalapack")
            else:
                llibs.append(spec["scalapack"].libs.ld_flags)

        if spec.satisfies("+cuda"):
            if spec.satisfies("@6.3:"):
                # openacc
                cpp_options.extend(["-D_OPENACC", "-DUSENCCL"])
                llibs.extend(["-cudalib=cublas,cusolver,cufft,nccl", "-cuda"])
                fc.append("-acc")
                fcl.append("-acc")
                cuda_flags = [f"cuda{str(spec['cuda'].version.dotted[0:2])}", "rdc"]
                for f in spec.variants["cuda_arch"].value:
                    cuda_flags.append(f"cc{f}")
                fc.append(f"-gpu={','.join(cuda_flags)}")
                fcl.append(f"-gpu={','.join(cuda_flags)}")
                fcl.extend(list(self.compiler.stdcxx_libs))
                cc = [spec["mpi"].mpicc, "-acc"]
                if spec.satisfies("+openmp"):
                    cc.append(omp_flag)
                filter_file("^CC[ \t]*=.*$", f"CC = {' '.join(cc)}", make_include)

            else:
                # old cuda thing
                cflags.extend(["-DGPUSHMEM=300", "-DHAVE_CUBLAS"])
                filter_file(r"^CUDA_ROOT[ \t]*\?=.*$", spec["cuda"].prefix, make_include)

        if spec.satisfies("+vaspsol"):
            cpp_options.append("-Dsol_compat")
            copy("VASPsol/src/solvation.F", "src/")

        if spec.satisfies("+hdf5"):
            cpp_options.append("-DVASP_HDF5")
            llibs.append(spec["hdf5:fortran"].libs.ld_flags)
            incs.append(spec["hdf5"].headers.include_flags)

        if spec.satisfies("%gcc@10:"):
            fflags.append("-fallow-argument-mismatch")

        filter_file(r"^VASP_TARGET_CPU[ ]{0,}\?=.*", "", make_include)

        if spec.satisfies("@:5"):
            filter_file("-DscaLAPACK.*$\n", "", make_include)

        if spec.satisfies("+fftlib"):
            cxxftlib = (
                f"CXX_FFTLIB = {spack_cxx} {omp_flag}"
                f" -DFFTLIB_THREADSAFE{' '.join(list(self.compiler.stdcxx_libs))}"
            )
            filter_file("^#FCL[ ]{0,}=fftlib.o", "FCL += fftlib/fftlib.o", make_include)
            filter_file("^#CXX_FFTLIB.*$", cxxftlib, make_include)
            filter_file(
                "^#INCS_FFTLIB.*$",
                f"INCS_FFTLIB = -I./include {spec['fftw-api'].headers.include_flags}",
                make_include,
            )
            filter_file(r"#LIBS[ \t]*\+=.*$", "LIBS = fftlib", make_include)
            llibs.append("-ldl")
            fcl.append(join_path("fftlib", "fftlib.o"))

        # clean multiline CPP options at begining of file
        filter_file(r"^[ \t]+(-D[a-zA-Z0-9_=]+[ ]*)+[ ]*\\*$", "", make_include)
        # replace relevant variables in the makefile.include
        filter_file("^FFLAGS[ \t]*=.*$", f"FFLAGS = {' '.join(fflags)}", make_include)
        filter_file(r"^FFLAGS[ \t]*\+=.*$", "", make_include)
        filter_file(
            "^CPP_OPTIONS[ \t]*=.*$", f"CPP_OPTIONS = {' '.join(cpp_options)}", make_include
        )
        filter_file(r"^INCS[ \t]*\+?=.*$", f"INCS = {' '.join(incs)}", make_include)
        filter_file(r"^LLIBS[ \t]*\+?=.*$", f"LLIBS = {' '.join(llibs)}", make_include)
        filter_file(r"^LLIBS[ \t]*\+=[ ]*-.*$", "", make_include)
        filter_file("^CFLAGS[ \t]*=.*$", f"CFLAGS = {' '.join(cflags)}", make_include)
        filter_file(
            "^OBJECTS_LIB[ \t]*=.*$", f"OBJECTS_LIB = {' '.join(objects_lib)}", make_include
        )
        filter_file("^FC[ \t]*=.*$", f"FC = {' '.join(fc)}", make_include)
        filter_file("^FCL[ \t]*=.*$", f"FCL = {' '.join(fcl)}", make_include)

        os.rename(make_include, "makefile.include")

    def setup_build_environment(self, spack_env):
        if self.spec.satisfies("%nvhpc +cuda"):
            spack_env.set("NVHPC_CUDA_HOME", self.spec["cuda"].prefix)

    def build(self, spec, prefix):
        if spec.satisfies("@:6.2"):
            if spec.satisfies("+cuda"):
                make("DEPS=1", "all")
            else:
                make("DEPS=1", "std", "gam", "ncl")
        else:
            make("DEPS=1, all")

    def install(self, spec, prefix):
        install_tree("bin/", prefix.bin)
