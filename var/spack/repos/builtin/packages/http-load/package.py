# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import datetime

from spack.package import *


class HttpLoad(MakefilePackage):
    """http_load - multiprocessing http test client"""

    homepage = "http://www.acme.com/software/http_load/"
    url      = "http://www.acme.com/software/http_load/http_load-09Mar2016.tar.gz"

    version('2016-03-09', sha256='a2bf118d88f6acd2a082cbf275d141538149caaa0a4ce1bcc66680668e781306')

    def url_for_version(self, version):
        ver = datetime.datetime.strptime(str(version), '%Y-%m-%d').date()
        verstr = datetime.datetime.strftime(ver, '%d%b%Y')
        return "http://www.acme.com/software/http_load/http_load-{0}.tar.gz".format(verstr)

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("BINDIR =\t/usr/local/bin",
                        "BINDIR =    {0}/bin".format(self.prefix))
        makefile.filter("MANDIR =\t/usr/local/man/man1",
                        "MANDIR={0}/man/man1".format(self.prefix))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.man.man1)
        make('install')
