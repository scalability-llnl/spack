# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Grep(AutotoolsPackage):
    """Grep searches one or more input files for lines containing a match to
    a specified pattern"""

    homepage = "https://www.gnu.org/software/grep/"
    url = "https://ftp.gnu.org/gnu/grep/grep-3.3.tar.xz"

    license("GPL-3.0-or-later")

    version("3.11", sha256="1db2aedde89d0dea42b16d9528f894c8d15dae4e190b59aecc78f5a951276eab")
    version("3.10", sha256="24efa5b595fb5a7100879b51b8868a0bb87a71c183d02c4c602633b88af6855b")
    version("3.9", sha256="abcd11409ee23d4caf35feb422e53bbac867014cfeed313bb5f488aca170b599")
    version("3.7", sha256="5c10da312460aec721984d5d83246d24520ec438dd48d7ab5a05dbc0d6d6823c")
    version("3.3", sha256="b960541c499619efd6afe1fa795402e4733c8e11ebf9fafccc0bb4bccdc5b514")

    depends_on("c", type="build")  # generated

    variant("pcre", default=False, description="Enable Perl Compatible Regular Expression support")

    build_directory = "spack-build"

    depends_on("pcre2", when="@3.8:+pcre")
    depends_on("pcre", when="@:3.7+pcre")

    def configure_args(self):
        args = []

        if self.spec.satisfies("+pcre"):
            args.append("--enable-perl-regexp")
        else:
            args.append("--disable-perl-regexp")

        return args
