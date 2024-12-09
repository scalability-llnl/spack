# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rocksdb(MakefilePackage):
    """RocksDB: A Persistent Key-Value Store for Flash and RAM Storage"""

    homepage = "https://github.com/facebook/rocksdb"
    url = "https://github.com/facebook/rocksdb/archive/v6.5.3.tar.gz"
    git = "https://github.com/facebook/rocksdb.git"

    license("Apache-2.0 OR GPL-2.0-only")

    version("master", git=git, branch="master", submodules=True)
    version("9.4.0", sha256="1f829976aa24b8ba432e156f52c9e0f0bd89c46dc0cc5a9a628ea70571c1551c")
    version("9.2.1", sha256="bb20fd9a07624e0dc1849a8e65833e5421960184f9c469d508b58ed8f40a780f")
    version("8.6.7", sha256="cdb2fc3c6a556f20591f564cb8e023e56828469aa3f76e1d9535c443ba1f0c1a")
    version("8.1.1", sha256="9102704e169cfb53e7724a30750eeeb3e71307663852f01fa08d5a320e6155a8")
    version("7.7.3", sha256="b8ac9784a342b2e314c821f6d701148912215666ac5e9bdbccd93cf3767cb611")
    version("7.2.2", sha256="c4ea6bd2e3ffe3f0f8921c699234d59108c9122d61b0ba2aa78358642a7b614e")
    version("6.20.3", sha256="c6502c7aae641b7e20fafa6c2b92273d935d2b7b2707135ebd9a67b092169dca")
    version("6.19.3", sha256="5c19ffefea2bbe4c275d0c60194220865f508f371c64f42e802b4a85f065af5b")
    version("6.11.4", sha256="6793ef000a933af4a834b59b0cd45d3a03a3aac452a68ae669fb916ddd270532")
    version("6.7.3", sha256="c4d1397b58e4801b5fd7c3dd9175e6ae84541119cbebb739fe17d998f1829e81")
    version("6.5.3", sha256="6dc023a11d61d00c8391bd44f26ba7db06c44be228c10b552edc84e02d7fbde2")
    version("5.18.3", sha256="7fb6738263d3f2b360d7468cf2ebe333f3109f3ba1ff80115abd145d75287254")
    version("5.17.2", sha256="101f05858650a810c90e4872338222a1a3bf3b24de7b7d74466814e6a95c2d28")
    version("5.16.6", sha256="f0739edce1707568bdfb36a77638fd5bae287ca21763ce3e56cf0bfae8fff033")
    version("5.15.10", sha256="26d5d4259fa352ae1604b5b4d275f947cacc006f4f7d2ef0b815056601b807c0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("bz2", default=False, description="Enable bz2 compression support")
    variant("lz4", default=True, description="Enable lz4 compression support")
    variant("shared", default=True, description="Build shared library")
    variant("snappy", default=False, description="Enable snappy compression support")
    variant("static", default=True, description="Build static library")
    variant("zlib", default=True, description="Enable zlib compression support")
    variant("zstd", default=False, description="Enable zstandard compression support")
    variant("tbb", default=False, description="Enable Intel TBB support")
    variant("werror", default=False, description="Build with -Werror")
    variant("rtti", default=False, description="Build with RTTI")

    depends_on("bash", type="build")
    # Depends on coreutil's install command (e.g., Alpine's Busybox version does not work)
    depends_on("coreutils", type="build")
    depends_on("perl", type="build")
    depends_on("which", type="build")

    depends_on("bzip2", when="+bz2")
    depends_on("gflags")
    depends_on("lz4", when="+lz4")
    depends_on("snappy", when="+snappy")
    depends_on("zlib-api", when="+zlib")
    depends_on("zstd", when="+zstd")
    depends_on("tbb", when="+tbb")

    # https://github.com/facebook/rocksdb/issues/8286
    patch("pkg-config.patch", when="@6.13.2:6.27.3")
    patch("pkg-config-6.28.patch", when="@6.28.2:")

    conflicts("~shared~static", msg="have to build one type of library")

    phases = ["install"]

    def patch(self):
        filter_file("-march=native", "", join_path("build_tools", "build_detect_platform"))

    def install(self, spec, prefix):
        cflags = []
        ldflags = []

        if spec.satisfies("%gcc@9:"):
            cflags.append("-Wno-error=deprecated-copy")
            cflags.append("-Wno-error=pessimizing-move")
            cflags.append("-Wno-error=redundant-move")

        if "+zlib" in self.spec:
            cflags.append("-I" + self.spec["zlib-api"].prefix.include)
            ldflags.append(self.spec["zlib-api"].libs.ld_flags)
        else:
            env["ROCKSDB_DISABLE_ZLIB"] = "YES"

        if "+bz2" in self.spec:
            cflags.append("-I" + self.spec["bz2"].prefix.include)
            ldflags.append(self.spec["bz2"].libs.ld_flags)
        else:
            env["ROCKSDB_DISABLE_BZIP"] = "YES"

        if "+tbb" in self.spec:
            cflags.append(spec["tbb"].headers.cpp_flags)
            ldflags.append("-L" + spec["tbb"].prefix.lib)
        else:
            env["ROCKSDB_DISABLE_TBB"] = "YES"

        for pkg in ["lz4", "snappy", "zstd"]:
            if "+" + pkg in self.spec:
                cflags.append(self.spec[pkg].headers.cpp_flags)
                ldflags.append(self.spec[pkg].libs.ld_flags)
            else:
                env["ROCKSDB_DISABLE_" + pkg.upper()] = "YES"

        cflags.append(self.spec["gflags"].headers.cpp_flags)
        ldflags.append(self.spec["gflags"].libs.ld_flags)

        env["CFLAGS"] = " ".join(cflags)
        env["PLATFORM_FLAGS"] = " ".join(ldflags)

        if "~werror" in self.spec:
            env["DISABLE_WARNING_AS_ERROR"] = "1"

        if "+rtti" in self.spec:
            env["USE_RTTI"] = "1"

        if self.spec.satisfies("@6.13.2:"):
            env["PREFIX"] = self.spec.prefix
        else:
            env["INSTALL_PATH"] = self.spec.prefix

        if "+static" in spec:
            make("install-static")

        # We need to clean before building the shared library, otherwise
        # we might end up with errors regarding missing -fPIC.
        if "+static+shared" in spec:
            make("clean")

        if "+shared" in spec:
            make("install-shared")

    @run_after("install")
    def install_pkgconfig(self):
        if self.spec.satisfies("@6.13.2:"):
            return

        libdir = self.spec["rocksdb"].libs.directories[0]
        pkg_path = join_path(libdir, "pkgconfig")
        mkdirp(pkg_path)

        with open(join_path(pkg_path, "rocksdb.pc"), "w") as f:
            f.write("prefix={0}\n".format(self.prefix))
            f.write("exec_prefix=${prefix}\n")
            f.write("libdir={0}\n".format(libdir))
            f.write("includedir={0}\n".format(self.prefix.include))
            f.write("\n")
            f.write("Name: rocksdb\n")
            f.write(
                "Description: RocksDB: A Persistent Key-Value Store for" " Flash and RAM Storage\n"
            )
            f.write("Version: {0}\n".format(self.spec.version))
            f.write("Cflags: -I${includedir}\n")
            f.write("Libs: -L${libdir} -lrocksdb -ldl\n")
