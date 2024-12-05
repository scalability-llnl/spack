# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLdap3(PythonPackage):
    """A strictly RFC 4510 conforming LDAP V3 pure Python client library."""

    homepage = "https://github.com/cannatag/ldap3"
    pypi = "ldap3/ldap3-2.9.1.tar.gz"

    maintainers("LydDeb")

    license("LGPL-3.0-or-later")

    version("2.9.1", sha256="f3e7fc4718e3f09dda568b57100095e0ce58633bcabbed8667ce3f8fbaa4229f")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyasn1@0.4.6:", type=("build", "run"))
