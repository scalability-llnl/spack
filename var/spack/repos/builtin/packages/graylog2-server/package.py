# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Graylog2Server(Package):
    """Free and open source log management."""

    homepage = "https://www.graylog.org/"
    url = "https://github.com/Graylog2/graylog2-server/archive/3.2.4.tar.gz"

    license("GPL-3.0-or-later")

    version("3.2.4", sha256="d34cc9fd42b2ee0b872c0f644fe53ef9b2e9790029c5d2182f782f66f1e1d99d")
    version("3.2.3", sha256="6da5ba1da897a371a490a6ba7c9d017a479a22e3c16a39280a49e61f551280c0")
    version("3.2.2", sha256="dc7baa5c0e451b0927b28320c4d9ca19810f4690eb2c521ed8a8272c99fb3bc3")
    version("3.2.1", sha256="f570dbb557888ca4dbc932fb6ed840dbb616b9ed50e034d17de69a69f08d1aec")
    version("3.2.0", sha256="094eed607d0d0a7c380825d6507c1e40a53c4493b5f9fe8ae5a3ddd86521711e")

    depends_on("java@8", type=("build", "run"))

    def install(self, spec, prefix):
        install_tree(".", prefix)
