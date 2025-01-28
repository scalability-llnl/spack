# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPs(RPackage):
    """List, Query, Manipulate System Processes.

    List, query and manipulate all system processes, on 'Windows', 'Linux' and
    'macOS'."""

    cran = "ps"

    license("MIT")

    version("1.7.7", sha256="46fedcb2b8faa94ea1451e48e6f31a1e4ed3b12f529e645f9efcfca1003d22f2")
    version("1.7.5", sha256="1abc3ae3c55797b994973f7e43bf5c7bbb4da649a0dcfad36675e196dba4cb4e")
    version("1.7.2", sha256="9225ebdedb5c1b245bb38b01ce88084c0fc7eafcff6c4fda2e299003ace6b21a")
    version("1.7.1", sha256="9c458a377d47cc972d3cd0b2a17d0b7ad3cf3b62226410803072089a57a55ef1")
    version("1.7.0", sha256="8220cf32c6a12c908b6b7669f96b57445d3147a1aa484b9b5209e0f3fd4b52e1")
    version("1.6.0", sha256="89ad7ddc5e0818bccacfd0673ddf2da0892ac2a3b4d3a821e40884ab1e96bf31")
    version("1.5.0", sha256="7461a196f55557feda569a9791ad851c884f9a2dd71671655ed17cb048fafe96")
    version("1.3.0", sha256="289193d0ccd2db0b6fe8702e8c5711e935219b17f90f01a6e9684982413e98d1")
    version("1.2.1", sha256="bd7207164e6557a9e4213c4b00dc5dc23d7705ab290569765998640b16a3beff")
    version("1.1.0", sha256="5d5240d5bf1d48c721b3fdf47cfc9dbf878e388ea1f057b764db05bffdc4a9fe")
    version("1.0.0", sha256="9bdaf64aaa44ae11866868402eb75bf56c2e3022100476d9b9dcd16ca784ffd8")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@1.7.0:")
