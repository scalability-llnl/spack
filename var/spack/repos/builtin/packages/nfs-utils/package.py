# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NfsUtils(AutotoolsPackage):
    """The NFS Utilities package contains the userspace server and client tools
    necessary to use the kernel's NFS abilities. NFS is a protocol that allows
    sharing file systems over the network."""

    homepage = "http://linux-nfs.org/"
    url = "https://sourceforge.net/projects/nfs/files/nfs-utils/2.4.2/nfs-utils-2.4.2.tar.gz/download"

    license("GPL-2.0-only")

    version("2.4.2", sha256="bb08106cd7bd397c6cc34e2461bc7818a664450d2805da08b07e1ced88e5155f")
    version("2.4.1", sha256="c0dda96318af554881f4eb1590bfe91f1aba2fba59ed2ac3ba099f80fdf838e9")
    version("2.3.4", sha256="36e70b0a583751ead0034ebe5d8826caf2dcc7ee7c0beefe94d6ee5a3b0b2484")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("libtirpc")
    depends_on("libevent")
    depends_on("libdmx")
    depends_on("lvm2")
    depends_on("keyutils")
    depends_on("sqlite")
    depends_on("uuid")
    depends_on("util-linux")
    depends_on("gettext")

    def configure_args(self):
        args = ["--disable-gss", "--with-rpcgen=internal"]
        if "intl" in self.spec["gettext"].libs.names:
            args.append("LIBS=-lintl")
        return args
