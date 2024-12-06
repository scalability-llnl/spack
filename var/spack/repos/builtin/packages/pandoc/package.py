# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class Pandoc(Package):
    """If you need to convert files from one markup format into another, pandoc
    is your swiss-army knife."""

    homepage = "https://pandoc.org"

    # The following installs the binaries for pandoc and pandoc-citeproc. The
    # reason for installing binaries is that pandoc is a Haskell package and
    # the Haskell framework is not yet in Spack. See #1408 for a discussion of
    # the challenges with Haskell. Until the Haskell framework is in Spack this
    # package will meet the needs of packages that have a dependency on pandoc.

    skip_version_audit = ["platform=windows"]

    if platform.system() == "Linux" and platform.machine() == "aarch64":
        url = "https://github.com/jgm/pandoc/releases/download/2.14.0.3/pandoc-2.14.0.3-linux-arm64.tar.gz"
        version(
            "2.19.2", sha256="43f364915b9da64905fc3f6009f5542f224e54fb24f71043ef5154540f1a3983"
        )
        version(
            "2.14.0.3", sha256="1212e528fb717e0ffa6662d4930640abdbe0c36d14d283560a9688c8403bf34c"
        )

    elif platform.system() == "Linux":
        url = "https://github.com/jgm/pandoc/releases/download/2.14.0.3/pandoc-2.14.0.3-linux-amd64.tar.gz"

        version(
            "2.19.2", sha256="9d55c7afb6a244e8a615451ed9cb02e6a6f187ad4d169c6d5a123fa74adb4830"
        )
        version(
            "2.14.0.3", sha256="3ed8bf98126fb68fa6ce05861ab866f5100edc38bcf47bc0bb000692453344c0"
        )
        version(
            "2.11.4", sha256="b15ce6009ab833fb51fc472bf8bb9683cd2bd7f8ac948f3ddeb6b8f9a366d69a"
        )
        version(
            "2.7.3",
            sha256="eb775fd42ec50329004d00f0c9b13076e707cdd44745517c8ce2581fb8abdb75",
            url="https://github.com/jgm/pandoc/releases/download/2.7.3/pandoc-2.7.3-linux.tar.gz",
        )

    elif platform.system() == "Darwin":
        url = "https://github.com/jgm/pandoc/releases/download/2.14.0.3/pandoc-2.14.0.3-macOS.zip"

        version(
            "2.19.2", sha256="af0cda69e31e42f01ba6adc0aa779d3e5853e6c092beeb420a4fc22712d2110b"
        )
        version(
            "2.14.0.3", sha256="c6c1addd968699733c7d597cf269cc66d692371995703c32e5262f84a125c27b"
        )
        version(
            "2.11.4", sha256="13b8597860afa6ab802993a684b340be3f31f4d2a06c50b6601f9e726cf76f71"
        )
        version("2.7.3", sha256="fb93800c90f3fab05dbd418ee6180d086b619c9179b822ddfecb608874554ff0")

    variant("texlive", default=False, description="Use TeX Live to enable PDF output")

    conflicts("target=aarch64:", msg="aarch64 is not supported.", when="@:2.11")

    depends_on("texlive", when="+texlive")

    def install(self, spec, prefix):
        install_tree(".", prefix)
