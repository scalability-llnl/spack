# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *

_versions = {
    # cuTensor 1.5.0
    "1.5.0.3": {
        "Linux-x86_64": "4fdebe94f0ba3933a422cff3dd05a0ef7a18552ca274dd12564056993f55471d",
        "Linux-ppc64le": "ad736acc94e88673b04a3156d7d3a408937cac32d083acdfbd8435582cbe15db",
        "Linux-aarch64": "5b9ac479b1dadaf40464ff3076e45f2ec92581c07df1258a155b5bcd142f6090",
    },
    "2.0.1.2": {
        "Linux-x86_64": "ededa12ca622baad706ea0a500a358ea51146535466afabd96e558265dc586a2",
        "Linux-ppc64le": "7176083a4dad44cb0176771be6efb3775748ad30a39292bf7b4584510f1dd811",
        "Linux-aarch64": "4214a0f7b44747c738f2b643be06b2b24826bd1bae6af27f29f3c6dec131bdeb",
    },
}


class Cutensor(Package):
    """NVIDIA cuTENSOR Library is a GPU-accelerated tensor linear algebra
    library providing tensor contraction, reduction and elementwise
    operations."""

    homepage = "https://developer.nvidia.com/cutensor"

    maintainers("bvanessen")
    url = "cutensor"

    skip_version_audit = ["platform=darwin", "platform=windows"]

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        cutensor_ver = ver

        cuda_ver = "10.0"
        if platform.machine() == "aarch64":
            cuda_ver = "11.0"

        if pkg:
            version(cutensor_ver, sha256=pkg)
            # Add constraints matching CUDA version to cuTensor version
            cuda_req = "cuda@{0}:".format(cuda_ver)
            cutensor_ver_req = "@{0}".format(cutensor_ver)
            depends_on(cuda_req, when=cutensor_ver_req)

    def url_for_version(self, version):
        # Get the system and machine arch for building the file path
        sys = "{0}-{1}".format(platform.system(), platform.machine())
        # Munge it to match Nvidia's naming scheme
        sys_key = sys.lower()
        sys_key = sys_key.replace("aarch64", "sbsa")

        url = "https://developer.download.nvidia.com/compute/cutensor/redist/libcutensor/{0}/libcutensor-{0}-{1}-archive.tar.xz"
        return url.format(sys_key, version)

    def install(self, spec, prefix):
        install_tree(".", prefix)
