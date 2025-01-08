# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RChron(RPackage):
    """Chronological objects which can handle dates and times.

    Provides chronological objects which can handle dates and times."""

    cran = "chron"

    license("GPL-2.0-only")

    version("2.3-61", sha256="a096957625a0438075b3486322ee07c753c7c4ba3efcd04a3ac92476d6c43b9b")
    version("2.3-60", sha256="0e0675cec55b6cea87fc5776846215e0445442554684120079e66013067491ee")
    version("2.3-58", sha256="057fc628cde330c22b9d20365316d3632c2d217f4f2f97d39b1d1a2c93f766d0")
    version("2.3-57", sha256="9645d86a84d1afc12a0accf4f826fdd40e6d050a313424ad70f8085e8f19c232")
    version("2.3-56", sha256="863ecbb951a3da994761ea9062fa96d34e94e19fbc4122521ac179274dfa3f5d")
    version("2.3-53", sha256="521814b46ba958eae28e29d8766aebd285da5e6fa16c5806603df3ae39f77309")
    version("2.3-52", sha256="c47fcf4abb635babe6337604c876d4853d8a24639a98b71523746c56ce75b4a0")
    version("2.3-47", sha256="9a8c771021165de517e54c3369c622aaac1bf3e220a2fbf595aba285e60445f6")

    depends_on("r@2.12.0:", type=("build", "run"))
