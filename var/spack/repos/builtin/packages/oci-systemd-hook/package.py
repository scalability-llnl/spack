# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OciSystemdHook(AutotoolsPackage):
    """OCI systemd hook enables users to run systemd in docker and OCI
    compatible runtimes such as runc without requiring --privileged flag."""

    homepage = "https://github.com/projectatomic/oci-systemd-hook/"
    url = "https://github.com/projectatomic/oci-systemd-hook/archive/v0.2.0.tar.gz"

    license("GPL-3.0-or-later")

    version("0.2.0", sha256="da1ce3a1fd68752fc27b8f2062daa0d273c211474841ecf14737b10031bedcf5")
    version("0.1.18", sha256="c17291bf5151e972c502ec3cc9b445967823444b1f3917481eb419c9e476649e")
    version("0.1.5", sha256="53f773b055928d0f3d25ccc966d0d0b3ccb4dd00e8ff71a067b105142da22763")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("gettext")
    depends_on("yajl")
    depends_on("uuid")
    depends_on("util-linux")
    depends_on("go-md2man")

    def flag_handler(self, name, flags):
        if name == "ldlibs":
            if "intl" in self.spec["gettext"].libs.names:
                flags.append("-lintl")
        return self.build_system_flags(name, flags)

    def install(self, spec, prefix):
        oci_systemd_hook_jsondir = "oci_systemd_hook_jsondir="
        oci_systemd_hook_jsondir += "{0}/usr/share/containers/oci/hooks.d"
        make("install", oci_systemd_hook_jsondir.format(prefix))
