# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ExternalCommonGdbm(Package):
    homepage = "http://www.gnu.org.ua/software/gdbm/gdbm.html"
    url = "https://ftpmirror.gnu.org/gdbm/gdbm-1.18.1.tar.gz"

    version("1.18.1", md5="be78e48cdfc1a7ad90efff146dce6cfe")
