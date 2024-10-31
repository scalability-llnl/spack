# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Scorep(AutotoolsPackage):
    """The Score-P measurement infrastructure is a highly scalable and
    easy-to-use tool suite for profiling, event tracing, and online analysis
    of HPC applications.
    """

    homepage = "https://www.vi-hps.org/projects/score-p"
    url = "https://perftools.pages.jsc.fz-juelich.de/cicd/scorep/tags/scorep-7.1/scorep-7.1.tar.gz"
    maintainers("wrwilliams")

    version("8.4", sha256="7bbde9a0721d27cc6205baf13c1626833bcfbabb1f33b325a2d67976290f7f8a")
    version("8.3", sha256="76c914e6319221c059234597a3bc53da788ed679179ac99c147284dcefb1574a")
    # version 8.2 was immediately superseded before it hit Spack
    version("8.1", sha256="3a40b481fce610871ddf6bdfb88a6d06b9e5eb38c6080faac6d5e44990060a37")
    version("8.0", sha256="4c0f34f20999f92ebe6ca1ff706d0846b8ce6cd537ffbedb49dfaef0faa66311")
    version("7.1", sha256="98dea497982001fb82da3429ca55669b2917a0858c71abe2cfe7cd113381f1f7")
    version("7.0", sha256="68f24a68eb6f94eaecf500e17448f566031946deab74f2cba072ee8368af0996")
    version(
        "6.0",
        sha256="5dc1023eb766ba5407f0b5e0845ec786e0021f1da757da737db1fb71fc4236b8",
        deprecated="true",
    )
    version(
        "5.0",
        sha256="0651614eacfc92ffbe5264a3efebd0803527ae6e8b11f7df99a56a02c37633e1",
        deprecated="true",
    )
    version(
        "4.1",
        sha256="7bb6c1eecdd699b4a3207caf202866778ee01f15ff39a9ec198fcd872578fe63",
        deprecated="true",
    )
    version(
        "4.0",
        sha256="c050525606965950ad9b35c14077b88571bcf9bfca08599279a3d8d1bb00e655",
        deprecated="true",
    )
    version(
        "3.1",
        sha256="49efe8a4e02afca752452809e1b21cba42e8ccb0a0772f936d4459d94e198540",
        deprecated="true",
    )
    version(
        "3.0",
        sha256="c9e7fe0a8239b3bbbf7628eb15f7e90de9c36557818bf3d01aecce9fec2dc0be",
        deprecated="true",
    )
    version(
        "2.0.2",
        sha256="d19498408781048f0e9039a1a245bce6b384f09fbe7d3643105b4e2981ecd610",
        deprecated="true",
    )
    version(
        "1.4.2",
        sha256="d7f3fcca2efeb2f5d5b5f183b3b2c4775e66cbb3400ea2da841dd0428713ebac",
        deprecated="true",
    )
    version(
        "1.3",
        sha256="dcfd42bd05f387748eeefbdf421cb3cd98ed905e009303d70b5f75b217fd1254",
        deprecated="true",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    def url_for_version(self, version):
        if version < Version("7.0"):
            return "https://www.vi-hps.org/cms/upload/packages/scorep/scorep-{0}.tar.gz".format(
                version
            )

        return "https://perftools.pages.jsc.fz-juelich.de/cicd/scorep/tags/scorep-{0}/scorep-{0}.tar.gz".format(
            version
        )

    patch("gcc7.patch", when="@1.4:3")
    patch("gcc10.patch", when="@3.1:6.0")

    variant("mpi", default=True, description="Enable MPI support")
    variant("papi", default=True, description="Enable PAPI")
    variant("pdt", default=False, description="Enable PDT")
    variant("shmem", default=False, description="Enable shmem tracing")
    variant("unwind", default=False, description="Enable sampling via libunwind and lib wrapping")
    variant("cuda", default=False, description="Enable CUDA support")
    variant("hip", default=False, description="Enable ROCm/HIP support", when="@8.0:")
    # Dependencies for SCORE-P are quite tight. See the homepage for more
    # information. Starting with scorep 4.0 / cube 4.4, Score-P only depends on
    # two components of cube -- cubew and cubelib.

    # SCOREP 8
    depends_on("binutils", type="link", when="@8:")
    depends_on("otf2@3:", when="@8:")
    depends_on("cubew@4.8.2:", when="@8.3:")
    depends_on("cubelib@4.8.2:", when="@8.3:")
    depends_on("cubew@4.8:", when="@8:8.2")
    depends_on("cubelib@4.8:", when="@8:8.2")
    # fall through to Score-P 7's OPARI2, no new release
    # SCOREP 7
    depends_on("otf2@2.3:2.3.99", when="@7.0:7")
    depends_on("cubew@4.6:4.7.99", when="@7.0:7")
    depends_on("cubelib@4.6:4.7.99", when="@7.0:7")
    depends_on("opari2@2.0.6:", when="@7:")
    # SCOREP 6
    depends_on("otf2@2.2:", when="@6.0:6")
    # SCOREP 4 and 5
    depends_on("otf2@2.1:", when="@4:5")
    depends_on("cubew@4.4:4.5", when="@4:6")
    depends_on("cubelib@4.4:4.5", when="@4:6")
    # SCOREP 3
    depends_on("otf2@2:", when="@3.0:3")
    depends_on("opari2@2.0:2.0.5", when="@3:6")
    depends_on("cube@4.3:4.3.5", when="@3.0:3")
    # SCOREP 2.0.2
    depends_on("otf2@2.0", when="@2.0.2")
    depends_on("opari2@2.0", when="@2.0.2")
    depends_on("cube@4.3:4.3.5", when="@2.0.2")
    # SCOREP 1.4.2
    depends_on("otf2@1.5:1.6", when="@1.4.2")
    depends_on("opari2@1.1.4", when="@1.4.2")
    depends_on("cube@4.2.3:4.3.5", when="@1.4.2")
    # SCOREP 1.3
    depends_on("otf2@1.4", when="@1.3")
    depends_on("opari2@1.1.4", when="@1.3")
    depends_on("cube@4.2.3", when="@1.3")

    depends_on("mpi@2.2:", when="@7.0:+mpi")
    depends_on("mpi", when="+mpi")
    depends_on("papi", when="+papi")
    depends_on("pdt", when="+pdt")
    depends_on("llvm", when="+unwind")
    depends_on("libunwind", when="+unwind")
    depends_on("cuda@7:", when="@8.0:+cuda")
    depends_on("cuda", when="+cuda")
    depends_on("hip@4.2:", when="+hip")
    depends_on("rocprofiler-dev", when="+hip")
    depends_on("rocm-smi-lib", when="+hip")
    # Score-P requires a case-sensitive file system, and therefore
    # does not work on macOS
    # https://github.com/spack/spack/issues/1609
    conflicts("platform=darwin")
    # Score-P first has support for ROCm 6.x as of v8.4
    conflicts("hip@6.0:", when="@1.0:8.3+hip")

    def find_libpath(self, libname, root):
        libs = find_libraries(libname, root, shared=True, recursive=True)
        if len(libs.directories) == 0:
            return None
        return libs.directories[0]

    # handle any mapping of Spack compiler names to Score-P args
    # this should continue to exist for backward compatibility
    def clean_compiler(self, compiler):
        renames = {"cce": "cray", "rocmcc": "amdclang"}
        if compiler in renames:
            return renames[compiler]
        return compiler

    def configure_args(self):
        spec = self.spec

        config_args = [
            "--with-otf2=%s" % spec["otf2"].prefix.bin,
            "--with-opari2=%s" % spec["opari2"].prefix.bin,
            "--enable-shared",
        ]

        cname = self.clean_compiler(spec.compiler.name)

        config_args.append("--with-nocross-compiler-suite={0}".format(cname))

        if self.version >= Version("4.0"):
            config_args.append("--with-cubew=%s" % spec["cubew"].prefix.bin)
            config_args.append("--with-cubelib=%s" % spec["cubelib"].prefix.bin)
        else:
            config_args.append("--with-cube=%s" % spec["cube"].prefix.bin)

        if "+papi" in spec:
            config_args.append("--with-papi-header=%s" % spec["papi"].prefix.include)
            config_args.append("--with-papi-lib=%s" % spec["papi"].prefix.lib)

        if "+pdt" in spec:
            config_args.append("--with-pdt=%s" % spec["pdt"].prefix.bin)

        if "+unwind" in spec:
            config_args.append("--with-libunwind=%s" % spec["libunwind"].prefix)
        if "+cuda" in spec:
            config_args.append("--with-libcudart=%s" % spec["cuda"].prefix)
            cuda_driver_path = self.find_libpath("libcuda", spec["cuda"].prefix)
            config_args.append("--with-libcuda-lib=%s" % cuda_driver_path)
        if "+hip" in spec:
            config_args.append("--with-rocm=%s" % spec["hip"].prefix)

        config_args += self.with_or_without("shmem")
        config_args += self.with_or_without("mpi")

        if spec.satisfies("^intel-mpi"):
            config_args.append("--with-mpi=intel3")
        elif (
            spec.satisfies("^mpich")
            or spec.satisfies("^mvapich2")
            or spec.satisfies("^cray-mpich")
        ):
            config_args.append("--with-mpi=mpich3")
        elif spec.satisfies("^openmpi") or spec.satisfies("^hpcx-mpi"):
            config_args.append("--with-mpi=openmpi")

        if spec.satisfies("^binutils"):
            config_args.append("--with-libbfd-lib=%s" % spec["binutils"].prefix.lib)
            config_args.append("--with-libbfd-include=%s" % spec["binutils"].prefix.include)

        config_args.extend(
            [
                "CFLAGS={0}".format(self.compiler.cc_pic_flag),
                "CXXFLAGS={0}".format(self.compiler.cxx_pic_flag),
            ]
        )

        if "+mpi" in spec:
            config_args.extend(
                [
                    "MPICC={0}".format(spec["mpi"].mpicc),
                    "MPICXX={0}".format(spec["mpi"].mpicxx),
                    "MPIF77={0}".format(spec["mpi"].mpif77),
                    "MPIFC={0}".format(spec["mpi"].mpifc),
                ]
            )

        return config_args
