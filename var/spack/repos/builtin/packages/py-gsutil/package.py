# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGsutil(PythonPackage):
    """A command line tool for interacting with cloud storage services."""

    homepage = "https://cloud.google.com/storage/docs/gsutil"
    pypi = "gsutil/gsutil-4.59.tar.gz"
    git = "https://github.com/GoogleCloudPlatform/gsutil.git"

    maintainers("dorton21")

    license("Apache-2.0")

    version("5.24", sha256="1f841645cda40fcc817e9ca84d285cdf541cc015fd38a5862017b085756729a0")
    version("5.2", sha256="08857eedbd89c7c6d10176b14f94fb1168d5ef88f5b5b15b3e8a37e29302b79b")
    version("4.59", sha256="349e0e0b48c281659acec205917530ae57e2eb23db7220375f5add44688d3ddf")

    depends_on("python@2.7:2.8,3.5:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-argcomplete@1.9.4:", type=("build", "run"))
    depends_on("py-crcmod@1.7:", type=("build", "run"))
    depends_on("py-fasteners@0.14.1:", type=("build", "run"))
    depends_on("py-gcs-oauth2-boto-plugin@3:", when="@5:", type=("build", "run"))
    depends_on("py-gcs-oauth2-boto-plugin@2.7:", type=("build", "run"))
    depends_on("py-google-apitools@0.5.32:", type=("build", "run"))
    depends_on("py-httplib2@0.20.4", when="@5.17:", type=("build", "run"))
    depends_on("py-httplib2@0.18:", type=("build", "run"))
    depends_on("py-google-reauth@0.1.0:", type=("build", "run"))
    depends_on("py-monotonic@1.4:", type=("build", "run"))
    depends_on("py-pyopenssl@0.13:", type=("build", "run"))
    depends_on("py-retry-decorator@1.0.0:", type=("build", "run"))
    depends_on("py-six@1.12.0:", type=("build", "run"))
    depends_on("py-google-auth+aiohttp@2.5:", when="@5.7:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-mock@2:3.0.5", when="@:4.67", type=("build", "run"))

    skip_modules = ["gslib.vendored"]
