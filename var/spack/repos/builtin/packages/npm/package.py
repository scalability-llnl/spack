# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

from spack.package import *


# NOTE: not actually an Autotools package
class Npm(Package):
    """npm: A package manager for javascript."""

    homepage = "https://github.com/npm/cli"
    # base http://www.npmjs.com/
    url      = "https://registry.npmjs.org/npm/-/npm-6.13.4.tgz"

    version('6.14.9', sha256='1e0e880ce0d5adf0120fb3f92fc8e5ea5bac73681d37282615d074ff670f7703')
    version('6.14.8', sha256='fe8e873cb606c06f67f666b4725eb9122c8927f677c8c0baf1477f0ff81f5a2c')
    version('6.13.7', sha256='6adf71c198d61a5790cf0e057f4ab72c6ef6c345d72bed8bb7212cb9db969494')
    version('6.13.4', sha256='a063290bd5fa06a8753de14169b7b243750432f42d01213fbd699e6b85916de7')
    version('3.10.9', sha256='fb0871b1aebf4b74717a72289fade356aedca83ee54e7386e38cb51874501dd6')
    version('3.10.5', sha256='ff019769e186152098841c1fa6325e5a79f7903a45f13bd0046a4dc8e63f845f')

    depends_on('node-js', type=('build', 'run'))

    # npm 6.13.4 ships with node-gyp 5.0.5, which contains several Python 3
    # compatibility issues on macOS. Manually update to node-gyp 6.0.1 for
    # full Python 3 support.
    resource(name='node-gyp', destination='node-gyp',
             url='https://registry.npmjs.org/node-gyp/-/node-gyp-6.0.1.tgz',
             sha256='bbc0e137e17a63676efc97a0e3b1fcf101498a1c2c01c3341cd9491f248711b8')
    resource(name='env-paths', destination='env-paths',
             url='https://registry.npmjs.org/env-paths/-/env-paths-2.2.0.tgz',
             sha256='168b394fbca60ea81dc84b1824466df96246b9eb4d671c2541f55f408a264b4c')

    phases = ['configure', 'build', 'install']

    def patch(self):
        shutil.rmtree('node_modules/node-gyp')
        install_tree('node-gyp/package', 'node_modules/node-gyp')
        filter_file(r'"node-gyp": "\^5\..*"', '"node-gyp": "^6.0.1"',
                    'package.json')
        install_tree('env-paths/package', 'node_modules/env-paths')

    def configure(self, spec, prefix):
        configure('--prefix={0}'.format(prefix))

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make('install')

    def setup_dependent_build_environment(self, env, dependent_spec):
        npm_config_cache_dir = "%s/npm-cache" % dependent_spec.prefix
        if not os.path.isdir(npm_config_cache_dir):
            mkdirp(npm_config_cache_dir)
        env.set('npm_config_cache', npm_config_cache_dir)

    def setup_dependent_run_environment(self, env, dependent_spec):
        npm_config_cache_dir = "%s/npm-cache" % dependent_spec.prefix
        if not os.path.isdir(npm_config_cache_dir):
            mkdirp(npm_config_cache_dir)
        env.set('npm_config_cache', npm_config_cache_dir)
