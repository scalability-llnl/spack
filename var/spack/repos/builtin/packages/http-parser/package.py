# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class HttpParser(MakefilePackage):
    """http request/response parser for c"""

    homepage = "https://github.com/nodejs/http-parser"
    url = "https://github.com/nodejs/http-parser/archive/v2.9.4.tar.gz"

    license("MIT")

    version("2.9.4", sha256="467b9e30fd0979ee301065e70f637d525c28193449e1b13fbcb1b1fab3ad224f")
    version("2.9.3", sha256="8fa0ab8770fd8425a9b431fdbf91623c4d7a9cdb842b9339289bd2b0b01b0d3d")
    version("2.9.2", sha256="5199500e352584852c95c13423edc5f0cb329297c81dd69c3c8f52a75496da08")
    version("2.9.1", sha256="33220771208bcacecd970b6de03bebe239374a8e9cf3baeda79b4f3920bede21")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        make("install", "DESTDIR=%s" % prefix, "PREFIX=")
