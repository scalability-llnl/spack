# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lynx(AutotoolsPackage):
    """Lynx is the text web browser."""

    homepage = "https://lynx.invisible-island.net/"
    url = "https://invisible-mirror.net/archives/lynx/tarballs/lynx2.8.9rel.1.tar.gz"

    license("GPL-2.0-only")

    version("2.9.2", sha256="99f8f28f860094c533100d1cedf058c27fb242ce25e991e2d5f30ece4457a3bf")
    version("2.8.9.1", sha256="a46e4167b8f02c066d2fe2eafcc5603367be0e3fe2e59e9fc4eb016f306afc8e")

    depends_on("c", type="build")  # generated
    depends_on("ncurses", type=("build", "run"))
    depends_on("openssl", type=("build", "run"))

    def configure_args(self):
        args = []

        args.append("--with-ssl")

        return args

    def url_for_version(self, version):
        version_str = version.string
        index = version_str.rfind(".")
        tmp = list(version_str)
        if index >= 0:
            tmp.insert(index, "rel")
            version_str = "".join(tmp)
        else:
            version_str = version
        url = "https://invisible-mirror.net/archives/lynx/tarballs/lynx{0}.tar.gz".format(
            version_str
        )
        return url
