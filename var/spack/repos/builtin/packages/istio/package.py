# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *

_versions = {
    "1.23.2": {
        "Linux-aarch64": "c2f1ca6cec376cb7eaff5807124b6d7ebcef9c84ff9f3fb7ad3ed1e942cfefab",
        "Linux-x86_64": "c4bbcb95e3015f63f9aa76ac07a544d4c2f46d6d3b20971559d9216eb07b676b",
    },
    # Deprecated versions
    # https://nvd.nist.gov/vuln/detail/CVE-2022-31045
    "1.6.7": {
        "Linux-aarch64": "22b0f94efafe9f221c00f4599d9a04e473554515e5fdf8d119fd27e27e36c89f",
        "Linux-x86_64": "3243d2c4bb7a116aa04a6bc21d289fb73cdc704988af1749d2a1f0fb5426be36",
        "deprecated": True,
    },
    "1.6.6": {
        "Linux-aarch64": "b122a0abde24b7680194f504815db5e054483b3657292a6150104e9d129787a5",
        "Linux-x86_64": "3f092ffb3a1c13eccfadb42fe14166049535945f349241f90a91d97e57036da7",
        "deprecated": True,
    },
    "1.6.5": {
        "Linux-aarch64": "c32ed12be0e2bb33bae510fd6b680656990bf2c2ba6059277b6f463a195355a0",
        "Linux-x86_64": "68e58e8aec544c2b72377f7c334f90f6215bc819f3ed71ac952692cc5c9b73ac",
        "deprecated": True,
    },
    "1.6.4": {
        "Linux-aarch64": "700416965f48f91ce5a654513b5aa4ed56dd5875e98af203389b3d20d55016b2",
        "Linux-x86_64": "97ce26edad734b4a324b1a3914cead3a38ac70a029dbe09777a483ec192d04df",
        "deprecated": True,
    },
}


class Istio(Package):
    """An open platform to connect, manage, and secure microservices."""

    homepage = "https://istio.io/"
    url = "https://github.com/istio/istio/releases/download/1.6.5/istio-1.6.5-linux-arm64.tar.gz"
    list_url = "https://github.com/istio/istio/releases/download"
    list_depth = 1

    license("Apache-2.0")

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        sha_val = packages.get(key)
        if sha_val:
            version(ver, sha256=sha_val, deprecated=packages.get("deprecated", False))

    def url_for_version(self, version):
        url = "https://github.com/istio/istio/releases/download/{0}/istio-{0}-linux-{1}.tar.gz"
        if platform.machine() == "aarch64":
            aarch = "arm64"
        elif platform.machine() == "x86_64":
            aarch = "amd64"
        else:
            aarch = "unknown"
        return url.format(version, aarch)

    def install(self, spec, prefix):
        install_tree(".", prefix)
