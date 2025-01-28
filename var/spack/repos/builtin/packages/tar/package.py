# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Tar(AutotoolsPackage, GNUMirrorPackage):
    """GNU Tar provides the ability to create tar archives, as well as various
    other kinds of manipulation."""

    homepage = "https://www.gnu.org/software/tar/"
    gnu_mirror_path = "tar/tar-1.32.tar.gz"

    executables = [r"^tar$"]

    tags = ["core-packages"]

    license("GPL-3.0-or-later")

    version("1.35", sha256="14d55e32063ea9526e057fbf35fcabd53378e769787eff7919c3755b02d2b57e")
    version("1.34", sha256="03d908cf5768cfe6b7ad588c921c6ed21acabfb2b79b788d1330453507647aed")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2019-9923
        version("1.32", sha256="b59549594d91d84ee00c99cf2541a3330fed3a42c440503326dab767f2fbb96c")
        version("1.31", sha256="b471be6cb68fd13c4878297d856aebd50551646f4e3074906b1a74549c40d5a2")
        version("1.30", sha256="4725cc2c2f5a274b12b39d1f78b3545ec9ebb06a6e48e8845e1995ac8513b088")
        version("1.29", sha256="cae466e6e58c7292355e7080248f244db3a4cf755f33f4fa25ca7f9a7ed09af0")
        version("1.28", sha256="6a6b65bac00a127a508533c604d5bf1a3d40f82707d56f20cefd38a05e8237de")

    depends_on("c", type="build")

    variant(
        "zip",
        default="pigz",
        values=("gzip", "pigz"),
        description="Default compression program for tar -z",
    )

    depends_on("iconv")

    # Compression
    depends_on("gzip", type="run", when="zip=gzip")
    depends_on("pigz", type="run", when="zip=pigz")
    depends_on("zstd+programs", type="run", when="@1.31:")
    depends_on("xz", type="run")  # for xz/lzma
    depends_on("bzip2", type="run")

    patch("tar-pgi.patch", when="@1.29")
    patch("config-pgi.patch", when="@:1.29")
    patch("se-selinux.patch", when="@:1.29")
    patch("argp-pgi.patch", when="@:1.29")
    patch("gnutar-configure-xattrs.patch", when="@1.28")

    # The NVIDIA compilers do not currently support some GNU builtins.
    # Detect this case and use the fallback path.
    with when("%nvhpc"):
        patch("nvhpc-1.30.patch", when="@1.30:1.32")
        patch("nvhpc-1.34.patch", when="@1.34")
        # Workaround bug where __LONG_WIDTH__ is not defined
        patch("nvhpc-long-width.patch", when="@1.34:")
        # Newer versions are marked as conflict for now
        conflicts("@1.35:", msg="NVHPC not yet supported for 1.35")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"tar \(GNU tar\) (\S+)", output)
        return match.group(1) if match else None

    def flag_handler(self, name, flags):
        if name == "ldflags" and self.spec.satisfies("@1.35 ^[virtuals=iconv] libiconv"):
            # https://savannah.gnu.org/bugs/?64441
            flags.append("-liconv")
        return (flags, None, None)

    def configure_args(self):
        # Note: compression programs are passed by abs path,
        # so that tar can locate them when invoked without spack load.
        args = [
            "--disable-nls",
            f"--with-xz={self.spec['xz'].prefix.bin.xz}",
            f"--with-lzma={self.spec['xz'].prefix.bin.lzma}",
            f"--with-bzip2={self.spec['bzip2'].prefix.bin.bzip2}",
        ]

        if self.spec.dependencies("zstd"):
            args.append(f"--with-zstd={self.spec['zstd'].prefix.bin.zstd}")

        # Choose gzip/pigz
        zip = self.spec.variants["zip"].value
        if zip == "gzip":
            gzip_path = self.spec["gzip"].prefix.bin.gzip
        elif zip == "pigz":
            gzip_path = self.spec["pigz"].prefix.bin.pigz
        args.append(f"--with-gzip={gzip_path}")

        if self.spec["iconv"].name == "libiconv":
            args.append(f"--with-libiconv-prefix={self.spec['iconv'].prefix}")
        else:
            args.append("--without-libiconv-prefix")
        return args
