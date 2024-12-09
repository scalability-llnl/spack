# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class SourceHighlight(AutotoolsPackage, GNUMirrorPackage):
    """This program, given a source file, produces a document with syntax
    highlighting. It also provides a C++ highlight library
    (since version 3.0)."""

    homepage = "https://www.gnu.org/software/src-highlite/"
    gnu_mirror_path = "src-highlite/source-highlight-3.1.8.tar.gz"
    git = "https://git.savannah.gnu.org/git/src-highlite.git"

    license("GPL-3.0-or-later")

    version("master", branch="master")
    version("3.1.9", sha256="3a7fd28378cb5416f8de2c9e77196ec915145d44e30ff4e0ee8beb3fe6211c91")
    version("3.1.8", sha256="01336a7ea1d1ccc374201f7b81ffa94d0aecb33afc7d6903ebf9fbf33a55ada3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch(
        "https://git.savannah.gnu.org/cgit/src-highlite.git/"
        + "patch/lib?id=904949c9026cb772dc93fbe0947a252ef47127f4",
        sha256="45087b174b2b128a8dc81b0728f8ae63213d255ceef6dabfcba27c94e2a75ce9",
        when="%gcc@11:",
    )

    depends_on("boost+exception+regex")

    # git version needs autotools
    depends_on("m4", when="@master")
    depends_on("autoconf", when="@master")
    depends_on("automake", when="@master")
    depends_on("libtool", when="@master")
    depends_on("texinfo", when="@master")

    def configure_args(self):
        args = ["--with-boost={0}".format(self.spec["boost"].prefix)]
        return args
