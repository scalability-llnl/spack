# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openipmi(AutotoolsPackage):
    """The Open IPMI project aims to develop an open code base
    to allow access to platform information using Intelligent
    Platform Management Interface (IPMI)."""

    homepage = "https://sourceforge.net/projects/openipmi/"
    url = "https://sourceforge.net/projects/openipmi/files/OpenIPMI%202.0%20Library/OpenIPMI-2.0.29.tar.gz"

    version("2.0.35", sha256="b059114f6299d73f04ff6e76a0857a0ab81aa362dee99644d256b223872437ad")
    version("2.0.29", sha256="2244124579afb14e569f34393e9ac61e658a28b6ffa8e5c0d2c1c12a8ce695cd")
    version("2.0.28", sha256="8e8b1de2a9a041b419133ecb21f956e999841cf2e759e973eeba9a36f8b40996")
    version("2.0.27", sha256="f3b1fafaaec2e2bac32fec5a86941ad8b8cb64543470bd6d819d7b166713d20b")

    depends_on("c", type="build")  # generated

    depends_on("popt", type="link")
    depends_on("python", type=("build", "link", "run"))
    depends_on("perl", type=("build", "link", "run"))
    depends_on("termcap", type="link")
    depends_on("ncurses", type="link")
    depends_on("readline", type="link")

    patch("readline.patch", when="@2.0.27")

    def configure_args(self):
        args = ["LIBS=" + self.spec["ncurses"].libs.link_flags]
        return args

    def install(self, spec, prefix):
        make("install", parallel=False)
