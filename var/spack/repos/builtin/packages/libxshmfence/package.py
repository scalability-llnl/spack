# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxshmfence(AutotoolsPackage, XorgPackage):
    """libxshmfence - Shared memory 'SyncFence' synchronization primitive.

    This library offers a CPU-based synchronization primitive compatible
    with the X SyncFence objects that can be shared between processes
    using file descriptor passing."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libxshmfence"
    xorg_mirror_path = "lib/libxshmfence-1.3.2.tar.xz"

    license("MIT")

    version("1.3.2", sha256="870df257bc40b126d91b5a8f1da6ca8a524555268c50b59c0acd1a27f361606f")
    version("1.3.1", sha256="1129f95147f7bfe6052988a087f1b7cb7122283d2c47a7dbf7135ce0df69b4f8")
    version("1.3", sha256="b884300d26a14961a076fbebc762a39831cb75f92bed5ccf9836345b459220c7")
    version("1.2", sha256="d21b2d1fd78c1efbe1f2c16dae1cb23f8fd231dcf891465b8debe636a9054b0c")

    depends_on("c", type="build")

    depends_on("xproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    def url_for_version(self, version):
        url = super().url_for_version(version)
        if version <= Version("1.3"):
            return url.replace("xz", "bz2")

        return url
