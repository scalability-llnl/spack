# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPykerberos(PythonPackage):
    """This Python package is a high-level wrapper for Kerberos (GSSAPI) operations."""

    homepage = "https://github.com/02strich/pykerberos"
    pypi = "pykerberos/pykerberos-1.2.4.tar.gz"

    license("Apache-2.0")

    version("1.2.4", sha256="9d701ebd8fc596c99d3155d5ba45813bd5908d26ef83ba0add250edb622abed4")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")

    depends_on("krb5", type=("build", "link"))
