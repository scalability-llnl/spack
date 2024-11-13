# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Leveldb(CMakePackage):
    """LevelDB is a fast key-value storage library written at Google
    that provides an ordered mapping from string keys to string values."""

    homepage = "https://github.com/google/leveldb"
    url = "https://github.com/google/leveldb/archive/1.22.tar.gz"
    git = "https://github.com/google/leveldb.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.23", sha256="9a37f8a6174f09bd622bc723b55881dc541cd50747cbd08831c2a82d620f6d76")
    version("1.22", sha256="55423cac9e3306f4a9502c738a001e4a339d1a38ffbee7572d4a07d5d63949b2")
    version("1.20", sha256="f5abe8b5b209c2f36560b75f32ce61412f39a2922f7045ae764a2c23335b6664")
    version("1.18", sha256="4aa1a7479bc567b95a59ac6fb79eba49f61884d6fd400f20b7af147d54c5cee5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared library")

    depends_on("cmake@3.9:", when="@1.21:", type="build")

    depends_on("snappy")

    patch("0001-fix-check-for-Wthread-safety.patch", when="@1.22")

    def url_for_version(self, version):
        url = "https://github.com/google/leveldb/archive/{0}.tar.gz"

        if version >= Version("1.21"):
            ver = version
        else:
            ver = "v{0}".format(version)

        return url.format(ver)

    # CMake support was added in version 1.21
    @when("@:1.20")
    def cmake(self, spec, prefix):
        pass

    @when("@:1.20")
    def build(self, spec, prefix):
        pass

    @when("@:1.20")
    def install(self, spec, prefix):
        make()

        mkdirp(prefix.lib)

        # Needed for version 1.20
        install("out-shared/libleveldb.*", prefix.lib)
        install("out-static/libleveldb.*", prefix.lib)
        # Needed for version 1.18
        install("libleveldb.*", prefix.lib)

        install_tree("include", prefix.include)

    def cmake_args(self):
        args = []

        if self.spec.satisfies("+shared"):
            args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            args.append("-DBUILD_SHARED_LIBS=OFF")

        # 1.23 tarball is missing the benchmark and test submodules
        # and for older versions, some compilers fail to compile the
        # benchmarks
        args.append("-DLEVELDB_BUILD_BENCHMARKS=OFF")
        args.append("-DLEVELDB_BUILD_TESTS=OFF")

        return args

    @run_after("install")
    def install_pkgconfig(self):
        libdir = self.spec["leveldb"].libs.directories[0]
        pkg_path = join_path(libdir, "pkgconfig")
        mkdirp(pkg_path)

        with open(join_path(pkg_path, "leveldb.pc"), "w") as f:
            f.write("prefix={0}\n".format(self.prefix))
            f.write("exec_prefix=${prefix}\n")
            f.write("libdir={0}\n".format(libdir))
            f.write("includedir={0}\n".format(self.prefix.include))
            f.write("\n")
            f.write("Name: leveldb\n")
            f.write(
                "Description: LevelDB is a fast key-value storage library"
                " written at Google that provides an ordered mapping from"
                " string keys to string values.\n"
            )
            f.write("Version: {0}\n".format(self.spec.version))
            f.write("Cflags: -I${includedir}\n")
            f.write("Libs: -L${libdir} -lleveldb\n")
