# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMniPerllib(PerlPackage):
    """MNI Perl Library for scripting long-running scientific computations"""

    homepage = "https://github.com/BIC-MNI/mni-perllib"
    git = "https://github.com/BIC-MNI/mni-perllib.git"

    version("develop", commit="170827f5644820b87bcb2b194494c5ebf0928149")

    patch("no-stdin.patch")

    depends_on("perl-getopt-tabular", type=("build", "run"))
    depends_on("perl-text-format", type=("build", "run"))
