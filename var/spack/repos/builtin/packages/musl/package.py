# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Musl(MakefilePackage):
    """Musl is a libc, an implementation of the standard library
    functionality described in the ISO C and POSIX standards, plus common
    extensions, intended for use on Linux-based systems. Whereas the kernel
    (Linux) governs access to hardware, memory, filesystems, and the
    privileges for accessing these resources, the C library is responsible
    for providing the actual C function interfaces userspace applications
    see, and for constructing higher-level buffered stdio, memory
    allocation management, thread creation and synchronization operations,
    and so on using the lower-level interfaces the kernel provides, as well
    as for implementing pure library routines of the C language like
    strstr, snprintf, strtol, exp, sqrt, etc.

    Musl is a new general-purpose implementation of the C library. It is
    lightweight, fast, simple, free, and aims to be correct in the sense of
    standards-conformance and safety."""

    homepage = "https://www.musl-libc.org"
    url = "https://www.musl-libc.org/releases/musl-1.1.23.tar.gz"
    tags = ["runtime"]

    license("MIT")

    # This is used when the package is external and we need to find the actual default include path
    # which may be in a multiarch subdir.
    representative_headers = ["iso646.h"]

    provides("libc")
    provides("iconv")

    version("1.2.4", sha256="7a35eae33d5372a7c0da1188de798726f68825513b7ae3ebe97aaaa52114f039")
    version("1.2.3", sha256="7d5b0b6062521e4627e099e4c9dc8248d32a30285e959b7eecaa780cf8cfd4a4")
    version("1.2.2", sha256="9b969322012d796dc23dda27a35866034fa67d8fb67e0e2c45c913c3d43219dd")
    version("1.2.1", sha256="68af6e18539f646f9c41a3a2bb25be4a5cfa5a8f65f0bb647fd2bbfdf877e84b")
    version("1.2.0", sha256="c6de7b191139142d3f9a7b5b702c9cae1b5ee6e7f57e582da9328629408fd4e8")
    version("1.1.24", sha256="1370c9a812b2cf2a7d92802510cca0058cc37e66a7bedd70051f0a34015022a3")
    version("1.1.23", sha256="8a0feb41cef26c97dde382c014e68b9bb335c094bbc1356f6edaaf6b79bd14aa")
    version("1.1.22", sha256="8b0941a48d2f980fd7036cfbd24aa1d414f03d9a0652ecbd5ec5c7ff1bee29e3")
    version("1.1.21", sha256="c742b66f6f49c9e5f52f64d8b79fecb5a0f6e0203fca176c70ca20f6be285f44")
    version("1.1.20", sha256="44be8771d0e6c6b5f82dd15662eb2957c9a3173a19a8b49966ac0542bbd40d61")

    depends_on("c", type="build")  # generated

    def patch(self):
        config = FileFilter("configure")
        if self.compiler.name == "gcc":
            config.filter("WRAPCC_GCC = .*'", "WRAPCC_GCC = {0}'".format(self.compiler.cc))
        elif self.compiler.name in ("clang", "apple-clang"):
            config.filter("WRAPCC_CLANG = .*'", "WRAPCC_CLANG = {0}'".format(self.compiler.cc))

    def configure_args(self):
        args = ["--prefix={0}".format(self.prefix)]
        if self.compiler.name == "gcc":
            args.append("--enable-wrapper=gcc")
        elif self.compiler.name in ("clang", "apple-clang"):
            args.append("--enable-wrapper=clang")
        else:
            args.append("--enable-wrapper=no")
        args.append("--syslibdir={0}".format(self.prefix.lib))
        return args

    def edit(self, spec, prefix):
        configure(*self.configure_args())

    @property
    def libs(self):
        return LibraryList([])

    @property
    def headers(self):
        return HeaderList([])
