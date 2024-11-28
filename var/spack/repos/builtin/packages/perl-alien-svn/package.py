# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PerlAlienSvn(PerlPackage):
    """Perl SVN extension."""

    homepage = "https://metacpan.org/source/MSCHWERN/Alien-SVN-v1.8.11.0"
    url = "https://cpan.metacpan.org/authors/id/M/MS/MSCHWERN/Alien-SVN-v1.8.11.0.tar.gz"

    version("1.8.11.0", sha256="acf8ebce1cb6958ef24611a453abee32b8e4dfe767563834362891ef3f30fc68")
    version("1.7.19.0", sha256="80df1eef9ffb7b0fb0c45285eec05d15bcb45c349c441f97131c64b8697dceb0")
    version("1.7.17.1", sha256="35ae83fda2ef9a5b48012ac8317ec063058d1e9fc5f2719fa141eecedf6baef8")
    version("1.7.17.0", sha256="f3e11ac89453e91f9c298c43958f8115bbb49cb67bb22a0e92690a8e8447c3d0")
    version("1.7.3.1", sha256="e85efca8f9519b2cef81f39e026d227c077c9531c41f44995b31550c3af02366")
    version("1.7.3.0", sha256="02abbe17ad7db912001e6f1c5018cec08c3840e0c32700363a79274e144e74e5")
    version("1.6.12.1", sha256="a89d8eeff61e34aa7b3d35dee3e6752b12dfa5f0f04bf69d796846cf0391f53d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("perl-module-build", type="build")
    depends_on("apr@1.6.2", type="build")
    depends_on("apr-util", type=("build", "link"))
    depends_on("sqlite", type="build")
    depends_on("zlib-api")
    depends_on("libbsd")

    def setup_build_environment(self, env):
        # non-interactive build, use defaults
        env.set("PERL_MM_USE_DEFAULT", "1")

    def setup_run_environment(self, env):
        # SVN libs are not RPATHed correctly...
        # TODO: extend to other plaforms
        if sys.platform.startswith("linux"):
            env.prepend_path(
                "LD_LIBRARY_PATH",
                join_path(
                    self.prefix, "lib", "perl4", "x86_64-linux-thread-multi", "Alien", "SVN"
                ),
            )
