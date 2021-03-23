# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Dysco(CMakePackage):
    """Dysco is a compressing storage manager for Casacore mearement sets."""

    homepage = "https://github.com/aroffringa/dysco"
    url      = "https://github.com/aroffringa/dysco/archive/v1.2.tar.gz"

    version('1.2', sha256='dd992c5a13df67173aa1d3f6dc5df9b51b0bea2fe77bc08f5be7a839be741269')

    depends_on('casacore')
    depends_on('gsl')
    depends_on('boost+date_time+python')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
