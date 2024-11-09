# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

import llnl.util.tty as tty

from spack.package import *


class Likwid(Package):
    """Likwid is a simple to install and use toolsuite of command line
    applications for performance oriented programmers. It works for Intel and
    AMD processors on the Linux operating system. This version uses the
    perf_event backend which reduces the feature set but allows user installs.
    See https://github.com/RRZE-HPC/likwid/wiki/TutorialLikwidPerf#feature-limitations
    for information."""

    homepage = "https://hpc.fau.de/research/tools/likwid/"
    url = "https://github.com/RRZE-HPC/likwid/archive/v5.0.0.tar.gz"
    git = "https://github.com/RRZE-HPC/likwid.git"
    maintainers("TomTheBear")

    license("GPL-3.0-only")

    version("5.3.0", sha256="c290e554c4253124ac2ab8b056e14ee4d23966b8c9fbfa10ba81f75ae543ce4e")
    version("5.2.2", sha256="7dda6af722e04a6c40536fc9f89766ce10f595a8569b29e80563767a6a8f940e")
    version("5.2.1", sha256="1b8e668da117f24302a344596336eca2c69d2bc2f49fa228ca41ea0688f6cbc2")
    version("5.2.0", sha256="aa6dccacfca59e52d8f3be187ffcf292b2a2fa1f51a81bf8912b9d48e5a257e0")
    version("5.1.1", sha256="faec7c62987967232f476a6ff0ee85af686fd24b5a360126896b7f435d1f943f")
    version("5.1.0", sha256="5a180702a1656c6315b861a85031ab4cb090424aec42cbbb326b849e29f55571")
    version("5.0.2", sha256="0a1c8984e4b43ea8b99d09456ef05035eb934594af1669432117585c638a2da4")
    version("5.0.1", sha256="3757b0cb66e8af0116f9288c7f90543acbd8e2af8f72f77aef447ca2b3e76453")
    version("5.0.0", sha256="26623f5a1a5fec19d798f0114774a5293d1c93a148538b9591a13e50930fa41e")
    version("4.3.4", sha256="5c0d1c66b25dac8292a02232f06454067f031a238f010c62f40ef913c6609a83")
    version("4.3.3", sha256="a681378cd66c1679ca840fb5fac3136bfec93c01b3d78cc1d00a641db325a9a3")
    version("4.3.2", sha256="fd39529854b8952e7530da1684835aa43ac6ce2169f5ebd1fb2a481f6fb288ac")
    version("4.3.1", sha256="4b40a96717da54514274d166f9b71928545468091c939c1d74109733279eaeb1")
    version("4.3.0", sha256="86fc5f82c80fcff1a643394627839ec79f1ca2bcfad30000eb7018da592588b4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    patch(
        "https://github.com/RRZE-HPC/likwid/commit/e0332ace8fe8ca7dcd4b4477a25e37944f173a5c.patch?full_index=1",
        when="@5.0.1",
        sha256="13211de1b9f256b547e1565240c2c9d063855b17d70bd7379442789aa3424246",
    )
    patch(
        "https://github.com/RRZE-HPC/likwid/commit/d2d0ef333b5e0997d7c80fc6ac1a473b5e47d084.patch?full_index=1",
        when="@4.3.4",
        sha256="f14cd6bc5870e4665fe465dabaff965a5fdee19c6d669a1ec5ce2b143dcdde4b",
    )
    patch(
        "https://github.com/RRZE-HPC/likwid/files/5341379/likwid-lua5.1.patch.txt",
        when="@5.0.2^lua@5.1",
        sha256="bc56253c1e3436b5ba7bf4c5533d0391206900c8663c008f771a16376975e416",
    )
    patch(
        "https://github.com/RRZE-HPC/likwid/releases/download/v5.1.0/likwid-mpirun-5.1.0.patch?full_index=1",
        when="@5.1.0",
        sha256="62da145da0a09de21020f9726290e1daf7437691bab8a92d7254bc192d5f3061",
    )
    patch(
        "https://github.com/RRZE-HPC/likwid/releases/download/v5.2.0/likwid-icx-mem-group-fix.patch",
        sha256="af4ce278ef20cd1df26d8749a6b0e2716e4286685dae5a5e1eb4af8c383f7d10",
        when="@5.2.0:5.2.2",
    )
    variant("fortran", default=True, description="with fortran interface")
    variant("cuda", default=False, description="with Nvidia GPU profiling support")
    variant("rocm", default=False, description="with AMD GPU profiling support")

    variant(
        "accessmode",
        default="perf_event",
        values=("perf_event", "accessdaemon"),
        description="the default mode for MSR access",
    )

    # NOTE: There is no way to use an externally provided hwloc with Likwid.
    # The reason is that the internal hwloc is patched to contain extra
    # functionality and functions are prefixed with "likwid_".
    # Note: extra functionality was included in upstream hwloc

    depends_on("lua", when="@:4")
    depends_on("lua@5.2:", when="@5:5.0.1")
    depends_on("lua", when="@5.0.2:")
    depends_on("cuda", when="@5: +cuda")
    depends_on("hwloc", when="@5.2.0:")
    depends_on("rocprofiler-dev", when="@5.3: +rocm")
    depends_on("rocm-core", when="@5.3: +rocm")
    depends_on("rocm-smi-lib", when="@5.3: +rocm")

    # TODO: check
    # depends_on('gnuplot', type='run')

    depends_on("perl", type=("build", "run"))

    def patch(self):
        files = glob.glob("perl/*.*") + glob.glob("bench/perl/*.*")

        # Allow the scripts to find Spack's perl
        filter_file("^#!/usr/bin/perl -w", "#!/usr/bin/env perl", *files)
        filter_file("^#!/usr/bin/perl", "#!/usr/bin/env perl", *files)

    def setup_run_environment(self, env):
        if self.spec.satisfies("+cuda"):
            libs = find_libraries(
                "libcupti", root=self.spec["cuda"].prefix, shared=True, recursive=True
            )
            for lib in libs.directories:
                env.append_path("LD_LIBRARY_PATH", lib)
        if self.spec.satisfies("+rocm"):
            libs = find_libraries(
                "librocprofiler64.so.1",
                root=self.spec["rocprofiler-dev"].prefix,
                shared=True,
                recursive=True,
            )
            for lib in libs.directories:
                env.append_path("LD_LIBRARY_PATH", lib)
            libs = find_libraries(
                "libhsa-runtime64.so",
                root=self.spec["rocm-core"].prefix,
                shared=True,
                recursive=True,
            )
            for lib in libs.directories:
                env.append_path("LD_LIBRARY_PATH", lib)
            libs = find_libraries(
                "librocm_smi64.so",
                root=self.spec["rocm-smi-lib"].prefix,
                shared=True,
                recursive=True,
            )
            for lib in libs.directories:
                env.append_path("LD_LIBRARY_PATH", lib)

    @run_before("install")
    def filter_sbang(self):
        # Filter sbang before install so Spack's sbang hook can fix it up
        files = ["perl/feedGnuplot"] + glob.glob("filters/*")

        filter_file("^#!/usr/bin/perl", "#!{0}".format(self.spec["perl"].command.path), *files)

    def install(self, spec, prefix):
        supported_compilers = {
            "apple-clang": "CLANG",
            "clang": "CLANG",
            "gcc": "GCC",
            "intel": "ICC",
        }
        if spec.target.family == "aarch64":
            supported_compilers = {"gcc": "GCCARMv8", "clang": "ARMCLANG", "arm": "ARMCLANG"}
        elif spec.target.family == "ppc64" or spec.target.family == "ppc64le":
            supported_compilers = {"gcc": "GCCPOWER"}
        if self.compiler.name not in supported_compilers:
            raise RuntimeError(
                "{0} is not a supported compiler \
            to compile Likwid".format(
                    self.compiler.name
                )
            )

        filter_file(
            "^COMPILER .*", "COMPILER = " + supported_compilers[self.compiler.name], "config.mk"
        )
        filter_file("^PREFIX .*", "PREFIX = " + prefix, "config.mk")

        filter_file(
            "^ACCESSMODE .*",
            "ACCESSMODE = {}".format(spec.variants["accessmode"].value),
            "config.mk",
        )
        if spec.satisfies("accessmode=accessdaemon"):
            # Disable the chown, see the `spack_perms_fix` template and script
            filter_file("^INSTALL_CHOWN .*", "INSTALL_CHOWN =", "config.mk")
        else:
            filter_file("^BUILDFREQ .*", "BUILDFREQ = false", "config.mk")
            filter_file("^BUILDDAEMON .*", "BUILDDAEMON = false", "config.mk")

        if self.spec.satisfies("+fortran"):
            filter_file("^FORTRAN_INTERFACE .*", "FORTRAN_INTERFACE = true", "config.mk")
            if self.compiler.name == "gcc":
                makepath = join_path("make", "include_GCC.mk")
                filter_file("ifort", "gfortran", makepath)
                filter_file("-module", "-I", makepath)
        else:
            filter_file("^FORTRAN_INTERFACE .*", "FORTRAN_INTERFACE = false", "config.mk")

        if self.spec.satisfies("+cuda"):
            filter_file("^NVIDIA_INTERFACE.*", "NVIDIA_INTERFACE = true", "config.mk")
            filter_file("^BUILDAPPDAEMON.*", "BUILDAPPDAEMON = true", "config.mk")
            cudainc = spec["cuda"].prefix.include
            filter_file("^CUDAINCLUDE.*", "CUDAINCLUDE = {0}".format(cudainc), "config.mk")
            cuptihead = HeaderList(find(spec["cuda"].prefix, "cupti.h", recursive=True))
            filter_file(
                "^CUPTIINCLUDE.*",
                "CUPTIINCLUDE = {0}".format(cuptihead.directories[0]),
                "config.mk",
            )
        else:
            filter_file("^NVIDIA_INTERFACE.*", "NVIDIA_INTERFACE = false", "config.mk")

        if self.spec.satisfies("+rocm"):
            env["ROCM_HOME"] = spec["rocm-core"].prefix
            filter_file("^ROCM_INTERFACE.*", "ROCM_INTERFACE = true", "config.mk")
            filter_file("^BUILDAPPDAEMON.*", "BUILDAPPDAEMON = true", "config.mk")
        else:
            filter_file("^ROCM_INTERFACE.*", "ROCM_INTERFACE = false", "config.mk")

        if spec.satisfies("^lua"):
            filter_file(
                "^#LUA_INCLUDE_DIR.*",
                "LUA_INCLUDE_DIR = {0}".format(spec["lua"].prefix.include),
                "config.mk",
            )
            filter_file(
                "^#LUA_LIB_DIR.*", "LUA_LIB_DIR = {0}".format(spec["lua"].prefix.lib), "config.mk"
            )
            filter_file("^#LUA_LIB_NAME.*", "LUA_LIB_NAME = lua", "config.mk")
            filter_file("^#LUA_BIN.*", "LUA_BIN = {0}".format(spec["lua"].prefix.bin), "config.mk")

        if spec.satisfies("^hwloc"):
            filter_file(
                "^#HWLOC_INCLUDE_DIR.*",
                "HWLOC_INCLUDE_DIR = {0}".format(spec["hwloc"].prefix.include),
                "config.mk",
            )
            ll = spec["hwloc"].libs
            if len(ll.directories) > 0 and len(ll.names) > 0:
                filter_file(
                    "^#HWLOC_LIB_DIR.*",
                    "HWLOC_LIB_DIR = {0}".format(ll.directories[0]),
                    "config.mk",
                )
                filter_file(
                    "^#HWLOC_LIB_NAME.*", "HWLOC_LIB_NAME = {0}".format(ll.names[0]), "config.mk"
                )
            else:
                raise InstallError("Failed to find library path and/or name of hwloc dependency")

        # https://github.com/RRZE-HPC/likwid/issues/287
        if self.spec.satisfies("@:5.0.2 %gcc@10:"):
            filter_file(r"^(CFLAGS.*)", "\\1 -fcommon", "make/include_GCC.mk")

        env["PWD"] = os.getcwd()
        make()
        make("install")

    # Until tty output works better from build steps, this ends up in
    # the build log.  See https://github.com/spack/spack/pull/10412.
    @run_after("install")
    def caveats(self):
        if self.spec.satisfies("accessmode=accessdaemon"):
            perm_script = "spack_perms_fix.sh"
            perm_script_path = join_path(self.spec.prefix, perm_script)
            daemons = glob.glob(join_path(self.spec.prefix, "sbin", "*"))
            with open(perm_script_path, "w") as f:
                env = spack.tengine.make_environment(dirs=self.package_dir)
                t = env.get_template(perm_script + ".j2")
                f.write(
                    t.render({"prefix": self.spec.prefix, "chowns": daemons, "chmods": daemons})
                )
            tty.warn(
                """
            For full functionality, you'll need to chown and chmod some files
            after installing the package.  This has security implications.

            We've installed a script that will make the necessary changes;
            read through it and then execute it as root (e.g. via sudo).

            The script is named:

            {0}
            """.format(
                    perm_script_path
                )
            )
