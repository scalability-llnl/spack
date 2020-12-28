# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PySip(Package):
    """SIP is a tool that makes it very easy to create Python bindings for C
       and C++ libraries."""

    homepage = "https://www.riverbankcomputing.com/software/sip/intro"
    url      = "https://www.riverbankcomputing.com/static/Downloads/sip/4.19.18/sip-4.19.18.tar.gz"
    list_url = "https://www.riverbankcomputing.com/software/sip/download"
    hg       = "https://www.riverbankcomputing.com/hg/sip"

    version('develop', hg=hg)  # wasn't actually able to clone this
    version('4.19.21', sha256='6af9979ab41590e8311b8cc94356718429ef96ba0e3592bdd630da01211200ae')
    version('4.19.20', sha256='04cc2f87ac97e8718d8e1ef036e3ec26050ab44c21f9277618d5b67432fcbfd6')
    version('4.19.19', sha256='5436b61a78f48c7e8078e93a6b59453ad33780f80c644e5f3af39f94be1ede44')
    version('4.19.18', sha256='c0bd863800ed9b15dcad477c4017cdb73fa805c25908b0240564add74d697e1e')
    version('4.19.15', sha256='2b5c0b2c0266b467b365c21376d50dde61a3236722ab87ff1e8dacec283eb610')
    version('4.19.13', sha256='e353a7056599bf5fbd5d3ff9842a6ab2ea3cf4e0304a0f925ec5862907c0d15e')

    variant('module', default='sip', description='Name of private SIP module',
            values=str, multi=False)

    extends('python')

    depends_on('flex', type='build', when='@develop')
    depends_on('bison', type='build', when='@develop')

    # https://www.riverbankcomputing.com/static/Docs/sip/installation.html
    phases = ['configure', 'build', 'install']

    @run_before('configure')
    def prepare(self):
        if self.spec.satisfies('@develop'):
            python('build.py', 'prepare')

    def configure(self, spec, prefix):
        args = [
            '--sip-module={0}'.format(spec.variants['module'].value),
            '--bindir={0}'.format(prefix.bin),
            '--destdir={0}'.format(site_packages_dir),
            '--incdir={0}'.format(python_include_dir),
            '--sipdir={0}'.format(prefix.share.sip),
            '--stubsdir={0}'.format(site_packages_dir),
        ]

        python('configure.py', *args)

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make('install')

    @run_after('install')
    def extend_path_setup(self):
        # See github issue #14121 and PR #15297
        module = self.spec.variants['module'].value
        if module != 'sip':
            module = module.split('.')[0]
            with working_dir(site_packages_dir):
                with open(os.path.join(module, '__init__.py'), 'w') as f:
                    f.write('from pkgutil import extend_path\n')
                    f.write('__path__ = extend_path(__path__, __name__)\n')
