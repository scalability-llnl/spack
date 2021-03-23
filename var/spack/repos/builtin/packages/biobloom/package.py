# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Biobloom(AutotoolsPackage):
    """BioBloom Tools (BBT) provides the means to create filters for a given
       reference and then to categorize sequences."""

    homepage = "https://github.com/bcgsc/biobloom"
    url      = "https://github.com/bcgsc/biobloom/releases/download/2.2.0/biobloomtools-2.2.0.tar.gz"

    version('2.2.0', sha256='5d09f8690f0b6402f967ac09c5b0f769961f3fe3791000f8f73af6af7324f02c')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('sdsl-lite')
    depends_on('sparsehash')
    depends_on('zlib')

    def configure_args(self):
        # newer versions of sdsl-lite introduce tolerable warnings
        # they must disabled to allow the build to continue

        return ['CXXFLAGS=-w', 'CPPFLAGS=-w']
