# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class PySip(Package):
    """SIP is a tool that makes it very easy to create Python bindings for C
       and C++ libraries."""

    homepage = "https://www.riverbankcomputing.com/software/sip/intro"
    url      = "https://www.riverbankcomputing.com/hg/sip/archive/4.19.21.tar.gz"
    list_url = "https://www.riverbankcomputing.com/hg/sip/archive"
    hg       = "https://www.riverbankcomputing.com/hg/sip"

    version('develop', hg=hg)  # wasn't actually able to clone this
    version('4.19.21', sha256='3bfd58e875a87471c00e008f25a01d8312885aa01efc4f688e5cac861c8676e4')
    version('4.19.20', sha256='475f85277a6601c406ade508b6c935b9f2a170c16fd3ae9dd4cdee7a4f7f340d')
    version('4.19.19', sha256='348cd6229b095a3090e851555814f5147bffcb601cec891f1038eb6b38c9d856')
    version('4.19.18', sha256='e274a8b9424047c094a40a8e70fc5e596c191cb8820472846d7bf739e461b2e8')
    version('4.19.15', sha256='02bff1ac89253e12cdf1406ad39f841d0e264b0d96a7de13dfe9e29740df2053')
    version('4.19.13', sha256='92193fcf990503bf29f03e290efc4ee1812d556efc18acf5c8b88c090177a630')

    variant('module', default='sip', description='Name of private SIP module',
            values=str, multi=False)

    extends('python')

    depends_on('flex', type='build', when='@develop')
    depends_on('bison', type='build', when='@develop')

    # https://www.riverbankcomputing.com/static/Docs/sip/installation.html
    phases = ['configure', 'build', 'install']

    @run_before('configure')
    def prepare(self):
        if not os.path.exists('configure.py'):
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
