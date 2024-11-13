# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Watch(AutotoolsPackage):
    """Executes a program periodically, showing output fullscreen."""

    # Note: there is a separate procps package, but it doesn't build on macOS.
    # This package only contains the `watch` program, a subset of procps which
    # does build on macOS.
    # https://github.com/NixOS/nixpkgs/issues/18929#issuecomment-249388571
    homepage = "https://gitlab.com/procps-ng/procps"
    git = "https://gitlab.com/procps-ng/procps.git"

    license("GPL-2.0-or-later")

    version("master", branch="master")
    version("3.3.15", tag="v3.3.15", commit="7bb949bcba13c107fa0f45d2d0298b1ad6b6d6cc")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig@0.9.0:", type="build")
    depends_on("gettext", type="build")
    depends_on("ncurses")

    # https://github.com/Homebrew/homebrew-core/blob/master/Formula/watch.rb
    def autoreconf(self, spec, prefix):
        sh = which("sh")
        sh("autogen.sh")

    def configure_args(self):
        return [
            "--with-ncurses",
            # Required to avoid libintl linking errors
            "--disable-nls",
        ]

    def build(self, spec, prefix):
        make("watch")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.man.man1)

        install("watch", prefix.bin)
        install("watch.1", prefix.man.man1)
