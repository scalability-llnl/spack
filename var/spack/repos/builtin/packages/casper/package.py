# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Casper(MakefilePackage):
    """CASPER (Context-Aware Scheme for Paired-End Read) is state-of-the art
       merging tool in terms of accuracy and robustness. Using this
       sophisticated merging method, we could get elongated reads from the
       forward and reverse reads."""

    homepage = "http://best.snu.ac.kr/casper/index.php?name=main"
    url      = "http://best.snu.ac.kr/casper/program/casper_v0.8.2.tar.gz"

    version('0.8.2', sha256='3005e165cebf8ce4e12815b7660a833e0733441b5c7e5ecbfdccef7414b0c914')

    depends_on('jellyfish@2.2.3:')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    conflicts('%gcc@7.1.0')

    def install(self, spec, prefix):
        install_tree('.', prefix)

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.spec.prefix)
