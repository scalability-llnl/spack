# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OpenIsns(AutotoolsPackage):
    """This is the iSNS server, supporting persistent storage
    of registrations in a file based database."""

    homepage = "https://github.com/open-iscsi/open-isns"
    url = "https://github.com/open-iscsi/open-isns/archive/v0.100.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.100", sha256="b011edbb0f31690aaca902a8ecf4e1f17b01d6c9e9afc51909d26b0993b4328f")
    version("0.99", sha256="a8febecf888d5a38abfa2fcb290194d993b1a7f5bea0cb61f5cf2e9f9e5273c2")
    version("0.98", sha256="c5cbd161e51fb993728c04e56d3da693b73eb3f4e81d17f66eb5b7653c29e8eb")
    version("0.97", sha256="c1c9ae740172e55a1ff33bc22151ec3d916562bf5d60c8420cd64496343683a9")
    version("0.96", sha256="487fd0d87826423ea99dc159826d0b654a5da016ed670d4395a77bfa4f62e2ec")

    depends_on("c", type="build")

    def configure_args(self):
        args = ["--enable-shared"]
        return args

    def install(self, spec, prefix):
        etc_dir = join_path(prefix, "etc")
        var_dir = join_path(prefix, "var")
        make("install", f"etcdir={etc_dir}", f"vardir={var_dir}")
        make("install_hdrs", f"etcdir={etc_dir}", f"vardir={var_dir}")
        make("install_lib", f"etcdir={etc_dir}", f"vardir={var_dir}")
