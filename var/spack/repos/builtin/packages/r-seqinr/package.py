# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSeqinr(RPackage):
    """Biological Sequences Retrieval and Analysis.

    Exploratory data analysis and data visualization for biological sequence
    (DNA and protein) data. Seqinr includes utilities for sequence data
    management under the ACNUC system described in Gouy, M. et al. (1984)
    Nucleic Acids Res. 12:121-127 <doi:10.1093/nar/12.1Part1.121>."""

    cran = "seqinr"

    license("GPL-2.0-or-later")

    version("4.2-36", sha256="931a62a091a7aaaa5efadb1fe85f29e861e2506b75710ba3a6be9b58cb14b225")
    version("4.2-30", sha256="faf8fe533867eeef57fddfa6592e19d5984954d0670c6c7dbeab6411d55fee4b")
    version("4.2-16", sha256="c4f3253832fc255197bdce7b4dd381db606c6b787d2e888751b4963acf3a4032")
    version("4.2-8", sha256="584b34e9dec0320cef02096eb356a0f6115bbd24356cf62e67356963e9d5e9f7")
    version("4.2-5", sha256="de9860759c23af2ec2f2ef03b5dd1cea72c804438eadd369b7d9269bdf8d32fc")
    version("3.4-5", sha256="162a347495fd52cbb62e8187a4692e7c50b9fa62123c5ef98f2744c98a05fb9f")
    version("3.3-6", sha256="42a3ae01331db744d67cc9c5432ce9ae389bed465af826687b9c10216ac7a08d")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@2.10.0:", type=("build", "run"), when="@4.2-30:")
    depends_on("r-ade4", type=("build", "run"))
    depends_on("r-segmented", type=("build", "run"))
    depends_on("zlib-api")
