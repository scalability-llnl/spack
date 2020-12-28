# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import datetime

from spack.package import *


class HttpPost(MakefilePackage):
    """Http_post does a POST operation to an HTTP URL and dumps the results
    to stdout. It does not do gopher, ftp, file, news, or any other type of
    URL, only HTTP. It can be configured to do HTTPS POSTs as well."""

    homepage = "http://www.acme.com/software/http_post/"
    url      = "http://www.acme.com/software/http_post/http_post_18May2018.tar.gz"

    version('2018-05-18', sha256='981c62bcc5cd12b8531f887b3e3779a63a7b7f370062575cded412865a20ea2c')

    def url_for_version(self, version):
        ver = datetime.datetime.strptime(str(version), '%Y-%m-%d').date()
        verstr = datetime.datetime.strftime(ver, '%d%b%Y')
        return "http://www.acme.com/software/http_post/http_post_{0}.tar.gz".format(verstr)

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
