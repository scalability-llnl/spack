# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kubernetes(Package):
    """Kubernetes is an open source system for managing containerized
    applications across multiple hosts. It provides basic mechanisms
    for deployment, maintenance, and scaling of applications."""

    homepage = "https://kubernetes.io"
    url = "https://github.com/kubernetes/kubernetes/archive/refs/tags/v1.27.0.tar.gz"

    maintainers("alecbcs")

    license("Apache-2.0")

    version("1.27.2", sha256="c6fcfddd38f877ce49c49318973496f9a16672e83a29874a921242950cd1c5d2")
    version("1.27.1", sha256="3a3f7c6b8cf1d9f03aa67ba2f04669772b1205b89826859f1636062d5f8bec3f")
    version("1.27.0", sha256="536025dba2714ee5e940bb0a6b1df9ca97c244fa5b00236e012776a69121c323")

    # Deprecated versions
    # https://nvd.nist.gov/vuln/detail/CVE-2022-3294
    version(
        "1.18.1",
        sha256="33ca738f1f4e6ad453b80f231f71e62470b822f21d44dc5b8121b2964ae8e6f8",
        deprecated=True,
    )
    version(
        "1.18.0",
        sha256="6bd252b8b5401ad6f1fb34116cd5df59153beced3881b98464862a81c083f7ab",
        deprecated=True,
    )
    version(
        "1.17.4",
        sha256="b61a6eb3bd5251884f34853cc51aa31c6680e7e476268fe06eb33f3d95294f62",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("bash", type="build")
    depends_on("go", type="build")

    phases = ["build", "install"]

    def build(self, spec, prefix):
        components = [
            "cmd/kubeadm",
            "cmd/kubelet",
            "cmd/kube-apiserver",
            "cmd/kube-controller-manager",
            "cmd/kube-proxy",
            "cmd/kube-scheduler",
        ]

        make(f"WHAT={' '.join(components)}")

    def install(self, spec, prefix):
        install_tree("_output/bin", prefix.bin)
