# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqt4(SIPPackage):
    """PyQt is a set of Python v2 and v3 bindings for The Qt Company's Qt
    application framework and runs on all platforms supported by Qt including
    Windows, OS X, Linux, iOS and Android. PyQt4 supports Qt v4 and will build
    against Qt v5."""

    homepage = "https://www.riverbankcomputing.com/software/pyqt/intro"
    url      = "http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.12.3/PyQt4_gpl_x11-4.12.3.tar.gz"

    sip_module = 'PyQt4.sip'

    version('4.12.3', sha256='a00f5abef240a7b5852b7924fa5fdf5174569525dc076cd368a566619e56d472')
    version('4.11.3', sha256='853780dcdbe2e6ba785d703d059b096e1fc49369d3e8d41a060be874b8745686',
            url='http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.3/PyQt-x11-gpl-4.11.3.tar.gz')

    # API files can be installed regardless if QScintilla is installed or not
    variant('qsci_api', default=False, description='Install PyQt API file for QScintilla')

    # Supposedly can also be built with Qt 5 compatibility layer
    depends_on('qt@:4')
    depends_on('py-sip@:4.19.18 module=PyQt4.sip')

    # https://www.riverbankcomputing.com/static/Docs/PyQt4/installation.html
    def configure_file(self):
        return 'configure-ng.py'

    def configure_args(self):
        args = [
            '--pyuic4-interpreter', self.spec['python'].command.path,
            '--sipdir', self.prefix.share.sip.PyQt4,
            '--stubsdir', join_path(site_packages_dir, 'PyQt4')
        ]
        if '+qsci_api' in self.spec:
            args.extend(['--qsci-api',
                         '--qsci-api-destdir', self.prefix.share.qsci])
        return args
