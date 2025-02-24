# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Geode(Package):
    """
    Apache Geode is a data management platform that provides real-time,
    consistent access to data-intensive applications throughout widely
    distributed cloud architectures.
    """

    homepage = "https://geode.apache.org/"
    url = "https://archive.apache.org/dist/geode/1.9.2/apache-geode-1.9.2.tgz"
    list_url = "https://archive.apache.org/dist/geode/"
    list_depth = 1

    license("Apache-2.0")

    version("1.15.1", sha256="2668970982d373ef42cff5076e7073b03e82c8e2fcd7757d5799b2506e265d57")
    version("1.14.3", sha256="5efb1c71db34ba3b7ce1004579f8b9b7a43eae30f42c37837d5abd68c6d778bd")
    version("1.13.8", sha256="b5fc105ce0a16aaf7ba341668e022d458b18d6d2c44705a8c79c42077c6d8229")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2022-37021
        version("1.9.2", sha256="4b8118114ef43166f6bf73af56b93aadbf9108fcab06d1fbbb8e27f7d559d7e0")
        version("1.9.0", sha256="8794808ebc89bc855f0b989b32e91e890d446cfd058e123f6ccb9e12597c1c4f")
        version("1.8.0", sha256="58edc41edac4eabd899322b73a24727eac41f6253274c2ce7d0a82227121ae3e")
        version("1.7.0", sha256="91eec04420f46e949d32104479c4a4b5b34a4e5570dca7b98ca067a30d5a783d")
        version("1.6.0", sha256="79e8d81d058b1c4edd5fb414ff30ac530f7913b978f5abc899c353fcb06e5ef3")

    depends_on("java", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)
