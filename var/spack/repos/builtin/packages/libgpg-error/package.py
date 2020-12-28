# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibgpgError(AutotoolsPackage):
    """Common error values for all GnuPG components."""

    homepage = "https://www.gnupg.org/related_software/libgpg-error/index.en.html"
    url      = "https://gnupg.org/ftp/gcrypt/libgpg-error/libgpg-error-1.37.tar.bz2"

    version('1.37', sha256='b32d6ff72a73cf79797f7f2d039e95e9c6f92f0c1450215410840ab62aea9763')
    version('1.36', sha256='babd98437208c163175c29453f8681094bcaf92968a15cafb1a276076b33c97c')
    version('1.27', sha256='4f93aac6fecb7da2b92871bb9ee33032be6a87b174f54abf8ddf0911a22d29d2')
    version('1.21', sha256='b7dbdb3cad63a740e9f0c632a1da32d4afdb694ec86c8625c98ea0691713b84d')
    version('1.18', sha256='9ff1d6e61d4cef7c1d0607ceef6d40dc33f3da7a3094170c3718c00153d80810')

    depends_on('awk', type=('build'))
    # Patch for using gawk@5, c.f. https://dev.gnupg.org/T4459
    patch('awk-5.patch', when='@1.36^gawk@5:')

    def configure_args(self):
        args = ['--enable-static']

        if self.run_tests:
            args.append('--enable-tests')
        else:
            args.append('--disable-tests')

        return args
