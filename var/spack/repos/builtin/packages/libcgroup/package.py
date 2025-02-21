# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcgroup(AutotoolsPackage):
    """Library of control groups."""

    homepage = "https://github.com/libcgroup/libcgroup/"
    url = "https://github.com/libcgroup/libcgroup/releases/download/v3.1.0/libcgroup-3.1.0.tar.gz"

    license("LGPL-2.1-only")

    version("3.1.0", sha256="976ec4b1e03c0498308cfd28f1b256b40858f636abc8d1f9db24f0a7ea9e1258")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2018-14348
        version("0.41", sha256="e4e38bdc7ef70645ce33740ddcca051248d56b53283c0dc6d404e17706f6fb51")
        version("0.37", sha256="15c8f3febb546530d3495af4e4904b3189c273277ca2d8553dec882cde1cd0f6")
        version("0.36", sha256="8dcd2ae220435b3de736d3efb0023fdf1192d7a7f4032b439f3cf5342cff7b4c")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("linux-pam")
    depends_on("systemd", when="@3.1:")

    def url_for_version(self, version):
        if self.spec.satisfies("@2.0.1:"):
            return f"https://github.com/libcgroup/libcgroup/releases/download/v{version}/libcgroup-{version}.tar.gz"
        else:
            return f"https://github.com/libcgroup/libcgroup/releases/download/v{version}/libcgroup-{version}.tar.bz2"
