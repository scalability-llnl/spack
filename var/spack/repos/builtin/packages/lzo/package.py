# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lzo(AutotoolsPackage):
    """Real-time data compression library"""

    homepage = "https://www.oberhumer.com/opensource/lzo/"
    url = "https://www.oberhumer.com/opensource/lzo/download/lzo-2.09.tar.gz"

    license("GPL-2.0-or-later")

    version("2.10", sha256="c0f892943208266f9b6543b3ae308fab6284c5c90e627931446fb49b4221a072")
    version("2.09", sha256="f294a7ced313063c057c504257f437c8335c41bfeed23531ee4e6a2b87bcb34c")
    version("2.08", sha256="ac1b3e4dee46febe9fd28737eb7f5692d3232ef1a01da10444394c3d47536614")
    version("2.07", sha256="9298ccf43f856ef00643d110042b2fefe694b569c161aef0c6f8e4ada590e6d4")
    version("2.06", sha256="ff79e6f836d62d3f86ef6ce893ed65d07e638ef4d3cb952963471b4234d43e73")
    version("2.05", sha256="449f98186d76ba252cd17ff1241ca2a96b7f62e0d3e4766f88730dab0ea5f333")

    depends_on("c", type="build")  # generated

    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )

    def configure_args(self):
        args = ["--disable-dependency-tracking"]
        args += self.enable_or_disable("libs")
        return args
