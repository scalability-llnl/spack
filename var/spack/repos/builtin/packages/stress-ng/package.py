# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class StressNg(MakefilePackage):
    """stress-ng will stress test a computer system in various
    selectable ways. It was designed to exercise various physical
    subsystems of a computer as well as the various operating system
    kernel interfaces."""

    homepage = "https://kernel.ubuntu.com/~cking/stress-ng/"
    url = "https://kernel.ubuntu.com/~cking/tarballs/stress-ng/stress-ng-0.12.06.tar.xz"

    license("GPL-2.0-or-later")

    version("0.12.06", sha256="75eb340266b1bbae944d8f9281af978bd5bc2c8085df97a098d5500d6f177296")

    depends_on("libaio")
    depends_on("libbsd")
    depends_on("judy")
    depends_on("libatomic-ops")
    depends_on("zlib-api")
    depends_on("keyutils")
    depends_on("libgcrypt")
    depends_on("libcap")

    conflicts("platform=darwin", msg="stress-ng is linux-only")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdirp(prefix.man.man1)
        mkdirp(join_path(prefix.share, "stress-ng", "example-jobs"))
        mkdirp(join_path(prefix.share, "bash-completion", "completions"))
        install("stress-ng", prefix.bin)
        install("stress-ng.1", prefix.man.man1)
        install_tree("example-jobs", join_path(prefix.share, "stress-ng"))
        install(
            "bash-completion/stress-ng", join_path(prefix.share, "bash-completion", "completions")
        )
