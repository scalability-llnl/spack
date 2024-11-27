# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsNtlm(PythonPackage):
    """This package allows for HTTP NTLM authentication using the requests library."""

    homepage = "https://github.com/requests/requests-ntlm"
    pypi = "requests_ntlm/requests_ntlm-1.1.0.tar.gz"

    license("ISC")

    version("1.1.0", sha256="9189c92e8c61ae91402a64b972c4802b2457ce6a799d658256ebf084d5c7eb71")

    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.0.0:", type=("build", "run"))
    depends_on("py-ntlm-auth@1.0.2:", type=("build", "run"))
    depends_on("py-cryptography@1.3:", type=("build", "run"))
