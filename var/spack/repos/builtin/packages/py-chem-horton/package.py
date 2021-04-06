# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import platform


class PyChemHorton(PythonPackage):
    """HORTON: Helpful Open-source Research TOol for N-fermion systems.
       Copyright (C) 2011-2016 The HORTON Development Team
    """

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://theochem.github.io/horton"
    url      = "https://github.com/theochem/horton/releases/download/2.1.1/horton-2.1.1.tar.gz"

    maintainers = ['frobnitzem']

    version('2.1.1', sha256='4b3f87920d881030ba80f097326a744de2cfee5316aa4499cc9a6501f64b5060')

    depends_on('python@2.7:2.99', type=('build', 'run'))
    # note: The py-setuptools dep should be type='build', but build_systems/python.py
    # adds "args += ['--single-version-externally-managed', '--root=/']"
    # This conflicts with the present setuptools version (required by python2).
    # So, it's hacked to run-dep here.
    depends_on('py-setuptools@:44.1.0',   type='run')
    # depends_on('py-nose@1.1.2:',        type=('test'))
    depends_on('py-numpy@1.9.1:1.16', type=('build', 'run'))
    depends_on('py-scipy@0.11.0:1.2.3', type=('build', 'run'))
    depends_on('py-cython@0.24.1:', type=('build'))
    depends_on('py-h5py@2.2.1:2.10.0', type=('build', 'run'))
    depends_on('py-matplotlib@1.0:2.2.5', type=('build', 'run'))
    depends_on('libxc@2.2.2:')
    depends_on('libint@2.0.3: tune=cp2k-lmax-7')
    depends_on('curl@7.0:',     type=('build', 'run'))

    patch("cext.patch")

    @run_before('build')
    def gen_setup_cfg(self):
        spec = self.spec

        def write_library_dirs(f, dirs):
            f.write('library_dirs = {0}\n'.format(dirs))
            if not ((platform.system() == 'Darwin') and
                    (Version(platform.mac_ver()[0]).up_to(2) == Version(
                        '10.12'))):
                # f.write('rpath = {0}\n'.format(dirs))
                f.write('extra_link_args = -Wl,-rpath={0}\n'.format(dirs))

        deps = {'libxc':  {'name': 'libxc', 'libraries': 'xc'},
                'libint': {'name': 'libint2', 'libraries': 'int2'}}
        for key, val in deps.items():
            # val['libraries'] = ','.join(spec[key].libs.names)
            val['library_dirs'] = spec[key].prefix + '/lib'
            val['include_dirs'] = spec[key].prefix + '/include'

        # Tell horton where to find libraries
        with open('setup.cfg', 'w') as f:
            for key, val in deps.items():
                f.write('[{0}]\n'.format(val['name']))
                f.write('libraries = {0}\n'.format(val['libraries']))
                write_library_dirs(f, val['library_dirs'])
                f.write('include_dirs = {0}\n'.format(val['include_dirs']))
                if key == 'libint':
                    f.write('extra_compile_args = -DLIBINT2_MAX_AM_ERI=7')
