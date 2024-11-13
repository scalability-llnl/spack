# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os

from spack.package import *


class Nauty(AutotoolsPackage):
    """nauty and Traces are programs for computing automorphism groups of
    graphsq and digraphs"""

    homepage = "https://pallini.di.uniroma1.it/index.html"
    url = "https://pallini.di.uniroma1.it//nauty26r7.tar.gz"

    license("Apache-2.0")

    version("2.6r7", sha256="97b5648de17645895cbd56a9a0b3e23cf01f5332c476d013ea459f1a0363cdc6")

    depends_on("c", type="build")  # generated

    # Debian/ Fedora patches for @2.6r7:
    urls_for_patches = {
        "@2.6r7": [
            # Debian patch to fix the gt_numorbits declaration
            (
                "https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-fix-gt_numorbits.patch",
                "c8e4546a7b262c92cee226beb1dc71d87d644b115375e9c8550598efcc00254f",
            ),
            # Debian patch to add explicit extern declarations where needed
            (
                "https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-fix-include-extern.patch",
                "c52c62e4dc46532ad89632a3f59a9faf13dd7988e9ef29fc5e5b2a3e17449bb6",
            ),
            # Debian patch to use zlib instead of invoking zcat through a pipe
            (
                "https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-zlib-blisstog.patch",
                "b1210bfb41ddbeb4c956d660266f62e806026a559a4700ce78024a9db2b82168",
            ),
            # Debian patch to improve usage and help information
            (
                "https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-help2man.patch",
                "c11544938446a3eca70d55b0f1084ce56fb1fb415db1ec1b5a69fd310a02b16c",
            ),
            # Debian patch to add libtool support for building a shared library
            (
                "https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-autotoolization.patch",
                "7f60ae3d8aeee830306db991c908efae461f103527a7899ce79d936bb15212b5",
            ),
            # Debian patch to canonicalize header file usage
            (
                "https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-includes.patch",
                "9a305f0cd3f1136a9885518bd7912c669d1ca4b2b43bd039d6fc5535b9679778",
            ),
            # Debian patch to prefix "nauty-" to the names of the generic tools
            (
                "https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-tool-prefix.patch",
                "736266813a62b3151e0b81ded6578bd0f53f03fc8ffbc54c7c2a2c64ac07b25f",
            ),
            # Fedora patch to detect availability of the popcnt
            # instruction at runtime
            (
                "https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-popcnt.patch",
                "0dc2e0374491dddf5757f0717d0ea3f949f85b540202385662f10c358b4a08e8",
            ),
        ]
    }
    # Iterate over patches
    for condition, url_and_sha256 in urls_for_patches.items():
        for path, sha256 in url_and_sha256:
            patch(path, when=condition, level=1, sha256=sha256)

    depends_on("m4", type="build", when="@2.6r7")
    depends_on("autoconf", type="build", when="@2.6r7")
    depends_on("automake", type="build", when="@2.6r7")
    depends_on("libtool", type="build", when="@2.6r7")
    depends_on("pkgconfig", type="build")
    depends_on("help2man", type="build")
    depends_on("zlib-api")
    depends_on("gmp")

    @property
    def force_autoreconf(self):
        return self.spec.satisfies("@2.6r7")

    def url_for_version(self, version):
        url = "https://pallini.di.uniroma1.it//nauty{0}.tar.gz"
        return url.format(version.joined)

    def patch(self):
        os.remove("makefile")
        ver = str(self.version.dotted).replace("r", ".")
        if self.spec.satisfies("@2.6r7"):
            filter_file("@INJECTVER@", ver, "configure.ac")
