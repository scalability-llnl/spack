# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ncdu(Package):
    """Ncdu is a disk usage analyzer with an ncurses interface. It is designed
    to find space hogs on a remote server where you don't have an entire
    gaphical setup available, but it is a useful tool even on regular desktop
    systems. Ncdu aims to be fast, simple and easy to use, and should be able
    to run in any minimal POSIX-like environment with ncurses installed.
    """

    homepage = "https://dev.yorhel.nl/ncdu"
    url = "https://dev.yorhel.nl/download/ncdu-1.11.tar.gz"

    license("MIT")

    version("1.19", sha256="30363019180cde0752c7fb006c12e154920412f4e1b5dc3090654698496bb17d")
    version("1.18.1", sha256="7c0fa1eb29d85aaed4ba174164bdbb8f011b5c390d017c57d668fc7231332405")
    version("1.17", sha256="810745a8ed1ab3788c87d3aea4cc1a14edf6ee226f764bcc383e024ba56adbf1")
    version("1.16", sha256="2b915752a183fae014b5e5b1f0a135b4b408de7488c716e325217c2513980fd4")
    version("1.15.1", sha256="b02ddc4dbf1db139cc6fbbe2f54a282770380f0ca5c17089855eab52a9ea3fb0")
    version("1.14.2", sha256="947a7f5c1d0cd4e338e72b4f5bc5e2873651442cec3cb012e04ad2c37152c6b1")
    version("1.13", sha256="f4d9285c38292c2de05e444d0ba271cbfe1a705eee37c2b23ea7c448ab37255a")
    version("1.12", sha256="820e4e4747a2a2ec7a2e9f06d2f5a353516362c22496a10a9834f871b877499a")
    version("1.11", sha256="d0aea772e47463c281007f279a9041252155a2b2349b18adb9055075e141bb7b")
    version("1.10", sha256="f5994a4848dbbca480d39729b021f057700f14ef72c0d739bbd82d862f2f0c67")
    version("1.9", sha256="ea7349544a9da77764293d84e52862110ab49ee29b949158bc4bab908d3dd3a5")
    version("1.8", sha256="42aaf0418c05e725b39b220166a9c604a9c54c0fbf7692c9c119b36d0ed5d099")
    version("1.7", sha256="70dfe10b4c0843050ee17ab27b7ad4d65714682f117079b85d779f83431fb333")

    depends_on("c", type="build")  # generated

    depends_on("ncurses")
    depends_on("pkgconfig", type="build")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix, "--with-ncurses=%s" % spec["ncurses"])

        make()
        make("install")
