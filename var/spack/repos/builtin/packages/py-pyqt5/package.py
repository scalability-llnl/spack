# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyqt5(SIPPackage):
    """PyQt is a set of Python v2 and v3 bindings for The Qt Company's Qt
    application framework and runs on all platforms supported by Qt including
    Windows, OS X, Linux, iOS and Android. PyQt5 supports Qt v5."""

    homepage = "https://www.riverbankcomputing.com/software/pyqt/intro"
    url      = "https://www.riverbankcomputing.com/static/Downloads/PyQt5/5.13.0/PyQt5_gpl-5.13.0.tar.gz"
    list_url = "https://www.riverbankcomputing.com/software/pyqt/download5"

    sip_module = 'PyQt5.sip'
    import_modules = [
        'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtHelp',
        'PyQt5.QtMultimedia', 'PyQt5.QtMultimediaWidgets', 'PyQt5.QtNetwork',
        'PyQt5.QtOpenGL', 'PyQt5.QtPrintSupport', 'PyQt5.QtQml',
        'PyQt5.QtQuick', 'PyQt5.QtSvg', 'PyQt5.QtTest', 'PyQt5.QtWebChannel',
        'PyQt5.QtWebSockets', 'PyQt5.QtWidgets', 'PyQt5.QtXml',
        'PyQt5.QtXmlPatterns'
    ]

    version('5.13.0', sha256='0cdbffe5135926527b61cc3692dd301cd0328dd87eeaf1313e610787c46faff9')

    variant('qsci', default=False, description='Build with QScintilla python bindings')

    # Without opengl support, I got the following error:
    # sip: QOpenGLFramebufferObject is undefined
    depends_on('qt@5:+opengl')
    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-enum34', type=('build', 'run'), when='^python@:3.3')

    depends_on('qscintilla', when='+qsci')

    # https://www.riverbankcomputing.com/static/Docs/PyQt5/installation.html
    def configure_args(self):
        return [
            '--pyuic5-interpreter', self.spec['python'].command.path,
            '--sipdir', self.prefix.share.sip.PyQt5,
            '--stubsdir', join_path(site_packages_dir, 'PyQt5'),
            '--qsci-api-destdir', self.prefix.share+'/qsci'
        ]

    @run_after('install')
    def make_qsci(self):
        if '+qsci' in self.spec:
            with working_dir(str(self.spec['qscintilla'].prefix)+'/share/qscintilla/src/Python'):
                pydir = join_path(site_packages_dir, 'PyQt5')
                pyqtsipdir = '--pyqt-sipdir=' + self.prefix.share.sip.PyQt5
                carg_sipinc = '--sip-incdir=' + self.prefix+'/include/python'+str(self.spec['python'].version.up_to(2))

                carg_inc = '--qsci-incdir='+self.spec['qscintilla'].prefix.include
                carg_lib = '--qsci-libdir='+self.spec['qscintilla'].prefix.lib
#                carg_sip = '--qsci-sipdir='+self.spec['qscintilla'].prefix+'/share/sip'
                carg_sip = '--qsci-sipdir='+self.prefix.share.sip.PyQt5
                carg_api = '--apidir='+self.prefix+'/share/qsci'
                carg_dest = '--destdir='+pydir
                carg_stub = '--stubsdir='+pydir

                python = which('python')

                python('configure.py', '--pyqt=PyQt5', carg_inc, carg_lib, carg_sip, carg_api, carg_dest, pyqtsipdir, carg_sipinc, carg_stub)

                # Add config options to avoid build errors
                # "QAbstractScrollArea: No such file or directory"
                # "qprinter.h: No such file or directory"
                qscipro=FileFilter('Qsci/Qsci.pro')
                qscipro.filter('TEMPLATE = lib',
                               'TEMPLATE = lib\nQT += widgets\nQT += printsupport')

                make()


                # TODO does INSTALL_ROOT already exist?

                makefile = FileFilter('Makefile')
                makefile.filter(r'\$\(INSTALL_ROOT\)','')
                makefile = FileFilter('Qsci/Makefile')
                makefile.filter(r'\$\(INSTALL_ROOT\)','')

                make('install')
