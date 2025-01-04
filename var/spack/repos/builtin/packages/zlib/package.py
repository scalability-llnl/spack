# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


# Although zlib comes with a configure script, it does not use Autotools
# The AutotoolsPackage causes zlib to fail to build with PGI
import glob
import os
import re

import spack.build_systems.generic
import spack.build_systems.makefile
from spack.package import *


class Zlib(MakefilePackage, Package):
    """A free, general-purpose, legally unencumbered lossless
    data-compression library.
    """

    homepage = "https://zlib.net"
    # URL must remain http:// so Spack can bootstrap curl
    url = "http://zlib.net/fossils/zlib-1.2.11.tar.gz"
    git = "https://github.com/madler/zlib.git"

    tags = ["core-packages"]
    libraries = ["libz", "zlib", "zlibstatic", "zlibd", "zlibstaticd"]

    version("1.3.1", sha256="9a93b2b7dfdac77ceba5a558a580e74667dd6fede4585b91eefb60f03b72df23")
    version("1.3", sha256="ff0ba4c292013dbc27530b3a81e1f9a813cd39de01ca5e0f8bf355702efa593e")
    version("1.2.13", sha256="b3a24de97a8fdbc835b9833169501030b8977031bcb54b3b3ac13740f846ab30")
    version(
        "1.2.12",
        sha256="91844808532e5ce316b3c010929493c0244f3d37593afd6de04f71821d5136d9",
        deprecated=True,
    )
    version(
        "1.2.11",
        sha256="c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1",
        deprecated=True,
    )
    version(
        "1.2.8",
        sha256="36658cb768a54c1d4dec43c3116c27ed893e88b02ecfcb44f2166f9c0b7f2a0d",
        deprecated=True,
    )
    version(
        "1.2.3",
        sha256="1795c7d067a43174113fdf03447532f373e1c6c57c08d61d9e4e9be5e244b05e",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    build_system("makefile", conditional("generic", when="platform=windows"), default="makefile")

    variant("pic", default=True, description="Produce position-independent code (for shared libs)")
    variant("shared", default=True, description="Enables the build of shared libraries.")
    variant("optimize", default=True, description="Enable -O2 for a more optimized lib")

    conflicts("build_system=makefile", when="platform=windows")

    patch("w_patch.patch", when="@1.2.11%cce")
    patch("configure-cc.patch", when="@1.2.12")

    provides("zlib-api")

    license("Zlib")

    @classmethod
    def determine_version(cls, lib):
        for library in cls.libraries:
            for ext in library_extensions:
                if ext == "dylib":
                    pattern = re.compile(rf"{library}\.(\d+\.\d+\.\d+)\.{ext}")
                else:
                    pattern = re.compile(rf"{library}\.{ext}\.(\d+\.\d+\.\d+)")
                    match = re.search(pattern, lib)
                    if match:
                        return match.group(1)

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries(["libz"], root=self.prefix, recursive=True, shared=shared)


class SetupEnvironment:
    def setup_build_environment(self, env):
        if "+pic" in self.spec:
            env.append_flags("CFLAGS", self.pkg.compiler.cc_pic_flag)
        if "+optimize" in self.spec:
            env.append_flags("CFLAGS", "-O2")


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder, SetupEnvironment):
    def edit(self, pkg, spec, prefix):
        config_args = []
        if "~shared" in self.spec:
            config_args.append("--static")
        configure("--prefix={0}".format(prefix), *config_args)

        if "+shared" in self.spec:
            # We need to fix the building of the shared libraries with compilers that are not
            # recognized as gcc. Note that a compiler is recognized as gcc if it has "gcc" or
            # "clang" substring either in its executable name (including the path) or in the output
            # generated with the `-v` flag (i.e '$CC -v 2>&1'). The latter is the reason why, for
            # example, %intel and %oneapi are often recognized as gcc: they almost always contain
            # "gcc" in the verbose output. Another example is %pgi, which has "gcc" in the name of
            # the C compiler (pgcc) and in the verbose output (e.g. "pgcc-Warning-No files to
            # process"). Although we should not rely on the false positive results of the configure
            # script but patch the makefile for all the aforementioned compilers, given the
            # importance of the package, we try to be conservative for now and do the patching only
            # for compilers that will not produce a correct shared library otherwise.
            if self.spec.satisfies("%nvhpc"):
                if "~pic" in self.spec:
                    # In this case, we should build the static library without PIC, therefore we
                    # don't append the respective compiler flag to CFLAGS in the build environment.
                    # However, we need the flag for the objects of the shared library:
                    filter_file(
                        r"^(SFLAGS *=.*)$",
                        r"\1 {0}".format(self.pkg.compiler.cc_pic_flag),
                        "Makefile",
                    )
                if self.spec.satisfies("platform=linux"):
                    # Without the following, the shared library will not have a soname entry.
                    filter_file(
                        r"^(LDSHARED *= *).*$",
                        # Note that we should use '-Wl,` and not self.pkg.compiler.linker_arg
                        # because the former is understood by virtually every C compiler and the
                        # latter might be meant for the Fortran compiler only (e.g. NAG):
                        r"\1 {0} -shared "
                        r"-Wl,-soname,libz.{1}.{2},--version-script,zlib.map".format(
                            spack_cc, dso_suffix, self.spec.version.up_to(1)
                        ),
                        "Makefile",
                    )


class GenericBuilder(spack.build_systems.generic.GenericBuilder, SetupEnvironment):
    def install(self, pkg, spec, prefix):
        nmake("-f" "win32\\Makefile.msc")
        build_dir = pkg.stage.source_path
        install_tree = {
            "bin": glob.glob(os.path.join(build_dir, "*.dll")),
            "lib": glob.glob(os.path.join(build_dir, "*.lib")),
        }
        compose_src_path = lambda x: os.path.join(build_dir, x)
        install_tree["include"] = [compose_src_path("zlib.h"), compose_src_path("zconf.h")]
        # Windows path seps are fine here as this method is Windows specific.
        install_tree["share\\man\\man3"] = [compose_src_path("zlib.3")]

        def installtree(dst, tree):
            for inst_dir in tree:
                install_dst = getattr(dst, inst_dir)
                try:
                    os.makedirs(install_dst)
                except OSError:
                    pass
                for file in tree[inst_dir]:
                    install(file, install_dst)

        installtree(prefix, install_tree)
