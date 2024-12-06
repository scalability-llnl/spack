# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

from spack.package import *


class Gawk(AutotoolsPackage, GNUMirrorPackage):
    """If you are like many computer users, you would frequently like to make
    changes in various text files wherever certain patterns appear, or
    extract data from parts of certain lines while discarding the
    rest. To write a program to do this in a language such as C or
    Pascal is a time-consuming inconvenience that may take many lines
    of code. The job is easy with awk, especially the GNU
    implementation: gawk.

    The awk utility interprets a special-purpose programming language
    that makes it possible to handle simple data-reformatting jobs
    with just a few lines of code.
    """

    homepage = "https://www.gnu.org/software/gawk/"
    gnu_mirror_path = "gawk/gawk-4.1.4.tar.xz"

    executables = ["^gawk$"]

    tags = ["build-tools", "core-packages"]

    license("GPL-3.0-or-later")

    version("5.3.1", sha256="694db764812a6236423d4ff40ceb7b6c4c441301b72ad502bb5c27e00cd56f78")
    version("5.3.0", sha256="ca9c16d3d11d0ff8c69d79dc0b47267e1329a69b39b799895604ed447d3ca90b")
    version("5.2.2", sha256="3c1fce1446b4cbee1cd273bd7ec64bc87d89f61537471cd3e05e33a965a250e9")
    version("5.2.1", sha256="673553b91f9e18cc5792ed51075df8d510c9040f550a6f74e09c9add243a7e4f")
    version("5.1.1", sha256="d87629386e894bbea11a5e00515fc909dc9b7249529dad9e6a3a2c77085f7ea2")
    version("5.1.0", sha256="cf5fea4ac5665fd5171af4716baab2effc76306a9572988d5ba1078f196382bd")
    version("5.0.1", sha256="8e4e86f04ed789648b66f757329743a0d6dfb5294c3b91b756a474f1ce05a794")
    version("4.1.4", sha256="53e184e2d0f90def9207860531802456322be091c7b48f23fdc79cda65adc266")

    depends_on("c", type="build")  # generated

    variant("nls", default=False, description="Enable Native Language Support")

    depends_on("gettext", when="+nls")
    depends_on("libsigsegv")
    depends_on("readline")
    depends_on("mpfr")
    depends_on("gmp")

    provides("awk")

    build_directory = "spack-build"

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"GNU Awk\s+([\d\.]+)", output)
        return match.group(1) if match else None

    def configure_args(self):
        args = self.enable_or_disable("nls")

        # https://github.com/Homebrew/homebrew-core/blob/5b93511fd6b87789871e30c9fe0790949bd6634c/Formula/gawk.rb#L38,L42
        if self.spec.satisfies("platform=darwin target=aarch64:"):
            args.append("--disable-pma")

        return args
