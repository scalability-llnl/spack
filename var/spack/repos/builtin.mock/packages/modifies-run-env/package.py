# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ModifiesRunEnv(Package):
    """Dependency package which needs to make shell modifications to run"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    def setup_run_environment(self, env):
        env.set('DEPENDENCY_ENV_VAR', '1')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
