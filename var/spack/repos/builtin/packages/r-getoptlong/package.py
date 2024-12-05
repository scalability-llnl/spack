# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGetoptlong(RPackage):
    """Parsing Command-Line Arguments and Simple Variable Interpolation.

    This is yet another command-line argument parser which wraps the powerful
    Perl module Getopt::Long and with some adaptation for easier use in R. It
    also provides a simple way for variable interpolation in R."""

    cran = "GetoptLong"

    version("1.0.5", sha256="8c237986ed3dfb72d956ad865ef7768644eebf144675ad66140acfd1aca9d701")
    version("0.1.7", sha256="b9a98881db407eae9b711c4fa9170168fd5f3be1f8485cd8f28d0a60ace083ba")
    version("0.1.6", sha256="f526f006e3ed8507f1f236430ac9e97341c1ee9c207fbb68f936dd4d377b28b5")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.3.0:", type=("build", "run"), when="@1.0.5:")
    depends_on("r-rjson", type=("build", "run"))
    depends_on("r-globaloptions@0.1.0:", type=("build", "run"))
    depends_on("r-crayon", type=("build", "run"), when="@1.0.5:")

    # The CRAN site lists SystemRequirments as: Perl, Getopt::Long. The
    # Getop::Long package will be installed with Perl so just depend on perl.
    depends_on("perl")
