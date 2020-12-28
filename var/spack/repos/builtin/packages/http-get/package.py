# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import datetime

from spack.package import *


class HttpGet(MakefilePackage):
    """Http_get fetches an HTTP URL and dumps the contents to stdout.
    It does not do gopher, ftp, file, news, or any other type of URL,
    only HTTP. It can be configured to do HTTPS fetches as well."""

    homepage = "http://www.acme.com/software/http_get/"
    url      = "http://www.acme.com/software/http_get/http_get_23May2018.tar.gz"

    version('2018-05-23', sha256='7d46ce25e53b6d3e27a99c1853c3054a046cc97d5e30a713a7ec986cfe7c4fe0')

    def url_for_version(self, version):
        ver = datetime.datetime.strptime(str(version), '%Y-%m-%d').date()
        verstr = datetime.datetime.strftime(ver, '%d%b%Y')
        return "http://www.acme.com/software/http_get/http_get_{0}.tar.gz".format(verstr)

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
