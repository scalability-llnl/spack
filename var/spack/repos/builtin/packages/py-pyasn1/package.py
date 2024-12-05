# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyasn1(PythonPackage):
    """Pure-Python implementation of ASN.1 types and DER/BER/CER codecs
    (X.208)."""

    homepage = "https://github.com/etingof/pyasn1"
    pypi = "pyasn1/pyasn1-0.4.6.tar.gz"

    license("BSD-2-Clause")

    version("0.4.8", sha256="aef77c9fb94a3ac588e87841208bdec464471d9871bd5050a287cc9a475cd0ba")
    version("0.4.6", sha256="b773d5c9196ffbc3a1e13bdf909d446cad80a039aa3340bcad72f395b76ebc86")
    version("0.4.5", sha256="da2420fe13a9452d8ae97a0e478adde1dee153b11ba832a95b223a2ba01c10f7")
    version("0.4.3", sha256="fb81622d8f3509f0026b0683fe90fea27be7284d3826a5f2edf97f69151ab0fc")
    version("0.2.3", sha256="738c4ebd88a718e700ee35c8d129acce2286542daa80a82823a7073644f706ad")

    depends_on("python@2.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
