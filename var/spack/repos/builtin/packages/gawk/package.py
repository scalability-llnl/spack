# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    version('5.0.1', sha256='8e4e86f04ed789648b66f757329743a0d6dfb5294c3b91b756a474f1ce05a794')
    version('4.1.4', sha256='53e184e2d0f90def9207860531802456322be091c7b48f23fdc79cda65adc266')

    depends_on('gettext')
    depends_on('libsigsegv')
    depends_on('readline')
    depends_on('mpfr')
    depends_on('gmp')

    provides('awk')

    build_directory = 'spack-build'
