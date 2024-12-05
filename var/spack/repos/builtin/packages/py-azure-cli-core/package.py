# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureCliCore(PythonPackage):
    """Microsoft Azure Command-Line Tools Core Module."""

    homepage = "https://github.com/Azure/azure-cli"
    pypi = "azure-cli-core/azure-cli-core-2.9.1.tar.gz"

    license("MIT")

    version("2.9.1", sha256="8618a30f7ea2188506f29801220c06396d731c26e4de92c327e6b0e8cc790db5")

    depends_on("py-setuptools", type="build")
    depends_on("py-adal@1.2.3:1.2", type=("build", "run"))
    depends_on("py-argcomplete@1.8:1", type=("build", "run"))
    depends_on("py-azure-cli-telemetry", type=("build", "run"))
    depends_on("py-colorama@0.4.1:0.4", type=("build", "run"))
    depends_on("py-humanfriendly@4.7:8", type=("build", "run"))
    depends_on("py-jmespath", type=("build", "run"))
    depends_on("py-knack@0.7.1", type=("build", "run"))
    depends_on("py-msal@1.0.0:1.0", type=("build", "run"))
    depends_on("py-msal-extensions@0.1.3:0.1", type=("build", "run"))
    depends_on("py-msrest@0.4.4:", type=("build", "run"))
    depends_on("py-msrestazure@0.6.3:", type=("build", "run"))
    depends_on("py-paramiko@2.0.8:2", type=("build", "run"))
    depends_on("py-pyjwt", type=("build", "run"))
    depends_on("py-pyopenssl@17.1.0:", type=("build", "run"))
    depends_on("py-requests@2.22:2", type=("build", "run"))
    depends_on("py-six@1.12:1", type=("build", "run"))
    depends_on("py-pkginfo@1.5.0.1:", type=("build", "run"))
    depends_on("py-azure-mgmt-resource@10.0.0", type=("build", "run"))
    depends_on("py-azure-mgmt-core@1.0.0", type=("build", "run"))
