# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonLdap(PythonPackage):
    """python-ldap provides an object-oriented API to access LDAP directory
    servers from Python programs.
    """

    homepage = "https://www.python-ldap.org/en/python-ldap-3.2.0/"
    pypi = "python-ldap/python-ldap-3.2.0.tar.gz"

    license("MIT")

    version("3.4.2", sha256="b16470a0983aaf09a00ffb8f40b69a2446f3d0be639a229256bce381fcb268f7")
    version("3.4.0", sha256="60464c8fc25e71e0fd40449a24eae482dcd0fb7fcf823e7de627a6525b3e0d12")
    version("3.3.1", sha256="4711cacf013e298754abd70058ccc995758177fb425f1c2d30e71adfc1d00aa5")
    version("3.2.0", sha256="7d1c4b15375a533564aad3d3deade789221e450052b21ebb9720fb822eccdb8e")
    version("3.0.0", sha256="86746b912a2cd37a54b06c694f021b0c8556d4caeab75ef50435ada152e2fbe1")

    depends_on("c", type="build")  # generated

    # See https://github.com/python-ldap/python-ldap/issues/432
    depends_on("openldap+client_only @:2.4", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("python@3.6:", when="@3.4.2:", type=("build", "run"))
    depends_on("py-pyasn1@0.3.7:", type=("build", "run"))
    depends_on("py-pyasn1-modules@0.1.5:", type=("build", "run"))
    depends_on("cyrus-sasl", type="link", when="^openldap+sasl")

    def patch(self):
        if self.spec.satisfies("^openldap~sasl"):
            filter_file("HAVE_SASL ", "", "setup.cfg")
