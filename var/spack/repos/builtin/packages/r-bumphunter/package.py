# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBumphunter(RPackage):
    """Bump Hunter.

    Tools for finding bumps in genomic data"""

    bioc = "bumphunter"

    version("1.42.0", commit="0eb2808a04920aaba00e1ce3e9dff503596e931f")
    version("1.40.0", commit="3de207a3659859737d4c748fc8023694943da43b")
    version("1.38.0", commit="06e2fa87b342d48793d0d2f1f7d94a95a6613995")
    version("1.36.0", commit="db50fcf7798c2eddfe48fd510d081dda82f2ee4e")
    version("1.32.0", commit="b7d39c2a6385ca217dceefc918b3ccd5c31bbaa0")
    version("1.26.0", commit="606bee8708a0911ced3efb197970b4c9fa52f2fa")
    version("1.24.5", commit="29b874033a38e86103b58ef2d4a55f285758147b")
    version("1.22.0", commit="fb71b193f4ef7fa12d100441e6eb498765f7afde")
    version("1.20.0", commit="c9d8e7ab0c19299988e5d7fa74970312e9a1eac0")
    version("1.16.0", commit="1c3ab4d1fd2d75b1586ccef12665960b3602080a")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@1.20.0:")
    depends_on("r@3.5:", type=("build", "run"), when="@1.24.5:")
    depends_on("r-s4vectors@0.9.25:", type=("build", "run"))
    depends_on("r-iranges@2.3.23:", type=("build", "run"))
    depends_on("r-genomeinfodb", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-foreach", type=("build", "run"))
    depends_on("r-iterators", type=("build", "run"))
    depends_on("r-locfit", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"))
    depends_on("r-limma", type=("build", "run"))
    depends_on("r-dorng", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-genomicfeatures", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
