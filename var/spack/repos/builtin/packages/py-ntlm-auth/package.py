# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNtlmAuth(PythonPackage):
    """Creates NTLM authentication structures."""

    homepage = "https://github.com/jborean93/ntlm-auth"
    pypi = "ntlm-auth/ntlm-auth-1.5.0.tar.gz"

    license("MIT")

    version("1.5.0", sha256="c9667d361dc09f6b3750283d503c689070ff7d89f2f6ff0d38088d5436ff8543")

    depends_on("python@2.6:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
