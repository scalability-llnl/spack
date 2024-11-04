# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os.path

from spack.package import *
from spack.util.environment import is_system_path


class Elfutils(AutotoolsPackage, SourcewarePackage):
    """elfutils is a collection of various binary tools such as
    eu-objdump, eu-readelf, and other utilities that allow you to
    inspect and manipulate ELF files. Refer to Table 5.Tools Included
    in elfutils for Red Hat Developer for a complete list of binary
    tools that are distributed with the Red Hat Developer Toolset
    version of elfutils."""

    homepage = "https://fedorahosted.org/elfutils/"
    sourceware_mirror_path = "elfutils/0.179/elfutils-0.179.tar.bz2"
    list_url = "https://sourceware.org/elfutils/ftp"
    list_depth = 1

    maintainers("mwkrentel")

    license("GPL-3.0-or-later AND ( GPL-2.0-or-later OR LGPL-3.0-or-later )")

    version("0.191", sha256="df76db71366d1d708365fc7a6c60ca48398f14367eb2b8954efc8897147ad871")
    version("0.190", sha256="8e00a3a9b5f04bc1dc273ae86281d2d26ed412020b391ffcc23198f10231d692")
    version("0.189", sha256="39bd8f1a338e2b7cd4abc3ff11a0eddc6e690f69578a57478d8179b4148708c8")
    version("0.188", sha256="fb8b0e8d0802005b9a309c60c1d8de32dd2951b56f0c3a3cb56d21ce01595dff")
    version("0.187", sha256="e70b0dfbe610f90c4d1fe0d71af142a4e25c3c4ef9ebab8d2d72b65159d454c8")
    version("0.186", sha256="7f6fb9149b1673d38d9178a0d3e0fb8a1ec4f53a9f4c2ff89469609879641177")
    version("0.185", sha256="dc8d3e74ab209465e7f568e1b3bb9a5a142f8656e2b57d10049a73da2ae6b5a6")
    version("0.184", sha256="87e7d1d7f0333815dd1f62135d047a4dc4082068f361452f357997c11360644b")
    version("0.183", sha256="c3637c208d309d58714a51e61e63f1958808fead882e9b607506a29e5474f2c5")
    version("0.182", sha256="ecc406914edf335f0b7fc084ebe6c460c4d6d5175bfdd6688c1c78d9146b8858")
    version("0.181", sha256="29a6ad7421ec2acfee489bb4a699908281ead2cb63a20a027ce8804a165f0eb3")
    version("0.180", sha256="b827b6e35c59d188ba97d7cf148fa8dc6f5c68eb6c5981888dfdbb758c0b569d")
    version("0.179", sha256="25a545566cbacaa37ae6222e58f1c48ea4570f53ba991886e2f5ce96e22a23a2")
    version("0.178", sha256="31e7a00e96d4e9c4bda452e1f2cdac4daf8abd24f5e154dee232131899f3a0f2")
    version("0.177", sha256="fa489deccbcae7d8c920f60d85906124c1989c591196d90e0fd668e3dc05042e")
    version("0.176", sha256="eb5747c371b0af0f71e86215a5ebb88728533c3a104a43d4231963f308cd1023")
    version("0.175", sha256="f7ef925541ee32c6d15ae5cb27da5f119e01a5ccdbe9fe57bf836730d7b7a65b")
    version("0.174", sha256="cdf27e70076e10a29539d89e367101d516bc4aa11b0d7777fe52139e3fcad08a")
    version("0.173", sha256="b76d8c133f68dad46250f5c223482c8299d454a69430d9aa5c19123345a000ff")
    version("0.170", sha256="1f844775576b79bdc9f9c717a50058d08620323c1e935458223a12f249c9e066")
    version("0.168", sha256="b88d07893ba1373c7dd69a7855974706d05377766568a7d9002706d5de72c276")
    version("0.163", sha256="7c774f1eef329309f3b05e730bdac50013155d437518a2ec0e24871d312f2e23")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Native language support from libintl.
    variant("nls", default=True, description="Enable Native Language Support.")
    variant("exeprefix", default=True, description="Add a prefix to generated executables.")

    # libdebuginfod support
    # NB: For 0.181 and newer, this enables _both_ the client and server
    variant(
        "debuginfod", default=False, description="Enable libdebuginfod support.", when="@0.179:"
    )

    # elfutils-0.185-static-inline.patch
    # elflint.c (buffer_left): Mark as 'inline' to avoid external linkage failure.
    patch(
        "https://794601.bugs.gentoo.org/attachment.cgi?id=714030",
        when="@0.185",
        sha256="d786d49c28d7f0c8fc27bab39ca8714e5f4d128c7f09bb18533a8ec99b38dbf8",
    )

    depends_on("bzip2", type="link")
    depends_on("xz", type="link")
    depends_on("zlib-api", type="link")
    depends_on("zstd", type="link", when="@0.182:")

    depends_on("gettext", when="+nls")
    depends_on("iconv")
    depends_on("m4", type="build")
    depends_on("pkgconfig@0.9.0:", type=("build", "link"))

    # debuginfod has extra dependencies
    # NB: Waiting on an elfutils patch before we can use libmicrohttpd@0.9.51
    depends_on("libmicrohttpd@0.9.33:0.9.50", type="link", when="+debuginfod")
    depends_on("libarchive@3.1.2:", type="link", when="+debuginfod")
    depends_on("sqlite@3.7.17:", type="link", when="+debuginfod")
    depends_on("curl@7.29.0:", type="link", when="+debuginfod")

    conflicts("%gcc@7.2.0:", when="@0.163")

    provides("elf@1")

    # libarchive with iconv doesn't configure (still broken as of libarchive@3.7.1)
    # see https://github.com/spack/spack/issues/36710
    # and https://github.com/libarchive/libarchive/issues/1819
    conflicts("^libarchive +iconv", when="+debuginfod")

    # https://sourceware.org/bugzilla/show_bug.cgi?id=24964
    conflicts("%apple-clang")
    conflicts("%clang", when="@:0.185")
    conflicts("%cce")

    # Elfutils uses -Wall and we don't want to fail the build over a
    # stray warning.
    def patch(self):
        files = glob.glob(os.path.join("*", "Makefile.in"))
        filter_file("-Werror", "", *files)

    def flag_handler(self, name, flags):
        if name == "ldlibs":
            spec = self.spec
            if "+nls" in spec and "intl" in spec["gettext"].libs.names:
                flags.append("-lintl")
        return self.inject_flags(name, flags)

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-bzlib=%s" % spec["bzip2"].prefix,
            "--with-lzma=%s" % spec["xz"].prefix,
            "--with-zlib=%s" % spec["zlib-api"].prefix,
        ]

        if spec.satisfies("+exeprefix"):
            args.append("--program-prefix='eu-'")
        else:
            args.append("--program-prefix=''")

        if spec.satisfies("@0.182:"):
            args.append("--with-zstd=%s" % spec["zstd"].prefix)

        if spec.satisfies("@0.183:"):
            if spec["iconv"].name == "libiconv":
                args.append(f"--with-libiconv-prefix={spec['iconv'].prefix}")
            else:
                args.append("--without-libiconv-prefix")

        if spec.satisfies("+nls"):
            # Prior to 0.183, only msgfmt is used from gettext.
            if spec.satisfies("@0.183:"):
                if "intl" not in spec["gettext"].libs.names:
                    args.append("--without-libintl-prefix")
                elif not is_system_path(spec["gettext"].prefix):
                    args.append("--with-libintl-prefix=" + spec["gettext"].prefix)
        else:
            args.append("--disable-nls")

        if spec.satisfies("+debuginfod"):
            args.append("--enable-debuginfod")
            if spec.satisfies("@0.181:"):
                args.append("--enable-libdebuginfod")
        else:
            args.append("--disable-debuginfod")
            if spec.satisfies("@0.181:"):
                args.append("--disable-libdebuginfod")

        return args

    # Install elf.h to include directory.
    @run_after("install")
    def install_elfh(self):
        install(join_path("libelf", "elf.h"), self.prefix.include)

    # Provide location of libelf.so to match libelf.
    @property
    def libs(self):
        return find_libraries("libelf", self.prefix, recursive=True)
