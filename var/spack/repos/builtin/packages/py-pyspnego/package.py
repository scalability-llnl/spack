# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyspnego(PythonPackage):
    """Python SPNEGO authentication library."""

    homepage = "https://github.com/jborean93/pyspnego"
    pypi = "pyspnego/pyspnego-0.11.1.tar.gz"

    maintainers("wdconinc")

    license("MIT", checked_by="wdconinc")

    version("0.11.1", sha256="e92ed8b0a62765b9d6abbb86a48cf871228ddb97678598dc01c9c39a626823f6")

    variant("kerberos", default=False, description="Enable Kerberos authentication on Linux")

    depends_on("py-setuptools@61:", type="build")
    depends_on("py-cryptography", type=("build", "run"))
    depends_on("py-sspilib", type=("build", "run"), when="platform=windows")

    with when("+kerberos"):
        depends_on("py-gssapi@1.6.0:", type=("build", "run"))
        depends_on("py-krb5@0.3.0:", type=("build", "run"))
    conflicts("+kerberos", when="platform=windows", msg="kerberos support unavailable on windows")
