# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kubectl(GoPackage):
    """
    Kubectl is a command-line interface for Kubernetes clusters.
    """

    homepage = "https://kubernetes.io"
    url = "https://github.com/kubernetes/kubernetes/archive/refs/tags/v1.27.0.tar.gz"

    maintainers("alecbcs")

    license("Apache-2.0")

    version("1.31.1", sha256="83094915698a9c24f93d1ffda3f17804a4024d3b65eabf681e77a62b35137208")
    version("1.31.0", sha256="6679eb90815cc4c3bef6c1b93f7a8451bf3f40d003f45ab57fdc9f8c4e8d4b4f")
    version("1.27.1", sha256="3a3f7c6b8cf1d9f03aa67ba2f04669772b1205b89826859f1636062d5f8bec3f")
    version("1.27.0", sha256="536025dba2714ee5e940bb0a6b1df9ca97c244fa5b00236e012776a69121c323")

    depends_on("bash", type="build")
    depends_on("go@1.22:", type="build", when="@1.30:")

    build_directory = "cmd/kubectl"
