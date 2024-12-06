# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sshfs(MesonPackage):
    """SSHFS allows you to mount a remote filesystem using SFTP."""

    homepage = "https://github.com/libfuse/sshfs"
    url = "https://github.com/libfuse/sshfs/releases/download/sshfs-3.7.1/sshfs-3.7.1.tar.xz"
    git = "https://github.com/libfuse/sshfs.git"

    maintainers("haampie")

    license("GPL-2.0-or-later")

    version("3.7.1", sha256="fe5d3436d61b46974889e0c4515899c21a9d67851e3793c209989f72353d7750")

    depends_on("c", type="build")  # generated

    depends_on("glib")
    depends_on("fuse@3.1.0:")

    # used for libfuse; when libfuse is external, make sure that pkgconfig is
    # external too, since spack's pkgconfig might not be able to locate libfuse.
    depends_on("pkgconfig", type="build")
