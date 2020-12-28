# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pasta(Package):
    """PASTA (Practical Alignment using SATe and Transitivity)"""

    homepage = "https://github.com/smirarab/pasta"
    git      = "https://github.com/smirarab/pasta"

    version('1.8.3', commit='738bec5e0d5a18d013c193d7453374bed47456c9')

    depends_on('python@2.7:')
    depends_on('py-dendropy')
    depends_on('java')

    resource(
        name='tools',
        git='https://github.com/smirarab/sate-tools-linux',
        commit='90fb074d61af554e94d1a67583dd3a80b11417ea',
        destination='.'
    )

    def setup_build_environment(self, env):
        tools = join_path(self.prefix, 'sate-tools-linux')
        env.set('PASTA_TOOLS_DEVDIR', tools)

    def install(self, spec, prefix):
        # build process for pasta is very hacky -- uses hard links to source
        # install the tree first so links don't break
        install_tree('.', prefix)

        # run the 'build' from within the prefix
        python = which('python2.7')

        with working_dir(prefix):
            python('setup.py', 'develop')
