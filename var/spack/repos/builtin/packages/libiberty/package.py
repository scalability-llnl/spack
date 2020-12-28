# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


# Libiberty has two homes: binutils and gcc.  This package uses the
# binutils tarfile but only builds the libiberty subdirectory.  This
# is useful for other packages that want the demangling functions
# without the rest of binutils.

class Libiberty(AutotoolsPackage, GNUMirrorPackage):
    """The libiberty.a library from GNU binutils.  Libiberty provides
    demangling and support functions for the GNU toolchain."""

    homepage = "https://www.gnu.org/software/binutils/"
    gnu_mirror_path = "binutils/binutils-2.31.1.tar.xz"
    maintainers = ['mwkrentel']

    version('2.33.1', sha256='ab66fc2d1c3ec0359b8e08843c9f33b63e8707efdff5e4cc5c200eae24722cbf')
    version('2.32',   sha256='0ab6c55dd86a92ed561972ba15b9b70a8b9f75557f896446c82e8b36e473ee04')
    version('2.31.1', sha256='5d20086ecf5752cc7d9134246e9588fa201740d540f7eb84d795b1f7a93bca86')
    version('2.30',   sha256='6e46b8aeae2f727a36f0bd9505e405768a72218f1796f0d09757d45209871ae6')
    version('2.29.1', sha256='e7010a46969f9d3e53b650a518663f98a5dde3c3ae21b7d71e5e6803bc36b577')
    version('2.28.1', sha256='16328a906e55a3c633854beec8e9e255a639b366436470b4f6245eb0d2fde942')

    variant('pic', default=False,
            description='Compile with position independent code.')

    # Configure and build just libiberty.
    configure_directory = 'libiberty'

    # Set default cflags (-g -O2), add -fPIC if requested, and move to
    # the configure line.
    def flag_handler(self, name, flags):
        if name != 'cflags':
            return (flags, None, None)

        if '-g' not in flags:
            flags.append('-g')

        for flag in flags:
            if flag.startswith('-O'):
                break
        else:
            flags.append('-O2')

        if '+pic' in self.spec:
            flags.append(self.compiler.cc_pic_flag)

        return (None, None, flags)

    def configure_args(self):
        args = ['--enable-install-libiberty']
        return args
