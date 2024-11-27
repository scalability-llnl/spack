# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudCore(PythonPackage):
    """Google Cloud API client core library."""

    homepage = "https://github.com/GoogleCloudPlatform/google-cloud-python"
    pypi = "google-cloud-core/google-cloud-core-1.0.3.tar.gz"

    license("Apache-2.0")

    version("2.3.2", sha256="b9529ee7047fd8d4bf4a2182de619154240df17fbe60ead399078c1ae152af9a")
    version("1.0.3", sha256="10750207c1a9ad6f6e082d91dbff3920443bdaf1c344a782730489a9efa802f1")

    depends_on("py-setuptools", type="build")
    depends_on("py-google-api-core@1.31.6:1,2.3.1:2", when="@2:", type=("build", "run"))
    depends_on("py-google-api-core@1.14:1", when="@:1", type=("build", "run"))
    depends_on("py-google-auth@1.25:2", when="@2:", type=("build", "run"))
