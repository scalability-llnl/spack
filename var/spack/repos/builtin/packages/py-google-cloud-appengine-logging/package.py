# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudAppengineLogging(PythonPackage):
    """Google Cloud Appengine Logging API client library."""

    homepage = "https://googleapis.github.io/google-cloud-python"
    pypi = "google_cloud_appengine_logging/google-cloud-appengine-logging-1.4.1.tar.gz"

    license("Apache-2.0")

    version("1.4.1", sha256="9905c7c30c3c2bbedd0b132e2b271fc8247333ebc931d2d23af1bbbd11b435fe")

    # https://github.com/googleapis/google-cloud-python/blob/google-cloud-appengine-logging-v1.4.1/packages/google-cloud-appengine-logging/setup.py

    depends_on("py-google-api-core+grpc@1.34.0:2", type=("build", "run"))
    conflicts("py-google-api-core@2.0:2.10")

    depends_on("py-google-auth@2.14.1:2", type=("build", "run"))
    depends_on("py-proto-plus@1.22.3:1", type=("build", "run"))

    depends_on("py-protobuf@3.19.5:4", type=("build", "run"))
    conflicts("py-protobuf@3.20.0,3.20.1,4.21.0:4.21.5")

    depends_on("py-setuptools", type="build")
