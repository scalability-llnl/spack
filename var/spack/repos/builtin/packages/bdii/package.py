# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bdii(MakefilePackage):
    """The Berkeley Database Information Index (BDII) consists of a
    standard LDAP database which is updated by an external process.
    The update process obtains LDIF from a number of sources and merges
    them. It then compares this to the contents of the database and
    creates an LDIF file of the differences. This is then used to
    update the database."""

    homepage = "https://github.com/EGI-Foundation/bdii"
    url = "https://github.com/EGI-Foundation/bdii/archive/v5.2.25.tar.gz"

    license("Apache-2.0")

    version("6.0.1", sha256="ac292559004881c4d5254517207a5da82d7a48af746194a380145dcedef507ce")
    version("5.2.25", sha256="6abc3ed872538a12dc470a1d30bf4ae1ca4d6302eb6b50370413940f9e9259ca")
    version("5.2.24", sha256="5d09ed06b8b09ce372b3489fab93e25302f68ca80d8fcc600c2535648c861a3a")

    depends_on("openldap", type="run")

    def install(self, spec, prefix):
        make("prefix={0}".format(prefix), "install")
