# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Musl(Package):
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
    url      = "https://www.musl-libc.org/releases/musl-1.1.23.tar.gz"

    version('1.1.23', sha256='8a0feb41cef26c97dde382c014e68b9bb335c094bbc1356f6edaaf6b79bd14aa')
    version('1.1.22', sha256='8b0941a48d2f980fd7036cfbd24aa1d414f03d9a0652ecbd5ec5c7ff1bee29e3')
    version('1.1.21', sha256='c742b66f6f49c9e5f52f64d8b79fecb5a0f6e0203fca176c70ca20f6be285f44')
    version('1.1.20', sha256='44be8771d0e6c6b5f82dd15662eb2957c9a3173a19a8b49966ac0542bbd40d61')

    phases = ['configure', 'build', 'install']

    def patch(self):
        config = FileFilter('configure')
        if self.compiler.name == 'gcc':
            config.filter("WRAPCC_GCC = .*'", "WRAPCC_GCC = {0}'".
                          format(self.compiler.cc))
        elif self.compiler.name in ('clang', 'apple-clang'):
            config.filter("WRAPCC_CLANG = .*'", "WRAPCC_CLANG = {0}'".
                          format(self.compiler.cc))

    def configure_args(self):
        args = ['--prefix={0}'.format(self.prefix)]
        if self.compiler.name == 'gcc':
            args.append('--enable-wrapper=gcc')
        elif self.compiler.name in ('clang', 'apple-clang'):
            args.append('--enable-wrapper=clang')
        else:
            args.append('--enable-wrapper=no')
        return args

    def configure(self, spec, prefix):
        configure(*self.configure_args())

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make('install')
