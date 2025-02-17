# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kubectl(GoPackage):
    """
    Kubectl is a command-line interface for Kubernetes clusters.
    """

    homepage = "https://kubernetes.io"
    url = "https://github.com/kubernetes/kubernetes/archive/refs/tags/v1.32.2.tar.gz"

    maintainers("alecbcs")

    license("Apache-2.0")

    version("1.32.2", sha256="d2a917570d7c9d7247e60b58bffa13c4a4dfcc63c195f2deedbf6224b9fb4993")
    version("1.31.6", sha256="4fbe4f949494d5f21e247b59313d85ecf4bd042dc1f3113430b023b1945248d0")
    version("1.30.10", sha256="556fa1f93d46184f839253f7507170a518cac74a7e632272aed466d105e8d159")

    with default_args(deprecated=True):
        version(
            "1.32.1", sha256="9724c849c524c2e69a0a0da4f1a3b0335d7d544eeaa9fc22cb5b87d7c0c52c9d"
        )
        version(
            "1.32.0", sha256="3793859c53f09ebc92e013ea858b8916cc19d7fe288ec95882dada4e5a075d08"
        )
        version(
            "1.31.5", sha256="7648c290f46bfc45cb8a24dc94e39cdea333bbe39223ab1cc253ebf9e2e0c3cb"
        )
        version(
            "1.31.4", sha256="ff3a2e9cae3b4734be4a6cdfeb933830c63219eaeda05cc4e59b7559fcde52b0"
        )
        version(
            "1.31.3", sha256="a58bf0797989acc9530a23164d529d5df5e4068e2fce9738cbe6f11f823ccf20"
        )
        version(
            "1.31.2", sha256="05007001f41176b388fcb01d6dc35e454db35a4e65b114db42b2b7340be8aed3"
        )
        version(
            "1.31.1", sha256="83094915698a9c24f93d1ffda3f17804a4024d3b65eabf681e77a62b35137208"
        )
        version(
            "1.31.0", sha256="6679eb90815cc4c3bef6c1b93f7a8451bf3f40d003f45ab57fdc9f8c4e8d4b4f"
        )
        version(
            "1.30.9", sha256="d703f03da3e1dadd3d4e8a1ef6dcaa572600c64d2193e802172cd9b9360c00e6"
        )
        version(
            "1.30.8", sha256="d33a93d74ae29d31a44384920039160c66eebacfb7ff83ceec9104577e3bd1e9"
        )
        version(
            "1.30.7", sha256="e11936d2a0e1ef2c10d3358ecca3bf7615a3664be8b337adb3e636342bff9750"
        )
        version(
            "1.30.6", sha256="8ef8826088ab531e9162ae7e0c3e4f197f807a69b5f1903324cf6f2df84083e9"
        )
        version(
            "1.30.5", sha256="e0c24a726a9a24180c9c51292d3a4ec9e1583537112661cf9504f92ed99e7aac"
        )
        version(
            "1.30.4", sha256="9f0fb73016b1ca9dee9fc8e5f072ec60822b1ec6457634b1a0085760d9bc2e97"
        )
        version(
            "1.30.3", sha256="2e57ccaa4d3a8fb9dd0527af61702d6f193ff2f4c3b2fb35362bbf5fed6ce674"
        )
        version(
            "1.30.2", sha256="a4ac165376708bce1634e0f1a2156c1cb1c4390fa574bacca3382b889f0d7b28"
        )
        version(
            "1.30.1", sha256="0b0bae91594fc8f8cc2ae3443f24b95660e6c5f5761bc2dc76cb7ef1c6047d9f"
        )
        version(
            "1.30.0", sha256="16385d1e4af6d3ede885b5c5d617ad06cc2a7a28e40a380fb04c521c9e7fb957"
        )
        version(
            "1.27.1", sha256="3a3f7c6b8cf1d9f03aa67ba2f04669772b1205b89826859f1636062d5f8bec3f"
        )
        version(
            "1.27.0", sha256="536025dba2714ee5e940bb0a6b1df9ca97c244fa5b00236e012776a69121c323"
        )

    depends_on("bash", type="build")
    depends_on("go@1.22:", type="build", when="@1.30:")
    depends_on("go@1.23:", type="build", when="@1.32:")

    build_directory = "cmd/kubectl"
