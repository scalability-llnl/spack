# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Uvw(CMakePackage):
    """uvw is a header-only, event based, tiny and easy to use libuv
    wrapper in modern C++.
    """

    homepage = "https://github.com/skypjack/uvw"
    url = "https://github.com/skypjack/uvw/archive/v1.14.0_libuv-v1.26.tar.gz"

    license("MIT")

    version("1.14.0", sha256="ef13977c1f87d5659887f6a75d37b7088f2dafbdf0aaff00358240071c70382e")
    version("1.13.0", sha256="cc9944e5a2cdeb19bb74c61c3c02816c5a02b4339f3ad16e979bb7c8640e22c0")
    version("1.12.0", sha256="b7751294fa00e8a96cd7d70989beda7a6117f5d9f4751306b7b2bbbb4702aac8")

    depends_on("cxx", type="build")  # generated

    variant("docs", default=False, description="Builds and install the documentation")

    depends_on("libuv", type="link")
    depends_on("doxygen", type="build", when="+docs")

    matching_libuv_version = {"1.14.0": "1.26", "1.13.0": "1.25", "1.12.0": "1.24"}

    def url_for_version(self, version):
        url = "https://github.com/skypjack/uvw/archive/v{0}_libuv-v{1}.tar.gz"
        return url.format(version, self.matching_libuv_version[str(version)])

    @property
    def build_targets(self):
        return [] if "~docs" in self.spec else ["docs"]
