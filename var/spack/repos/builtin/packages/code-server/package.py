# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CodeServer(Package):
    """code-server is VS Code running on a remote server,
    accessible through the browser."""

    homepage = "https://coder.com/docs/code-server/latest"
    url = "https://github.com/coder/code-server/releases/download/v4.4.0/code-server-4.4.0-linux-amd64.tar.gz"

    version("4.96.4", sha256="b3f9025d00f2cdf61caf83945ef7225d4a3eb576c4c007e45868f45713e39c8e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        install_tree(".", prefix)

        if spec.version <= Version("3.1.1"):
            mkdir(prefix.bin)
            symlink("{0}/code-server".format(prefix), prefix.bin)
