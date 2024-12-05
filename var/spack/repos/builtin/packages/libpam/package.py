# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libpam(AutotoolsPackage):
    """Example PAM module demonstrating two-factor authentication for
    logging into servers via SSH, OpenVPN, etc"""

    homepage = "https://github.com/google/google-authenticator-libpam"
    url = "https://github.com/google/google-authenticator-libpam/archive/1.09.tar.gz"

    license("Apache-2.0")

    version("1.09", sha256="ab1d7983413dc2f11de2efa903e5c326af8cb9ea37765dacb39949417f7cd037")
    version("1.08", sha256="6f6d7530261ba9e2ece84214f1445857d488b7851c28a58356b49f2d9fd36290")
    version("1.07", sha256="104a158e013585e20287f8d33935e93c711b96281e6dda621a5c19575d0b0405")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("linux-pam")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./bootstrap.sh")
