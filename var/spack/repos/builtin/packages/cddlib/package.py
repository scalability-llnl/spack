# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cddlib(AutotoolsPackage):
    """The C-library cddlib is a C implementation of the Double Description
    Method of Motzkin et al. for generating all vertices (i.e. extreme points)
    and extreme rays of a general convex polyhedron in R^d given by a system
    of linear inequalities"""

    homepage = "https://www.inf.ethz.ch/personal/fukudak/cdd_home/"
    url      = "ftp://ftp.math.ethz.ch/users/fukudak/cdd/cddlib-094h.tar.gz"

    version('0.94h', sha256='fe6d04d494683cd451be5f6fe785e147f24e8ce3ef7387f048e739ceb4565ab5')

    # Note: It should be possible to build cddlib also without gmp

    depends_on("gmp")
    depends_on("libtool", type="build")

    def url_for_version(self, version):
        url = "ftp://ftp.math.ethz.ch/users/fukudak/cdd/cddlib-{0}.tar.gz"
        return url.format(version.joined)
