# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import sys

import llnl.util.tty as tty

from spack.build_environment import optimization_flags
from spack.package import *


class Namd(MakefilePackage, CudaPackage, ROCmPackage):
    """NAMD is a parallel molecular dynamics code designed for
    high-performance simulation of large biomolecular systems."""

    homepage = "https://www.ks.uiuc.edu/Research/namd/"
    url = "file://{0}/NAMD_2.12_Source.tar.gz".format(os.getcwd())
    git = "https://charm.cs.illinois.edu/gerrit/namd.git"
    manual_download = True
    redistribute(source=False, binary=False)

    maintainers("jcphill")

    version("master", branch="master")
    version("3.0", sha256="301c64f0f1db860f7336efdb26223ccf66b5ab42bfc9141df8d81ec1e20bf472")
    version(
        "3.0b7",
        sha256="b18ff43b0f55ec59e137c62eba1812589dd88b2122c3a05ea652781667f438b4",
        deprecated=True,
    )
    version(
        "3.0b6",
        sha256="8b5fb1dc8d5b5666c6a45d20ee7e8c9d1f5c186578e2cf148b68ba421d43b850",
        deprecated=True,
    )
    version(
        "3.0b3",
        sha256="20c32b6161f9c376536e3cb97c3bfe5367e1baaaace3c716ff79831fc2eb8199",
        deprecated=True,
    )
    version(
        "2.15a2",
        sha256="8748cbaa93fc480f92fc263d9323e55bce6623fc693dbfd4a40f59b92669713e",
        deprecated=True,
    )
    version("2.15a1", branch="master", tag="release-2-15-alpha-1", deprecated=True)
    # Same as above, but lets you use a local file instead of git
    version(
        "2.15a1.manual",
        sha256="474006e98e32dddae59616b3b75f13a2bb149deaf7a0d617ce7fb9fd5a56a33a",
        deprecated=True,
    )
    version(
        "2.14",
        sha256="34044d85d9b4ae61650ccdba5cda4794088c3a9075932392dd0752ef8c049235",
        preferred=True,
    )
    version("2.13", md5="9e3323ed856e36e34d5c17a7b0341e38")
    version("2.12", md5="2a1191909b1ab03bf0205971ad4d8ee9")

    variant(
        "fftw",
        default="3",
        values=("none", "2", "3", "mkl", "amdfftw"),
        description="Enable the use of FFTW/FFTW3/MKL FFT/AMDFFTW",
    )

    variant(
        "interface",
        default="tcl",
        values=("none", "tcl", "python"),
        description="Enables Tcl and/or python interface",
    )

    variant(
        "avxtiles",
        when="target=x86_64_v4: @2.15:",
        default=False,
        description="Enable avxtiles supported with NAMD 2.15+",
    )
    variant("single_node_gpu", default=False, description="Single node GPU")

    # Adding memopt variant to build memory-optimized mode that utilizes a compressed
    # version of the molecular structure and also supports parallel I/O.
    # Refer: https://www.ks.uiuc.edu/Research/namd/wiki/index.cgi?NamdMemoryReduction
    variant(
        "memopt",
        when="@2.8:",
        default=False,
        description="Enable memory-optimized build supported with NAMD 2.8+",
    )

    # init_tcl_pointers() declaration and implementation are inconsistent
    # "src/colvarproxy_namd.C", line 482: error: inherited member is not
    # allowed
    patch("inherited-member-2.13.patch", when="@2.13")
    patch("inherited-member-2.14.patch", when="@2.14")
    # Handle change in python-config for python@3.8:
    patch("namd-python38.patch", when="interface=python ^python@3.8:")

    depends_on("charmpp@7.0.0:", when="@3.0:")
    depends_on("charmpp@6.10.1:6", when="@2.14:2")
    depends_on("charmpp@6.8.2", when="@2.13")
    depends_on("charmpp@6.7.1", when="@2.12")

    depends_on("fftw@:2", when="fftw=2")
    depends_on("fftw@3:", when="fftw=3")

    depends_on("amdfftw", when="fftw=amdfftw")

    depends_on("mkl", when="fftw=mkl")

    depends_on("tcl", when="interface=tcl")

    depends_on("tcl", when="interface=python")
    depends_on("python", when="interface=python")

    conflicts("+rocm", when="+cuda", msg="NAMD supports only one GPU backend at a time")
    conflicts("+single_node_gpu", when="~cuda~rocm")
    conflicts(
        "+memopt",
        when="+single_node_gpu",
        msg="memopt mode is not compatible with GPU-resident builds",
    )

    # https://www.ks.uiuc.edu/Research/namd/2.12/features.html
    # https://www.ks.uiuc.edu/Research/namd/2.13/features.html
    # https://www.ks.uiuc.edu/Research/namd/2.14/features.html
    depends_on("cuda@6.5.14:7.5.18", when="@2.12 +cuda")
    depends_on("cuda@8.0.61:", when="@2.13: +cuda")

    def _copy_arch_file(self, lib):
        config_filename = "arch/{0}.{1}".format(self.arch, lib)
        if self.arch == "linux-aarch64":
            copy("arch/Linux-ARM64.{0}".format(lib), config_filename)
        else:
            copy("arch/Linux-x86_64.{0}".format(lib), config_filename)

        if lib == "tcl":
            filter_file(
                r"-ltcl8\.5", "-ltcl{0}".format(self.spec["tcl"].version.up_to(2)), config_filename
            )

    def _append_option(self, opts, lib):
        if lib != "python":
            self._copy_arch_file(lib)
        spec = self.spec
        lib_prefix = (
            spec[lib].package.component_prefix
            if spec[lib].name == "intel-oneapi-mkl"
            else spec[lib].prefix
        )
        opts.extend(["--with-{0}".format(lib), "--{0}-prefix".format(lib), lib_prefix])

    @property
    def arch(self):
        plat = sys.platform
        if plat.startswith("linux"):
            plat = "linux"
        march = platform.machine()
        return "{0}-{1}".format(plat, march)

    @property
    def build_directory(self):
        return "{0}-spack".format(self.arch)

    def _edit_arch_generic(self, spec, prefix):
        """Generic arch makefile generation"""
        m64 = "-m64 " if not spec.satisfies("arch=aarch64:") else ""
        with working_dir("arch"):
            with open("{0}.arch".format(self.build_directory), "w") as fh:
                # this options are take from the default provided
                # configuration files
                # https://github.com/UIUC-PPL/charm/pull/2778
                archopt = optimization_flags(self.compiler, spec.target)

                if self.spec.satisfies("^charmpp@:6.10.1"):
                    optims_opts = {
                        "gcc": m64
                        + "-O3 -fexpensive-optimizations \
                                        -ffast-math -lpthread "
                        + archopt,
                        "intel": "-O2 -ip -qopenmp-simd" + archopt,
                        "clang": m64 + "-O3 -ffast-math -fopenmp " + archopt,
                        "aocc": m64
                        + "-O3 -ffp-contract=fast -ffast-math \
                                        -fopenmp "
                        + archopt,
                    }
                else:
                    optims_opts = {
                        "gcc": m64
                        + "-O3 -fexpensive-optimizations \
                                        -ffast-math -lpthread "
                        + archopt,
                        "intel": "-O2 -ip " + archopt,
                        "clang": m64 + "-O3 -ffast-math -fopenmp " + archopt,
                        "aocc": m64
                        + "-O3 -ffp-contract=fast \
                                        -ffast-math "
                        + archopt,
                    }

                if self.spec.satisfies("+avxtiles"):
                    optims_opts["aocc"] += " -DNAMD_AVXTILES"
                    optims_opts["clang"] += " -DNAMD_AVXTILES"
                    optims_opts["gcc"] += " -DNAMD_AVXTILES"
                    optims_opts["intel"] += " -DNAMD_AVXTILES"

                optim_opts = (
                    optims_opts[self.compiler.name] if self.compiler.name in optims_opts else ""
                )

                fh.write(
                    "\n".join(
                        [
                            "NAMD_ARCH = {0}".format(self.arch),
                            "CHARMARCH = {0}".format(self.spec["charmpp"].charmarch),
                            "CXX = {0.cxx} {0.cxx11_flag}".format(self.compiler),
                            "CXXOPTS = {0}".format(optim_opts),
                            "CC = {0}".format(self.compiler.cc),
                            "COPTS = {0}".format(optim_opts),
                            "",
                        ]
                    )
                )

    def _edit_arch_target_based(self, spec, prefix):
        """Try to use target base arch file return True if succeed"""
        if spec.version < Version("2.14"):
            return False

        found_special_opt = False
        with working_dir("arch"):
            arch_filename = "{0}.arch".format(self.build_directory)

            replace = [
                [r"^CHARMARCH = .*$", "CHARMARCH = {0}".format(self.spec["charmpp"].charmarch)],
                [r"^NAMD_ARCH = .*$", "NAMD_ARCH = {0}".format(self.arch)],
            ]

            # Optimizations for skylake_avx512
            if (
                spec.platform == "linux"
                and self.compiler.name == "intel"
                and "avx512" in spec.target
                and spec.target >= "skylake_avx512"
            ):
                if spec.version >= Version("2.15") and os.path.exists("Linux-AVX512-icc.arch"):
                    tty.info("Building binaries with AVX512-tile optimization")
                    copy("Linux-AVX512-icc.arch", arch_filename)
                elif spec.version >= Version("2.14") and os.path.exists("Linux-SKX-icc.arch"):
                    tty.info("Building binaries with Skylake-X" "AVX512 optimization")
                    copy("Linux-SKX-icc.arch", arch_filename)
                else:
                    return False

                replace.append([r"^CXX = icpc", "CXX = {0}".format(self.compiler.cxx)])
                replace.append([r"^CC = icc", "CC = {0}".format(self.compiler.cc)])
                found_special_opt = True

            if found_special_opt:
                for pattern, replacement in replace:
                    filter_file(pattern, replacement, arch_filename)

        return found_special_opt

    def _edit_arch(self, spec, prefix):
        """Try to use target base arch file, if not make generic"""
        if not self._edit_arch_target_based(spec, prefix):
            self._edit_arch_generic(spec, prefix)

    def edit(self, spec, prefix):
        self._edit_arch(spec, prefix)

        self._copy_arch_file("base")

        opts = ["--charm-base", spec["charmpp"].prefix]
        fftw_version = spec.variants["fftw"].value
        if fftw_version == "none":
            opts.append("--without-fftw")
        elif fftw_version == "mkl":
            self._append_option(opts, "mkl")
        elif fftw_version == "amdfftw":
            self._copy_arch_file("fftw3")
            opts.extend(["--with-fftw3", "--fftw-prefix", spec["amdfftw"].prefix])
        else:
            _fftw = "fftw{0}".format("" if fftw_version == "2" else "3")

            self._copy_arch_file(_fftw)
            opts.extend(["--with-{0}".format(_fftw), "--fftw-prefix", spec["fftw"].prefix])

        interface_type = spec.variants["interface"].value
        if interface_type != "none":
            self._append_option(opts, "tcl")

            if interface_type == "python":
                self._append_option(opts, "python")
        else:
            opts.extend(["--without-tcl", "--without-python"])

        if "+cuda" in spec:
            self._append_option(opts, "cuda")
            filter_file(
                "^CUDADIR=.*$",
                "CUDADIR={0}".format(spec["cuda"].prefix),
                join_path("arch", self.arch + ".cuda"),
            )
            for cuda_arch in spec.variants["cuda_arch"].value:
                opts.extend(["--cuda-gencode", f"arch=compute_{cuda_arch},code=sm_{cuda_arch}"])

            if "+single_node_gpu" in spec:
                opts.extend(["--with-single-node-cuda"])

        if "+rocm" in spec:
            self._copy_arch_file("hip")
            opts.append("--with-hip")
            opts.extend(["--rocm-prefix", os.environ["ROCM_PATH"]])

            if "+single_node_gpu" in spec:
                opts.extend(["--with-single-node-hip"])

        if spec.satisfies("+memopt"):
            opts.append("--with-memopt")

        config = Executable("./config")

        config(self.build_directory, *opts)

        # patch Make.config if needed
        # spack install charmpp straight to prefix
        # (not to $(CHARMBASE)/$(CHARMARCH))
        if not os.path.exists(
            join_path(self.spec["charmpp"].prefix, self.spec["charmpp"].charmarch)
        ):
            filter_file(
                r"^CHARM = \$\(CHARMBASE\)/\$\(CHARMARCH\)",
                "CHARM = $(CHARMBASE)",
                join_path(self.build_directory, "Make.config"),
            )

    @when("@3.0b3")
    def build(self, spec, prefix):
        # Disable parallel build
        # https://github.com/spack/spack/pull/43215
        with working_dir(self.build_directory):
            make(parallel=False)

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            if spec.version < Version("3"):
                install("namd2", prefix.bin)
            else:
                install("namd3", prefix.bin)
            install("psfgen", prefix.bin)

            # I'm not sure this is a good idea or if an autoload of the charm
            # module would not be better.
            install("charmrun", prefix.bin)
