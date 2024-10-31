# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class RPhantompeakqualtools(RPackage):
    """Computes informative enrichment and quality measures for
    ChIP-seq/DNase-seq/FAIRE-seq/MNase-seq data. This is a modified version
    of r-spp to be used in conjunction with the phantompeakqualtools
    package."""

    homepage = "https://github.com/kundajelab/phantompeakqualtools"
    url = "https://github.com/kundajelab/phantompeakqualtools/raw/master/spp_1.14.tar.gz"

    version("1.14", sha256="d03be6163e82aed72298e54a92c181570f9975a395f57a69b21ac02b1001520b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("boost@1.41.0:")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("r-catools", type=("build", "run"))
    depends_on("r-snow", type=("build", "run"))
    depends_on("r-snowfall", type=("build", "run"))
    depends_on("r-bitops", type=("build", "run"))
    depends_on("r-rsamtools", type=("build", "run"))

    conflicts("%gcc@6:")

    def setup_build_environment(self, env):
        env.set("BOOST_ROOT", self.spec["boost"].prefix)
