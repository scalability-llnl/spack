# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Glusterfs(AutotoolsPackage):
    """Gluster is a software defined distributed storage that can scale to
    several petabytes. It provides interfaces for object, block and file
    storage."""

    homepage = "https://www.gluster.org/"
    url = "https://download.gluster.org/pub/gluster/glusterfs/7/7.3/glusterfs-7.3.tar.gz"
    list_url = "https://download.gluster.org/pub/gluster/glusterfs/"
    list_depth = 2

    license("LGPL-3.0-or-later")

    version("7.3", sha256="2401cc7c3f5488f6fc5ea09ce2ab30c918612f592571fb3de6124f8482ad4954")
    version("7.2", sha256="8e43614967b90d64495fbe2c52230dd72572ce219507fb48bc317b1c228a06e1")
    version("7.1", sha256="ffc5bd78b079009382bd01391865646bc9b2e8e72366afc96d62ba891dd9dbce")
    version("7.0", sha256="8a872518bf9bd4dc1568f45c716bcde09e3bf7abf5b156ea90405e0fc2e9f07b")
    version("6.8", sha256="41e855bdc456759c8c15ef494c636a25cc7b62c55ad132ecd55bec05df64793f")
    version("6.7", sha256="e237dd59a2d5b73e156b0b71df49ff64a143b3aaf8f0a65daaf369bb40f5e923")

    depends_on("c", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("rpcsvc-proto")
    depends_on("acl")
    depends_on("uuid")
    depends_on("libtirpc")
    depends_on("userspace-rcu")
    depends_on("pkgconfig", type="build")

    def url_for_version(self, version):
        url = "https://download.gluster.org/pub/gluster/glusterfs/{0}/{1}/glusterfs-{1}.tar.gz"
        return url.format(version.up_to(1), version)

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
