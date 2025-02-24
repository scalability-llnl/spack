# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ExternalCommonPython(Package):
    homepage = "http://www.python.org"
    url = "http://www.python.org/ftp/python/3.8.7/Python-3.8.7.tgz"

    version("3.8.7", md5="be78e48cdfc1a7ad90efff146dce6cfe")
    depends_on("external-common-openssl")
    depends_on("external-common-gdbm")
