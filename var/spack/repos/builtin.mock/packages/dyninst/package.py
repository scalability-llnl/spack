# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dyninst(Package):
    homepage = "https://paradyn.org"
    url      = "http://www.paradyn.org/release8.1/DyninstAPI-8.1.1.tgz"

    version('8.2',   'cxyzab',
            url='http://www.paradyn.org/release8.2/DyninstAPI-8.2.tgz')
    version('8.1.2', 'bcxyza',
            url='http://www.paradyn.org/release8.1.2/DyninstAPI-8.1.2.tgz')
    version('8.1.1', 'abcxyz',
            url='http://www.paradyn.org/release8.1/DyninstAPI-8.1.1.tgz')

    depends_on("libelf")
    depends_on("libdwarf")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
