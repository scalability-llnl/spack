# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGoogleCloudAuditLog(PythonPackage):
    """Google Cloud Audit Protos."""

    homepage = "https://github.com/googleapis/python-audit-log"
    pypi = "google_cloud_audit_log/google-cloud-audit-log-0.2.5.tar.gz"

    license("Apache-2.0")

    version("0.2.5", sha256="86e2faba3383adc8fd04a5bd7fd4f960b3e4aedaa7ed950f2f891ce16902eb6b")

    # https://github.com/googleapis/python-audit-log/blob/v0.2.5/setup.py

    depends_on("py-protobuf@3.19.5:4", type=("build", "run"))
    conflicts("py-protobuf@3.20.0,3.20.1,4.21.1:4.21.5")

    depends_on("py-googleapis-common-protos@1.56.2:1", type=("build", "run"))

    depends_on("py-setuptools", type="build")
