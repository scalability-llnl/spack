# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

from spack.package import *


class Bzip2(Package, SourcewarePackage):
    """bzip2 is a freely available, patent free high-quality data
    compressor. It typically compresses files to within 10% to 15%
    of the best available techniques (the PPM family of statistical
    compressors), whilst being around twice as fast at compression
    and six times faster at decompression."""

    homepage = "https://sourceware.org/bzip2/"
    sourceware_mirror_path = "bzip2/bzip2-1.0.8.tar.gz"

    executables = [r"^bzip2$"]
    tags = ["windows"]

    license("bzip2-1.0.6")

    version("1.0.8", sha256="ab5a03176ee106d3f0fa90e381da478ddae405918153cca248e682cd0c4a2269")
    version("1.0.7", sha256="e768a87c5b1a79511499beb41500bcc4caf203726fff46a6f5f9ad27fe08ab2b")
    version("1.0.6", sha256="a2848f34fcd5d6cf47def00461fcb528a0484d8edef8208d6d2e2909dc61d9cd")

    depends_on("c", type="build")  # generated

    variant(
        "shared",
        default=(sys.platform != "win32"),
        description="Enables the build of shared libraries.",
    )
    variant("pic", default=False, description="Build static libraries with PIC")
    variant("debug", default=False, description="Enable debug symbols and disable optimization")

    # makefile.msc doesn't provide a shared recipe
    conflicts(
        "+shared",
        when="platform=windows",
        msg="Windows makefile has no recipe for shared builds, use ~shared.",
    )

    if sys.platform != "win32":
        depends_on("diffutils", type="build")

    depends_on("gmake", type="build", when="platform=linux")
    depends_on("gmake", type="build", when="platform=darwin")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--help", output=str, error=str)
        match = re.search(r"bzip2, a block-sorting file compressor." "  Version ([^,]+)", output)
        return match.group(1) if match else None

    # override default implementation
    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libbz2", root=self.prefix, shared=shared, recursive=True)

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("+pic"):
                flags.append(self.compiler.cc_pic_flag)
            if self.spec.satisfies("+debug"):
                flags.append("-g")
        return (flags, None, None)

    def patch(self):
        if self.spec.satisfies("+debug"):
            for makefile in ["Makefile", "Makefile-libbz2_so", "makefile.msc"]:
                filter_file(r"-O ", "-O0 ", makefile)
                filter_file(r"-O2 ", "-O0 ", makefile)
                filter_file(r"-Ox ", "-O0 ", makefile)

        # bzip2 comes with two separate Makefiles for static and dynamic builds
        # Tell both to use Spack's compiler wrapper instead of GCC
        filter_file(r"^CC=gcc", "CC={0}".format(spack_cc), "Makefile")
        filter_file(r"^CC=gcc", "CC={0}".format(spack_cc), "Makefile-libbz2_so")

        # The Makefiles use GCC flags that are incompatible with PGI
        if self.spec.satisfies("%pgi") or self.spec.satisfies("%nvhpc@:20.11"):
            filter_file("-Wall -Winline", "-Minform=inform", "Makefile")
            filter_file("-Wall -Winline", "-Minform=inform", "Makefile-libbz2_so")

        # Patch the link line to use RPATHs on macOS
        if "darwin" in self.spec.architecture:
            v = self.spec.version
            v1, v2, v3 = (v.up_to(i) for i in (1, 2, 3))

            kwargs = {"ignore_absent": False, "backup": False, "string": True}

            mf = FileFilter("Makefile-libbz2_so")
            mf.filter(
                "$(CC) -shared -Wl,-soname -Wl,libbz2.so.{0} -o libbz2.so.{1} $(OBJS)".format(
                    v2, v3
                ),
                (
                    "$(CC) -dynamiclib -Wl,-install_name -Wl,@rpath/libbz2.{0}.dylib "
                    "-current_version {1} -compatibility_version {2} -o libbz2.{3}.dylib $(OBJS)"
                ).format(v1, v2, v3, v3),
                **kwargs,
            )

            mf.filter(
                "$(CC) $(CFLAGS) -o bzip2-shared bzip2.c libbz2.so.{0}".format(v3),
                "$(CC) $(CFLAGS) -o bzip2-shared bzip2.c libbz2.{0}.dylib".format(v3),
                **kwargs,
            )
            mf.filter(
                "rm -f libbz2.so.{0}".format(v2), "rm -f libbz2.{0}.dylib".format(v2), **kwargs
            )
            mf.filter(
                "ln -s libbz2.so.{0} libbz2.so.{1}".format(v3, v2),
                "ln -s libbz2.{0}.dylib libbz2.{1}.dylib".format(v3, v2),
                **kwargs,
            )

    def install(self, spec, prefix):
        # Build the dynamic library first
        if spec.satisfies("+shared"):
            make("-f", "Makefile-libbz2_so")

        # Build the static library and everything else
        if self.spec.satisfies("platform=windows"):
            # Build step
            nmake = Executable("nmake.exe")
            nmake("-f", "makefile.msc")
            # Install step
            mkdirp(self.prefix.include)
            mkdirp(self.prefix.lib)
            mkdirp(self.prefix.bin)
            mkdirp(self.prefix.man)
            mkdirp(self.prefix.man.man1)
            install("*.h", self.prefix.include)
            install("*.lib", self.prefix.lib)
            install("*.exe", self.prefix.bin)
            install("*.1", self.prefix.man.man1)
        else:
            make()
            make("install", "PREFIX={0}".format(prefix))

        if spec.satisfies("+shared"):
            install("bzip2-shared", join_path(prefix.bin, "bzip2"))

            v1, v2, v3 = (self.spec.version.up_to(i) for i in (1, 2, 3))
            if "darwin" in self.spec.architecture:
                lib = "libbz2.dylib"
                lib1, lib2, lib3 = ("libbz2.{0}.dylib".format(v) for v in (v1, v2, v3))
            else:
                lib = "libbz2.so"
                lib1, lib2, lib3 = ("libbz2.so.{0}".format(v) for v in (v1, v2, v3))

            install(lib3, join_path(prefix.lib, lib3))
            with working_dir(prefix.lib):
                for libname in (lib, lib1, lib2):
                    symlink(lib3, libname)

        # These files won't be in a Windows installation
        if not self.spec.satisfies("platform=windows"):
            with working_dir(prefix.bin):
                force_remove("bunzip2", "bzcat")
                symlink("bzip2", "bunzip2")
                symlink("bzip2", "bzcat")

    @run_after("install")
    def install_pkgconfig(self):
        # Add pkgconfig file after installation
        libdir = self.spec["bzip2"].libs.directories[0]
        pkg_path = join_path(self.prefix.lib, "pkgconfig")
        mkdirp(pkg_path)

        with open(join_path(pkg_path, "bzip2.pc"), "w") as f:
            f.write("prefix={0}\n".format(self.prefix))
            f.write("exec_prefix=${prefix}/bin\n")
            f.write("libdir={0}\n".format(libdir))
            f.write("includedir={0}\n".format(self.prefix.include))
            f.write("\n")
            f.write("Name: bzip2\n")
            f.write("Description: a file compression library\n")
            f.write("Version: {0}\n".format(self.spec.version))
            f.write("Libs: -L${libdir} -lbz2\n")
            f.write("Cflags: -I${includedir}\n")
