# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0)

from spack.package import *


class Minikube(MakefilePackage):
    """minikube is local Kubernetes,  making it easy to learn and develop for Kubernetes."""

    homepage = "https://minikube.sigs.k8s.io/"
    url = "https://github.com/kubernetes/minikube/archive/refs/tags/v1.34.0.tar.gz"

    maintainers("teaguesterling")

    license("Apache-2.0", checked_by="teaguesterling")

    version("1.34.0", sha256="d747bdf98a0ef1c1b43c577607b57a31977d92e1fa1406f8c5ecf6ca31cc51d4")

    depends_on("go@1.22.0:")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("out/minikube", prefix.bin.minikube)
