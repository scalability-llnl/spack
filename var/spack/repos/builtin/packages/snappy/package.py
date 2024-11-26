# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Snappy(CMakePackage):
    """A fast compressor/decompressor: https://code.google.com/p/snappy"""

    homepage = "https://github.com/google/snappy"
    url = "https://github.com/google/snappy/archive/1.1.8.tar.gz"

    license("BSD-3-Clause")

    version("1.2.1", sha256="736aeb64d86566d2236ddffa2865ee5d7a82d26c9016b36218fcc27ea4f09f86")
    version("1.1.10", sha256="49d831bffcc5f3d01482340fe5af59852ca2fe76c3e05df0e67203ebbe0f1d90")
    version("1.1.9", sha256="75c1fbb3d618dd3a0483bff0e26d0a92b495bbe5059c8b4f1c962b478b6e06e7")
    version("1.1.8", sha256="16b677f07832a612b0836178db7f374e414f94657c138e6993cbfc5dcc58651f")
    version("1.1.7", sha256="3dfa02e873ff51a11ee02b9ca391807f0c8ea0529a4924afa645fbf97163f9d4")

    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")
    variant("pic", default=True, description="Build position independent code")

    depends_on("googletest", type="test")

    patch("link_gtest.patch", when="@:1.1.8")

    # Version 1.1.9 makes use of an assembler feature that is not necessarily available when the
    # __GNUC__ preprocessor macro is defined. Version 1.1.10 switched to the correct macro
    # __GCC_ASM_FLAG_OUTPUTS__, which we also do for the version 1.1.9 by applying the patch from
    # the upstream repo (see the commit message of the patch for more details).
    patch(
        "https://github.com/google/snappy/commit/8dd58a519f79f0742d4c68fbccb2aed2ddb651e8.patch?full_index=1",
        sha256="debcdf182c046a30e9afea99ebbff280dd1fbb203e89abce6a05d3d17c587768",
        when="@1.1.9",
    )

    # nvhpc@:22.3 does not know flag '-fno-rtti'
    # nvhpc@:22.7 fails to compile snappy.cc: line 126: error: excessive recursion at instantiation
    #   of class "snappy::<unnamed>::make_index_sequence<
    conflicts("@1.1.9:", when="%nvhpc@:22.7")

    def cmake_args(self):
        return [
            self.define("CMAKE_INSTALL_LIBDIR", self.prefix.lib),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("SNAPPY_BUILD_TESTS", self.run_tests),
            self.define("SNAPPY_BUILD_BENCHMARKS", "OFF"),
        ]

    def flag_handler(self, name, flags):
        flags = list(flags)
        if "+pic" in self.spec:
            if name == "cflags":
                flags.append(self.compiler.cc_pic_flag)
            elif name == "cxxflags":
                flags.append(self.compiler.cxx_pic_flag)
        return (None, None, flags)

    @run_after("install")
    def install_pkgconfig(self):
        mkdirp(self.prefix.lib.pkgconfig)

        with open(join_path(self.prefix.lib.pkgconfig, "snappy.pc"), "w") as f:
            f.write("prefix={0}\n".format(self.prefix))
            f.write("exec_prefix=${prefix}\n")
            f.write("libdir={0}\n".format(self.prefix.lib))
            f.write("includedir={0}\n".format(self.prefix.include))
            f.write("\n")
            f.write("Name: Snappy\n")
            f.write("Description: A fast compressor/decompressor.\n")
            f.write("Version: {0}\n".format(self.spec.version))
            f.write("Cflags: -I${includedir}\n")
            f.write("Libs: -L${libdir} -lsnappy\n")
