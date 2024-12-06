# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMsalExtensions(PythonPackage):
    """The Microsoft Authentication Extensions for Python offers secure
    mechanisms for client applications to perform cross-platform token cache
    serialization and persistence. It gives additional support to the
    Microsoft Authentication Library for Python (MSAL)."""

    homepage = "https://github.com/AzureAD/microsoft-authentication-library-for-python"
    pypi = "msal-extensions/msal-extensions-0.2.2.tar.gz"

    license("MIT")

    version("1.0.0", sha256="c676aba56b0cce3783de1b5c5ecfe828db998167875126ca4b47dc6436451354")
    version("0.2.2", sha256="31414753c484679bb3b6c6401623eb4c3ccab630af215f2f78c1d5c4f8e1d1a9")
    version("0.1.3", sha256="59e171a9a4baacdbf001c66915efeaef372fb424421f1a4397115a3ddd6205dc")

    # https://github.com/AzureAD/microsoft-authentication-extensions-for-python/blob/1.0.0/setup.py
    depends_on("py-setuptools", type="build")
    depends_on("py-msal@0.4.1:1", type=("build", "run"))
    depends_on("py-portalocker@1", when="@:0", type=("build", "run"))
    # This is the earliest version to work for Windows and non-Windows
    depends_on("py-portalocker@1.6:1", when="@1:", type=("build", "run"))
