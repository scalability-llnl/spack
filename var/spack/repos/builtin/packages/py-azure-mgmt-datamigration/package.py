# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureMgmtDatamigration(PythonPackage):
    """Microsoft Azure Data Migration Client Library for Python."""

    homepage = "https://github.com/Azure/azure-sdk-for-python"
    pypi = "azure-mgmt-datamigration/azure-mgmt-datamigration-4.0.0.zip"

    version("4.0.0", sha256="1efda568d67af911156591eb308432b5f9a56075b57ac0a5dd9f7aee17d79217")
    version("0.1.0", sha256="e754928992743f54d999800a5e0679ee3e91d804d23a25f12c2e6f2f86cd05df")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.5.0:", when="@4:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.32:1", when="@4:", type=("build", "run"))
    depends_on("py-msrestazure@0.4.27:1", type=("build", "run"))
    depends_on("py-azure-common@1.1:1", type=("build", "run"))
