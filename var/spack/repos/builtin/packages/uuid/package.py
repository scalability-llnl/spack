# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Uuid(AutotoolsPackage):
    """OSSP uuid is a ISO-C:1999 application programming interface (API) and
    corresponding command line interface (CLI) for the generation of DCE 1.1,
    ISO/IEC 11578:1996 and RFC 4122 compliant Universally Unique Identifier
    (UUID)."""

    homepage = "http://www.ossp.org/pkg/lib/uuid"
    url = "http://www.mirrorservice.org/sites/ftp.ossp.org/pkg/lib/uuid/uuid-1.6.2.tar.gz"

    version('1.6.2', sha256='11a615225baa5f8bb686824423f50e4427acd3f70d394765bdff32801f0fd5b0')
