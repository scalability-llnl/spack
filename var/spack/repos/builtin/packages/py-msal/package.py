# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMsal(PythonPackage):
    """The Microsoft Authentication Library (MSAL) for Python library enables
    your app to access the Microsoft Cloud by supporting authentication of
    users with Microsoft Azure Active Directory accounts (AAD) and Microsoft
    Accounts (MSA) using industry standard OAuth2 and OpenID Connect."""

    homepage = "https://github.com/AzureAD/microsoft-authentication-library-for-python"
    pypi = "msal/msal-1.26.0.tar.gz"

    license("MIT")

    version("1.26.0", sha256="224756079fe338be838737682b49f8ebc20a87c1c5eeaf590daae4532b83de15")
    version("1.20.0", sha256="78344cd4c91d6134a593b5e3e45541e666e37b747ff8a6316c3668dd1e6ab6b2")
    version("1.3.0", sha256="5442a3a9d006506e653d3c4daff40538bdf067bf07b6b73b32d1b231d5e77a92")
    version("1.0.0", sha256="ecbe3f5ac77facad16abf08eb9d8562af3bc7184be5d4d90c9ef4db5bde26340")

    # https://github.com/AzureAD/microsoft-authentication-library-for-python/blob/1.26.0/setup.cfg

    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2", type=("build", "run"))
    depends_on("py-pyjwt@1:2+crypto", type=("build", "run"), when="@1.9:")
    depends_on("py-pyjwt@1+crypto", type=("build", "run"), when="@:1.8")
    depends_on("py-cryptography@0.6:43", type=("build", "run"), when="@1.24:")
    depends_on("py-cryptography@0.6:42", type=("build", "run"), when="@1.22:1.23")
    depends_on("py-cryptography@0.6:40", type=("build", "run"), when="@1.19:1.21")
    depends_on("py-cryptography@0.6:39", type=("build", "run"), when="@1.18")
    depends_on("py-cryptography@0.6:38", type=("build", "run"), when="@1.17")
    depends_on("py-cryptography@0.6:37", type=("build", "run"), when="@1.15:1.16")
    depends_on("py-cryptography@0.6:3", type=("build", "run"), when="@1.6:1.14")
