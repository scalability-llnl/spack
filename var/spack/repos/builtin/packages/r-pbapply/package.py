# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPbapply(RPackage):
    """Adding Progress Bar to '*apply' Functions.

    A lightweight package that adds progress bar to vectorized R functions
    ('*apply'). The implementation can easily be added to functions where
    showing the progress is useful (e.g. bootstrap). The type and style of the
    progress bar (with percentages or remaining time) can be set through
    options. Supports several parallel processing backends."""

    cran = "pbapply"

    license("GPL-2.0-or-later")

    version("1.7-2", sha256="aeed8c8c308c7e3827daf10b01b8ed4b88c1d68cea57d72d67c600c0ce0dae13")
    version("1.7-0", sha256="64b8e931e0a09031c20b66173ce80a646043b8f135d329bc86226a11c6b706c0")
    version("1.5-0", sha256="effdfee286e5ba9534dc2ac3cee96590a37f5cd2af28c836d00c25ca9f070a55")
    version("1.4-3", sha256="8fe6287535be766b5a688810e2cc1ca4e668ac6b42b6e832473fe5701133eb21")
    version("1.4-1", sha256="b3633349181db944e1dfc4422b4728a6562e454117a232cbb51633906cd27cad")
    version("1.3-4", sha256="cdfdaf9b8aecbe48daac858aecaf65a766b74a363d1eb7cd6ebf27c0549f6552")
    version("1.3-3", sha256="7379b21d1176db5769f5cac858dd12c975736e80a600870180cec9625cf51047")
    version("1.3-2", sha256="196367da93fcd31431d8e78c177d4afccf9c634513edf24a7229adce2d95b5e9")
    version("1.3-1", sha256="fc4f1ea9d3290bab20a0ec74a3195c8887592b022ab6abb8d7754006a4487114")
    version("1.3-0", sha256="a6d4bf88ade12a3b25662e271329fe54d170596335cba2a2dd210bbb7e8a5936")
    version("1.2-2", sha256="81e5a8a5e0c7ce24b25679d0f69e8773908c9ce569f1e5984e52d4cef33ac34e")

    depends_on("r@3.2.0:", type=("build", "run"))
