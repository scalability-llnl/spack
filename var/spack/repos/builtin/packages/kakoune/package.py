# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kakoune(MakefilePackage):
    """mawww's experiment for a better code editor."""

    homepage = "https://www.kakoune.org"
    url = (
        "https://github.com/mawww/kakoune/releases/download/v2021.11.08/kakoune-2021.11.08.tar.bz2"
    )

    maintainers("Bambi", "taliaferro")

    license("Unlicense")

    version(
        "2024.05.18", sha256="dae8ac2e61d21d9bcd10145aa70b421234309a7b0bc57fad91bc34dbae0cb9fa"
    )
    version(
        "2024.05.09", sha256="2190bddfd3af590c0593c38537088976547506f47bd6eb6c0e22350dbd16a229"
    )
    version(
        "2023.08.05", sha256="3e45151e0addd3500de2d6a29b5aacf2267c42bb256d44a782e73defb29cda5c"
    )
    version(
        "2021.11.08", sha256="aa30889d9da11331a243a8f40fe4f6a8619321b19217debac8f565e06eddb5f4"
    )

    depends_on("cxx", type="build")  # generated

    depends_on("ncurses")

    conflicts("%gcc@:8", when="@2021.11.08", msg="GCC version must be at least 9.0!")
    conflicts("%gcc@:10.2", when="@2023.08.05", msg="GCC version must be at least 10.3!")
    conflicts("%llvm@:10", when="@2023.08.05", msg="Clang version must be at least 11!")

    build_targets = ["all", "man"]

    @property
    def install_targets(self):
        return ["-e", f"PREFIX={prefix}", "installdirs", "install"]
