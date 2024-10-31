# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
    maintainers("mwkrentel")

    license("LGPL-2.0-or-later")

    version("2.41", sha256="ae9a5789e23459e59606e6714723f2d3ffc31c03174191ef0d015bdf06007450")
    version("2.40", sha256="0f8a4c272d7f17f369ded10a4aca28b8e304828e95526da482b0ccc4dfc9d8e1")
    version("2.37", sha256="820d9724f020a3e69cb337893a0b63c2db161dadcb0e06fc11dc29eb1e84a32c")
    version("2.36.1", sha256="e81d9edf373f193af428a0f256674aea62a9d74dfe93f65192d4eae030b0f3b0")
    version("2.36", sha256="5788292cc5bbcca0848545af05986f6b17058b105be59e99ba7d0f9eb5336fb8")
    version("2.35.2", sha256="dcd5b0416e7b0a9b24bed76cd8c6c132526805761863150a26d016415b8bdc7b")
    version("2.35.1", sha256="3ced91db9bf01182b7e420eab68039f2083aed0a214c0424e257eae3ddee8607")
    version("2.35", sha256="1b11659fb49e20e18db460d44485f09442c8c56d5df165de9461eb09c8302f85")
    version("2.34", sha256="f00b0e8803dc9bab1e2165bd568528135be734df3fabf8d0161828cd56028952")
    version("2.33.1", sha256="ab66fc2d1c3ec0359b8e08843c9f33b63e8707efdff5e4cc5c200eae24722cbf")
    version("2.32", sha256="0ab6c55dd86a92ed561972ba15b9b70a8b9f75557f896446c82e8b36e473ee04")
    version("2.31.1", sha256="5d20086ecf5752cc7d9134246e9588fa201740d540f7eb84d795b1f7a93bca86")
    version("2.30", sha256="6e46b8aeae2f727a36f0bd9505e405768a72218f1796f0d09757d45209871ae6")
    version("2.29.1", sha256="e7010a46969f9d3e53b650a518663f98a5dde3c3ae21b7d71e5e6803bc36b577")
    version("2.28.1", sha256="16328a906e55a3c633854beec8e9e255a639b366436470b4f6245eb0d2fde942")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("pic", default=False, description="Compile with position independent code.")

    # Configure and build just libiberty.
    configure_directory = "libiberty"

    # Set default cflags (-g -O2), add -fPIC if requested, and move to
    # the configure line.
    def flag_handler(self, name, flags):
        if name != "cflags":
            return (flags, None, None)

        if "-g" not in flags:
            flags.append("-g")

        for flag in flags:
            if flag.startswith("-O"):
                break
        else:
            flags.append("-O2")

        if self.spec.satisfies("+pic"):
            flags.append(self.compiler.cc_pic_flag)

        return (None, None, flags)

    def configure_args(self):
        args = ["--enable-install-libiberty"]
        return args
