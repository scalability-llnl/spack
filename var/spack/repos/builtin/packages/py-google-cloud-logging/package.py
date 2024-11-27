# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudLogging(PythonPackage):
    """Stackdriver Logging API client library."""

    homepage = "https://github.com/googleapis/python-logging"
    pypi = "google-cloud-logging/google-cloud-logging-3.9.0.tar.gz"

    license("Apache-2.0")

    version("3.9.0", sha256="4decb1b0bed4a0e3c0e58a376646e6002d6be7cad039e3466822e8665072ea33")

    depends_on("py-google-api-core+grpc@1.33.2:2", type=("build", "run"))
    conflicts("py-google-api-core@2.0:2.7")

    depends_on("py-google-cloud-appengine-logging@0.1.0:1", type=("build", "run"))
    depends_on("py-google-cloud-audit-log@0.1.0:0", type=("build", "run"))
    depends_on("py-google-cloud-core@2", type=("build", "run"))
    depends_on("py-grpc-google-iam-v1@0.12.4:0", type=("build", "run"))
    depends_on("py-proto-plus@1.22.2:1", type=("build", "run"), when="^python@3.11:")
    depends_on("py-proto-plus@1.22:1", type=("build", "run"))

    depends_on("py-protobuf@3.19.5:4", type=("build", "run"))
    conflicts("py-protobuf@3.20.0:3.20.1,4.21.0:4.21.5")

    depends_on("py-setuptools", type="build")
