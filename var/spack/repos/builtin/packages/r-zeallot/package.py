# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RZeallot(RPackage):
    """Provides a %<-% operator to perform multiple, unpacking, and
    destructuring assignment in R. The operator unpacks the right-hand side of
    an assignment into multiple values and assigns these values to variables on
    the left-hand side of the assignment."""

    homepage = "https://github.com/nteetor/zeallot"
    url      = "https://cloud.r-project.org/src/contrib/zeallot_0.1.0.tar.gz"
    listurl  = "https://cloud.r-project.org/src/contrib/Archive/zeallot"

    version('0.1.0', sha256='439f1213c97c8ddef9a1e1499bdf81c2940859f78b76bc86ba476cebd88ba1e9')
