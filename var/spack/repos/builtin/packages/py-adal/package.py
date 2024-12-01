# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAdal(PythonPackage):
    """The ADAL for Python library makes it easy for python application to
    authenticate to Azure Active Directory (AAD) in order to access AAD
    protected web resources.

    DEPRECATED: replaced by MSAL Python."""

    homepage = "https://github.com/AzureAD/azure-activedirectory-library-for-python"
    pypi = "adal/adal-1.2.4.tar.gz"

    license("MIT")

    version("1.2.4", sha256="7a15d22b1ee7ce1be92441199958748982feba6b7dec35fbf60f9b607bad1bc0")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyjwt@1.0.0:", type=("build", "run"))
    depends_on("py-requests@2.0.0:", type=("build", "run"))
    depends_on("py-python-dateutil@2.1.0:", type=("build", "run"))
    depends_on("py-cryptography@1.1.0:", type=("build", "run"))
