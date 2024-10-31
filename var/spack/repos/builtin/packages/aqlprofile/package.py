# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *

_versions = {
    "6.2.1": {
        "apt": (
            "a196698d39c567aef39734b4a47e0daa1596c86945868b4b0cffc6fcb0904dea",
            "https://repo.radeon.com/rocm/apt/6.2.1/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.60201.60201-112~20.04_amd64.deb",
        ),
        "yum": (
            "771782e92156a25a775cb324a5ae4288d419659b963132688e9ed79eed22e421",
            "https://repo.radeon.com/rocm/yum/6.2.1/main/hsa-amd-aqlprofile-1.0.0.60201.60201-112.el7.x86_64.rpm",
        ),
        "zyp": (
            "bb70b54754638c4eb707ae82f4dc02fe9e8fc2e56618e478172169b839851d4d",
            "https://repo.radeon.com/rocm/zyp/6.2.1/main/hsa-amd-aqlprofile-1.0.0.60201.60201-sles155.112.x86_64.rpm",
        ),
    },
    "6.2.0": {
        "apt": (
            "75f4417477abb80f6a453f836d1ac44c8a3d24447b21cfa4b29787a73725ef4e",
            "https://repo.radeon.com/rocm/apt/6.2/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.60200.60200-66~20.04_amd64.deb",
        ),
        "yum": (
            "d8ec6ceffe366c041d4dda11c418da53ca3b2234e8a57d4c4af9fdec936349ed",
            "https://repo.radeon.com/rocm/yum/6.2/main/hsa-amd-aqlprofile-1.0.0.60200.60200-66.el7.x86_64.rpm",
        ),
        "zyp": (
            "e7b34e800e4da6542261379e00b4f3a0e3ebc15e80925bf056ce495aff0b25e9",
            "https://repo.radeon.com/rocm/zyp/6.2/main/hsa-amd-aqlprofile-1.0.0.60200.60200-sles155.66.x86_64.rpm",
        ),
    },
    "6.1.2": {
        "apt": (
            "93faa8a0d702bc1623d2346e07a9a1c9134d99c0d3f9de62903e7394e0eedf47",
            "https://repo.radeon.com/rocm/apt/6.1.2/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.60102.60102-119~20.04_amd64.deb",
        ),
        "yum": (
            "b8c6a8c8fad6b07c87f99a95126b982aeb39a3e4943d05df090d2221f4aef779",
            "https://repo.radeon.com/rocm/yum/6.1.2/main/hsa-amd-aqlprofile-1.0.0.60102.60102-119.el7.x86_64.rpm",
        ),
        "zyp": (
            "132dde13aa550376ac39d57a51b42b803574cd0c57d2bd1346f36bf8d7efa4c4",
            "https://repo.radeon.com/rocm/zyp/6.1.2/main/hsa-amd-aqlprofile-1.0.0.60102.60102-sles154.119.x86_64.rpm",
        ),
    },
    "6.1.1": {
        "apt": (
            "faa5dae914fc63f0c8d0c2be28b7ec502db487004bdff0fe88dd15432efc5401",
            "https://repo.radeon.com/rocm/apt/6.1.1/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.60101.60101-90~20.04_amd64.deb",
        ),
        "yum": (
            "cc247e15ceff625c94d6c7104ffea3990a4acbcd2f9114914ab7ab829fae4aeb",
            "https://repo.radeon.com/rocm/yum/6.1.1/main/hsa-amd-aqlprofile-1.0.0.60101.60101-90.el7.x86_64.rpm",
        ),
        "zyp": (
            "9af82841be1765d6334b06a463583570653b6a36d0de29cfc00c5c4b6560b956",
            "https://repo.radeon.com/rocm/zyp/6.1.1/main/hsa-amd-aqlprofile-1.0.0.60101.60101-sles154.90.x86_64.rpm",
        ),
    },
    "6.1.0": {
        "apt": (
            "0ef862503245f12721384443f8347528f3d5c2c7762289c770521f3235ba36c9",
            "https://repo.radeon.com/rocm/apt/6.1/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.60100.60100-82~20.04_amd64.deb",
        ),
        "yum": (
            "bb08ec49987ef821278e24b9669ccea613a1475af4aedfcc3ac77146e6fbf229",
            "https://repo.radeon.com/rocm/yum/6.1/main/hsa-amd-aqlprofile-1.0.0.60100.60100-82.el7.x86_64.rpm",
        ),
        "zyp": (
            "6a20c8933a878dc3476fa5a45936d3d230d5c2c417e914a6460c2f576a3d6e35",
            "https://repo.radeon.com/rocm/zyp/6.1/main/hsa-amd-aqlprofile-1.0.0.60100.60100-sles154.82.x86_64.rpm",
        ),
    },
    "6.0.2": {
        "apt": (
            "57efc4e8380d941fc9e3ba8353bc724913cd5b5be2c53fed016e92da63e31b2f",
            "https://repo.radeon.com/rocm/apt/6.0.2/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.60002.60002-115~20.04_amd64.deb",
        ),
        "yum": (
            "eb9099e86c3574124dfeec257217781b716f72c51cc5c11ed857d16cb0924467",
            "https://repo.radeon.com/rocm/yum/6.0.2/main/hsa-amd-aqlprofile-1.0.0.60002.60002-115.el7.x86_64.rpm",
        ),
        "zyp": (
            "b752eb18eed98226bf0cffa492363d452b318432fd5ae01ad86172c4ce132bef",
            "https://repo.radeon.com/rocm/zyp/6.0.2/main/hsa-amd-aqlprofile-1.0.0.60002.60002-sles154.115.x86_64.rpm",
        ),
    },
    "6.0.0": {
        "apt": (
            "e120268933eab5eff25d1b7d0646b0785a13a9fb2dce2bdaca7ac2a19482339c",
            "https://repo.radeon.com/rocm/apt/6.0/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.60000.60000-91~20.04_amd64.deb",
        ),
        "yum": (
            "431be1e9996a465e1305a312e238e9bc7de3991fa2488968a36195108ed7f7b5",
            "https://repo.radeon.com/rocm/yum/6.0/main/hsa-amd-aqlprofile-1.0.0.60000.60000-91.el7.x86_64.rpm",
        ),
        "zyp": (
            "e64f3c0642b209753e2ede374eee80c36827db9de348c754a4385139f7203487",
            "https://repo.radeon.com/rocm/zyp/6.0/main/hsa-amd-aqlprofile-1.0.0.60000.60000-sles154.91.x86_64.rpm",
        ),
    },
    "5.7.1": {
        "apt": (
            "9f00713062005624231dac5fd3e92481b8d1547b3301c3b8a07298d4548037b8",
            "https://repo.radeon.com/rocm/apt/5.7.1/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.50701.50701-98~20.04_amd64.deb",
        ),
        "yum": (
            "ea69d9deb604fdc0415070a9e3d8dbe90feecfc71533b92dd7507e2b8d2770de",
            "https://repo.radeon.com/rocm/yum/5.7.1/main/hsa-amd-aqlprofile-1.0.0.50701.50701-98.el7.x86_64.rpm",
        ),
        "zyp": (
            "d83ca93e280764afc20e2eca01b8cc1c047e2a4db0131b4df58ec19f0ddc2a07",
            "https://repo.radeon.com/rocm/zyp/5.7.1/main/hsa-amd-aqlprofile-1.0.0.50701.50701-sles154.98.x86_64.rpm",
        ),
    },
    "5.7.0": {
        "apt": (
            "131e2d699eb24ff19cba54a9721b83c362196c91a8380b5e4b4ba3583311df21",
            "https://repo.radeon.com/rocm/apt/5.7/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.50700.50700-63~20.04_amd64.deb",
        ),
        "yum": (
            "4f6eef63bb586c290b22234b3d849b382bcb4ddc0f28ed93b3232ca7f6914759",
            "https://repo.radeon.com/rocm/yum/5.7/main/hsa-amd-aqlprofile-1.0.0.50700.50700-63.el7.x86_64.rpm",
        ),
        "zyp": (
            "61b7ba9022cdf2903dd476811d39f294cdb0fd4bd385785bcba9abe575e9b63c",
            "https://repo.radeon.com/rocm/zyp/5.7/main/hsa-amd-aqlprofile-1.0.0.50700.50700-sles154.63.x86_64.rpm",
        ),
    },
    "5.6.1": {
        "apt": (
            "ddb231dc4c8ca45e586ba68cae86273c3bc109f5ec172855815fce1ea6aff172",
            "https://repo.radeon.com/rocm/apt/5.6.1/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.50601-93~20.04_amd64.deb",
        ),
        "yum": (
            "3c67b2e3cfbe71441d4c504dee2c55c9010a15ad7c973f1f858a052fb60524a6",
            "https://repo.radeon.com/rocm/yum/5.6.1/main/hsa-amd-aqlprofile-1.0.0.50601-93.el7.x86_64.rpm",
        ),
        "zyp": (
            "956382a085356211a35cb24210764c4f5575ce4d3d842439e39cc94287004176",
            "https://repo.radeon.com/rocm/zyp/5.6.1/main/hsa-amd-aqlprofile-1.0.0.50601-sles154.93.x86_64.rpm",
        ),
    },
    "5.6.0": {
        "apt": (
            "67273e8513c0efdef6d52fb211a0cf4b7e117b1c5e737f8763946699324a9d7d",
            "https://repo.radeon.com/rocm/apt/5.6/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.50600-67~20.04_amd64.deb",
        ),
        "yum": (
            "0aefd5f0eca5c1bcb55f5c80e946e252685533cbb3c936417abd44fe94c1f28e",
            "https://repo.radeon.com/rocm/yum/5.6/main/hsa-amd-aqlprofile-1.0.0.50600-67.el7.x86_64.rpm",
        ),
        "zyp": (
            "b752eb18eed98226bf0cffa492363d452b318432fd5ae01ad86172c4ce132bef",
            "https://repo.radeon.com/rocm/zyp/5.6/main/hsa-amd-aqlprofile-1.0.0.50600-sles154.67.x86_64.rpm",
        ),
    },
    "5.5.1": {
        "apt": (
            "67b957abe5ea872abd3ec6b98eb83ef66fe07668001392e695dd77ab1b6d8890",
            "https://repo.radeon.com/rocm/apt/5.5.1/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.50501-74~20.04_amd64.deb",
        ),
        "yum": (
            "2e6ae5a417d3a14a6b522b2daccbccea0a192ffe689b5e1817300ec2b65b60c2",
            "https://repo.radeon.com/rocm/yum/5.5.1/main/hsa-amd-aqlprofile-1.0.0.50501-74.el7.x86_64.rpm",
        ),
        "zyp": (
            "3ad17b1628c308396d39f61c12f7403800468f54eb3f7b3ed4b47e076ea1b821",
            "https://repo.radeon.com/rocm/zyp/5.5.1/main/hsa-amd-aqlprofile-1.0.0.50501-sles153.74.x86_64.rpm",
        ),
    },
    "5.5.0": {
        "apt": (
            "fbe08a39a36499959198fa7678338cf2d7888dc2aafb4694072d1f37b24e599f",
            "https://repo.radeon.com/rocm/apt/5.5/pool/main/h/hsa-amd-aqlprofile/hsa-amd-aqlprofile_1.0.0.50500-63~20.04_amd64.deb",
        ),
        "yum": (
            "fde2d38174d25af9d780ef2a1e91eb75b0de5943711f20930367b9f28f77a8bd",
            "https://repo.radeon.com/rocm/yum/5.5/main/hsa-amd-aqlprofile-1.0.0.50500-63.el7.x86_64.rpm",
        ),
        "zyp": (
            "eec9dc39ddbb0fc1f18e0b62a238252b3e0968152792c5b4948b3d001b07a53f",
            "https://repo.radeon.com/rocm/zyp/5.5/main/hsa-amd-aqlprofile-1.0.0.50500-sles153.63.x86_64.rpm",
        ),
    },
}


class Aqlprofile(Package):
    """
    HSA extension AMD AQL profile library.
    Provides AQL packets helper methods for perfcounters (PMC) and SQ threadtraces (SQTT).
    """

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    spack_os = spack.platforms.host().default_os
    if "rhel" in spack_os or "centos" in spack_os:
        pkg_type = "yum"
    elif "sles" in spack_os:
        pkg_type = "zyp"
    else:
        pkg_type = "apt"

    for ver, packages in _versions.items():
        pkg = packages.get(pkg_type)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1], expand=False)

    depends_on("cpio")

    def install(self, spec, prefix):
        # find deb or rpm pkg and extract files
        for file in os.listdir("."):
            if file.endswith(".rpm"):
                os.system(f"rpm2cpio {file} | cpio -idmv")
                break
            if file.endswith(".deb"):
                os.system(f"ar vx {file}")
                os.system("tar xvf data.tar.gz")
                break

        install_tree(f"opt/rocm-{spec.version}/share/", prefix.share)
        install_tree(f"opt/rocm-{spec.version}/lib/", prefix.lib)
