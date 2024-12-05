# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


# package has a Makefile, but only to build examples
class Pegtl(CMakePackage):
    """The Parsing Expression Grammar Template Library (PEGTL) is a
    zero-dependency C++11 header-only library for creating parsers
    according to a Parsing Expression Grammar (PEG).
    """

    homepage = "https://github.com/taocpp/PEGTL"
    url = "https://github.com/taocpp/PEGTL/tarball/2.1.4"
    git = "https://github.com/taocpp/PEGTL.git"

    license("MIT")

    version("master", branch="master")
    version("3.2.7", sha256="444c3c33686c6b2d8d45ad03af5041b7bc910ef44ac10216237d8e3e8d6e7025")
    version("3.2.0", sha256="91aa6529ef9e6b57368e7b5b1f04a3bd26a39419d30e35a3c5c66ef073926b56")
    version("2.8.3", sha256="370afd0fbe6d73c448a33c10fbe4a7254f92077f5a217317d0a32a9231293015")
    version("2.1.4", sha256="d990dccc07b4d9ba548326d11c5c5e34fa88b34fe113cb5377da03dda29f23f2")
    version("2.0.0", sha256="5aae0505077e051cae4d855c38049cc6cf71103a6cc8d0ddef01a576e8a60cc0")

    depends_on("cxx", type="build")  # generated

    # Ref: https://github.com/taocpp/PEGTL/blob/master/src/example/pegtl/json_classes.hpp
    patch("change_to_virtual_destructor.patch", when="@:2.4")

    # Ref: https://bugs.gentoo.org/733678
    patch_url = "https://gitweb.gentoo.org/repo/gentoo.git/plain/dev-libs/pegtl/files/pegtl-2.8.3-gcc-10.patch"
    patch_checksum = "fc40b0c7390f8c0473f2cb4821bda7a5e107f93ca9d2fafeff2065445bb39981"
    patch(patch_url, sha256=patch_checksum, level=0, when="@2.1.4")

    def cmake_args(self):
        args = []
        if self.run_tests:
            args.extend(["-DPEGTL_BUILD_EXAMPLES=ON", "-DPEGTL_BUILD_TESTS=ON"])
        else:
            args.extend(["-DPEGTL_BUILD_EXAMPLES=OFF", "-DPEGTL_BUILD_TESTS=OFF"])

        return args

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check(self):
        with working_dir(self.build_directory):
            make("test", parallel=False)
