# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpfr(AutotoolsPackage, GNUMirrorPackage):
    """The MPFR library is a C library for multiple-precision
    floating-point computations with correct rounding."""

    homepage = "https://www.mpfr.org/"
    gnu_mirror_path = "mpfr/mpfr-4.0.2.tar.bz2"

    maintainers("cessenat")

    license("LGPL-3.0-or-later")

    version("4.2.1", sha256="b9df93635b20e4089c29623b19420c4ac848a1b29df1cfd59f26cab0d2666aa0")
    version("4.2.0", sha256="691db39178e36fc460c046591e4b0f2a52c8f2b3ee6d750cc2eab25f1eaa999d")
    version("4.1.1", sha256="85fdf11614cc08e3545386d6b9c8c9035e3db1e506211a45f4e108117fe3c951")
    version("4.1.0", sha256="feced2d430dd5a97805fa289fed3fc8ff2b094c02d05287fd6133e7f1f0ec926")
    version("4.0.2", sha256="c05e3f02d09e0e9019384cdd58e0f19c64e6db1fd6f5ecf77b4b1c61ca253acc")
    version("4.0.1", sha256="a4d97610ba8579d380b384b225187c250ef88cfe1d5e7226b89519374209b86b")
    version("4.0.0", sha256="6aa31fbf3bd1f9f95bcfa241590a9d11cb0f874e2bb93b99c9e2de8eaea6d5fd")
    version("3.1.6", sha256="cf4f4b2d80abb79e820e78c8077b6725bbbb4e8f41896783c899087be0e94068")
    version("3.1.5", sha256="ca498c1c7a74dd37a576f353312d1e68d490978de4395fa28f1cbd46a364e658")
    version("3.1.4", sha256="d3103a80cdad2407ed581f3618c4bed04e0c92d1cf771a65ead662cc397f7775")
    version("3.1.3", sha256="f63bb459157cacd223caac545cb816bcdb5a0de28b809e7748b82e9eb89b0afd")
    version("3.1.2", sha256="79c73f60af010a30a5c27a955a1d2d01ba095b72537dab0ecaad57f5a7bb1b6b")

    depends_on("c", type="build")  # generated

    # mpir is a drop-in replacement for gmp
    depends_on("gmp@4.1:")  # 4.2.3 or higher is recommended
    depends_on("gmp@5.0:", when="@4.0.0:")  # https://www.mpfr.org/mpfr-4.0.0/

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("autoconf-archive", when="@4.0.0:", type="build")
    depends_on("texinfo", when="@4.1.0:", type="build")

    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )

    force_autoreconf = True

    # Check the Bugs section of old release pages for patches.
    # https://www.mpfr.org/mpfr-X.Y.Z/#bugs
    patches = {
        "4.0.2": "3f80b836948aa96f8d1cb9cc7f3f55973f19285482a96f9a4e1623d460bcccf0",
        "4.0.1": "5230aab653fa8675fc05b5bdd3890e071e8df49a92a9d58c4284024affd27739",
        "3.1.6": "7a6dd71bcda4803d6b89612706a17b8816e1acd5dd9bf1bec29cf748f3b60008",
        "3.1.5": "1ae14fb3a54ae8e0faed20801970255b279eee9e5ac624891ab5d29727f0bc04",
        "3.1.4": "113705d5333ef0d0ad3eb136a85404ba6bd1cc524dece5ce902c536aa2e29903",
        "3.1.3": "4152a780b3cc6e9643283e59093b43460196d0fea9302d8c93b2496f6679f4e4",
        "3.1.2": "1b9fdb515efb09a506a01e1eb307b1464455f5ca63d6c193db3a3da371ab3220",
    }

    for ver, checksum in patches.items():
        patch(
            "https://www.mpfr.org/mpfr-{0}/allpatches".format(ver), when="@" + ver, sha256=checksum
        )

    def flag_handler(self, name, flags):
        # Work around macOS Catalina / Xcode 11 code generation bug
        # (test failure t-toom53, due to wrong code in mpn/toom53_mul.o)
        if self.spec.satisfies("os=catalina") and name == "cflags":
            flags.append("-fno-stack-check")
        return (flags, None, None)

    def configure_args(self):
        args = ["--with-gmp=" + self.spec["gmp"].prefix]
        args += self.enable_or_disable("libs")
        if "libs=static" in self.spec:
            args.append("--with-pic")
        return args
