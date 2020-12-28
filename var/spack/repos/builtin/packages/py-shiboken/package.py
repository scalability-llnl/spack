# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyShiboken(PythonPackage):
    """Shiboken generates bindings for C++ libraries using CPython."""
    homepage = "https://shiboken.readthedocs.org/"
    url      = "https://pypi.io/packages/source/S/Shiboken/Shiboken-1.2.2.tar.gz"

    version('1.2.2', sha256='0baee03c6244ab56e42e4200d0cb5e234682b11cc296ed0a192fe457d054972f')

    depends_on('cmake', type='build')

    depends_on("py-setuptools", type='build')
    depends_on("py-sphinx", type=('build', 'run'))
    depends_on("libxml2")
    depends_on("qt@:4.8")

    def patch(self):
        """Undo Shiboken RPATH handling and add Spack RPATH."""
        # Add Spack's standard CMake args to the sub-builds.
        # They're called BY setup.py so we have to patch it.
        pypkg = self.spec['python'].package
        rpath = self.rpath
        rpath.append(os.path.join(
            self.prefix, pypkg.site_packages_dir, 'Shiboken'))

        filter_file(
            r'OPTION_CMAKE,',
            r'OPTION_CMAKE, ' + (
                '"-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE", '
                '"-DCMAKE_INSTALL_RPATH=%s",' % ':'.join(rpath)),
            'setup.py')

        # Shiboken tries to patch ELF files to remove RPATHs
        # Disable this and go with the one we set.
        filter_file(
            r'^\s*rpath_cmd\(shiboken_path, srcpath\)',
            r'#rpath_cmd(shiboken_path, srcpath)',
            'shiboken_postinstall.py')

    def build_args(self, spec, prefix):
        return ['--jobs={0}'.format(make_jobs)]
