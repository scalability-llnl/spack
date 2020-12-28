# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    homepage = "http://dev.yorhel.nl/ncdu"
    url      = "http://dev.yorhel.nl/download/ncdu-1.11.tar.gz"

    version('1.13', sha256='f4d9285c38292c2de05e444d0ba271cbfe1a705eee37c2b23ea7c448ab37255a')
    version('1.12', sha256='820e4e4747a2a2ec7a2e9f06d2f5a353516362c22496a10a9834f871b877499a')
    version('1.11', sha256='d0aea772e47463c281007f279a9041252155a2b2349b18adb9055075e141bb7b')
    version('1.10', sha256='f5994a4848dbbca480d39729b021f057700f14ef72c0d739bbd82d862f2f0c67')
    version('1.9', sha256='ea7349544a9da77764293d84e52862110ab49ee29b949158bc4bab908d3dd3a5')
    version('1.8', sha256='42aaf0418c05e725b39b220166a9c604a9c54c0fbf7692c9c119b36d0ed5d099')
    version('1.7', sha256='70dfe10b4c0843050ee17ab27b7ad4d65714682f117079b85d779f83431fb333')

    depends_on("ncurses")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--with-ncurses=%s' % spec['ncurses'])

        make()
        make("install")
