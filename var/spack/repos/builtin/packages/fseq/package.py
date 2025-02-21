# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fseq(Package):
    """F-Seq: A Feature Density Estimator for High-Throughput Sequence Tags"""

    homepage = "https://fureylab.web.unc.edu/software/fseq/"
    url = (
        "http://html-large-files-dept-fureylab.cloudapps.unc.edu/fureylabfiles/fseq/fseq_1.84.tgz"
    )

    version("1.84", sha256="22d603a51f127cb86cdecde9aeae14d273bb98bcd2b47724763ab3b3241a6e68")

    depends_on("java", type=("build", "run"))

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
        install("mapviewToBed.pl", prefix.bin)
