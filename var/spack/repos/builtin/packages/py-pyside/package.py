# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyPyside(PythonPackage):
    """Python bindings for Qt."""
    homepage = "https://pypi.python.org/pypi/pyside"
    url      = "https://pypi.io/packages/source/P/PySide/PySide-1.2.2.tar.gz"

    # More recent versions of PySide2 (for Qt5) have been taken under
    # the offical Qt umbrella.  For more information, see:
    # http://wiki.qt.io/Qt_for_Python_Development_Getting_Started

    # Version 1.2.4 claims to not work with Python 3.5, mostly
    # because it hasn't been tested.  Otherwise, it's the same as v1.2.3
    # https://github.com/PySide/pyside-setup/issues/58
    # Meanwhile, developers have moved onto pyside2 (for Qt5),
    # and show little interest in certifying PySide 1.2.4 for Python.
    version('1.2.4', sha256='1421bc1bf612c396070de9e1ffe227c07c1f3129278bc7d30c754b5146be2433')  # rpath problems

    # v1.2.2 does not work with Python3
    version('1.2.2', sha256='53129fd85e133ef630144c0598d25c451eab72019cdcb1012f2aec773a3f25be', preferred=True)

    depends_on('cmake', type='build')

    depends_on('py-setuptools', type='build')
    depends_on('py-sphinx', type=('build', 'run'))
    depends_on('qt@4.5:4.9')
    depends_on('libxml2@2.6.32:')
    depends_on('libxslt@1.1.19:')

    def patch(self):
        """Undo PySide RPATH handling and add Spack RPATH."""
        # Figure out the special RPATH
        pypkg = self.spec['python'].package
        rpath = self.rpath
        rpath.append(os.path.join(
            self.prefix, pypkg.site_packages_dir, 'PySide'))

        # Fix subprocess.mswindows check for Python 3.5
        # https://github.com/pyside/pyside-setup/pull/55
        filter_file(
            '^if subprocess.mswindows:',
            'mswindows = (sys.platform == "win32")\r\nif mswindows:',
            "popenasync.py")
        filter_file(
            '^    if subprocess.mswindows:',
            '    if mswindows:',
            "popenasync.py")

        # Add Spack's standard CMake args to the sub-builds.
        # They're called BY setup.py so we have to patch it.
        filter_file(
            r'OPTION_CMAKE,',
            r'OPTION_CMAKE, ' + (
                '"-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE", '
                '"-DCMAKE_INSTALL_RPATH=%s",' % ':'.join(rpath)),
            'setup.py')

        # PySide tries to patch ELF files to remove RPATHs
        # Disable this and go with the one we set.
        if self.spec.satisfies('@1.2.4:'):
            rpath_file = 'setup.py'
        else:
            rpath_file = 'pyside_postinstall.py'

        filter_file(r'(^\s*)(rpath_cmd\(.*\))', r'\1#\2', rpath_file)

        # TODO: rpath handling for PySide 1.2.4 still doesn't work.
        # PySide can't find the Shiboken library, even though it comes
        # bundled with it and is installed in the same directory.

        # PySide does not provide official support for
        # Python 3.5, but it should work fine
        filter_file("'Programming Language :: Python :: 3.4'",
                    "'Programming Language :: Python :: 3.4',\r\n        "
                    "'Programming Language :: Python :: 3.5'",
                    "setup.py")

    def build_args(self, spec, prefix):
        return ['--jobs={0}'.format(make_jobs)]
