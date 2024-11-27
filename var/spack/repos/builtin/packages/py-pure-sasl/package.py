# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPureSasl(PythonPackage):
    """This package provides a reasonably high-level SASL client
    written in pure Python. New mechanisms may be integrated easily,
    but by default, support for PLAIN, ANONYMOUS, EXTERNAL, CRAM-MD5,
    DIGEST-MD5, and GSSAPI are provided."""

    homepage = "https://github.com/thobbs/pure-sasl"
    pypi = "pure-sasl/pure-sasl-0.6.2.tar.gz"

    license("MIT")

    version("0.6.2", sha256="53c1355f5da95e2b85b2cc9a6af435518edc20c81193faa0eea65fdc835138f4")

    variant("gssapi", default=True, description="build with kerberos/gssapi support")

    depends_on("py-setuptools", type="build")
    depends_on("py-kerberos@1.3.0:", type=("build", "run"), when="+gssapi")
