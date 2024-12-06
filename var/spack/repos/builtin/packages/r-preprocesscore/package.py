# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPreprocesscore(RPackage):
    """A collection of pre-processing functions.

    A library of core preprocessing routines."""

    bioc = "preprocessCore"

    version("1.62.0", commit="a6e3d339bc8204d15db4e750bd98f0313490b658")
    version("1.60.0", commit="7f62a7d54776a21ab6c2d3df4668382d531d1ee8")
    version("1.58.0", commit="2995e3e1a8f428a80aee200db42ee44743d893f6")
    version("1.56.0", commit="8f3272219507aa85e0c876fb434dc3b926c22c5d")
    version("1.52.1", commit="91de4ab67315dc2af68554ae3c48823f4b1ea8ac")
    version("1.46.0", commit="8cfc3938c1b08424587f437ed6cd2ec43512500e")
    version("1.44.0", commit="dc1dc61fc562aaff3fd9b11ab0d48c2d6b3a5b81")
    version("1.42.0", commit="2e3a8baeacfaa1526d51252642772ea951015bba")
    version("1.40.0", commit="969bb0e5cbd63d569502ae4e6eaadc1e216646dd")
    version("1.38.1", commit="c58cb4c720eda0f1c733b989b14912093a7c5fbc")

    depends_on("c", type="build")  # generated
