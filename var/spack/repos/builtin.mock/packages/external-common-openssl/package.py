# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ExternalCommonOpenssl(Package):
    homepage = "http://www.openssl.org"
    url      = "http://www.openssl.org/source/openssl-1.1.1i.tar.gz"

    version('1.1.1i', 'be78e48cdfc1a7ad90efff146dce6cfe')
    depends_on('external-common-perl')
