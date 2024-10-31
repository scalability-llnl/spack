# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class E2fsprogs(AutotoolsPackage):
    """It provides the filesystem utilities for use with the ext2 filesystem.
    It also supports the ext3 and ext4 filesystems."""

    homepage = "https://github.com/tytso/e2fsprogs"
    url = "https://github.com/tytso/e2fsprogs/archive/v1.45.6.tar.gz"

    license("GPL-2.0-or-later AND LGPL-2.0-or-later AND BSD-3-Clause AND MIT")

    version("1.47.1", sha256="db95ff1cb6ef741c9aa8875d9f3f52a34168360febba765b6377b80bada09a8c")
    version("1.47.0", sha256="74c8ea97c73294edc6c11dc5e7fbb4324f86c28efd66ad0ba50be4eec8a48be2")
    version("1.45.6", sha256="d785164a2977cd88758cb0cac5c29add3fe491562a60040cfb193abcd0f9609b")
    version("1.45.5", sha256="0fd76e55c1196c1d97a2c01f2e84f463b8e99484541b43ff4197f5a695159fd3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("fuse2fs", default=False, description="Build fuse2fs")

    depends_on("texinfo", type="build")
    depends_on("fuse", when="+fuse2fs")
    depends_on("pkgconfig", when="+fuse2fs")

    # fuse3 support is in the yet unreleased 1.47.1
    patch(
        "https://github.com/tytso/e2fsprogs/commit/5598a96.patch?full_index=1",
        sha256="72b28eb4599dbae45a01a1518ab6b8b6fc23db4f67381b49f63d3a3d45822340",
        when="@:1.47.0 +fuse2fs",
    )
    patch(
        "https://github.com/tytso/e2fsprogs/commit/1ac0061.patch?full_index=1",
        sha256="c5fbcd4e6d7f29d083d923b33998d916e2059b8f108c8cc20e8b5c928186eef2",
        when="@:1.47.0 +fuse2fs",
    )
    patch(
        "https://github.com/tytso/e2fsprogs/commit/448a3f8.patch?full_index=1",
        sha256="fb45c3af229b49fab19c70c00c33b9f3579a9455025aedb8049ff411b1cf3a96",
        when="@:1.47.0 +fuse2fs",
    )

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)

    def configure_args(self):
        # avoid installing things in /etc
        args = ["--without-udev-rules-dir", "--without-crond-dir", "--without-systemd-unit-dir"]
        args.extend(self.enable_or_disable("fuse2fs"))
        return args
