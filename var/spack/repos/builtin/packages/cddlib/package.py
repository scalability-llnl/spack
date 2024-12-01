# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cddlib(AutotoolsPackage):
    """The C-library cddlib is a C implementation of the Double Description
    Method of Motzkin et al. for generating all vertices (i.e. extreme points)
    and extreme rays of a general convex polyhedron in R^d given by a system
    of linear inequalities"""

    homepage = "https://people.inf.ethz.ch/fukudak/cdd_home"
    url = "https://github.com/cddlib/cddlib/archive/refs/tags/0.94m.tar.gz"

    license("GPL-2.0-or-later")

    maintainers("NessieCanCode")
    version("0.94m", sha256="70dffdb3369b8704dc75428a1b3c42ab9047b81ce039f12f427e2eb2b1b0dee2")
    version("0.94h", sha256="7382782c3834214b022c8b2898ed775a7bf915f2cb2acb73fa045d6fd9a3de33")

    depends_on("c", type="build")  # generated

    depends_on("gmp", when="@0.94h")

    def url_for_version(self, version):
        if self.spec.satisfies("@:0.94i"):
            url = "https://github.com/cddlib/cddlib/archive/refs/tags/{0}.tar.gz"
        elif self.spec.satisfies("@0.94j:"):
            url = "https://github.com/cddlib/cddlib/releases/download/{0}/cddlib-{0}.tar.gz"
        return url.format(version.dotted)
