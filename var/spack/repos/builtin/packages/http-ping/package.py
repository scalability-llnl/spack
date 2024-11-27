# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import datetime

from spack.package import *


class HttpPing(MakefilePackage):
    """http_ping is like the regular ping command, except that it sends
    HTTP requests instead of ICMP echo requests."""

    homepage = "https://www.acme.com/software/http_ping/"
    url = "https://www.acme.com/software/http_ping/http_ping_09Mar2016.tar.gz"

    version(
        "2016-03-09", sha256="f8b95773aaed09839a44a1927f979a62752d57aace79da3846bfb73e6c9805e9"
    )

    depends_on("c", type="build")  # generated

    def url_for_version(self, version):
        ver = datetime.datetime.strptime(str(version), "%Y-%m-%d").date()
        verstr = datetime.datetime.strftime(ver, "%d%b%Y")
        return "https://www.acme.com/software/http_ping/http_ping_{0}.tar.gz".format(verstr)

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("BINDIR =\t/usr/local/bin", "BINDIR =    {0}/bin".format(self.prefix))
        makefile.filter("MANDIR =\t/usr/local/man/man1", "MANDIR={0}/man/man1".format(self.prefix))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.man.man1)
        make("install")
