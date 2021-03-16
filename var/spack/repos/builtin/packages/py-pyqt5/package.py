# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

    version('5.15.2', sha256='372b08dc9321d1201e4690182697c5e7ffb2e0770e6b4a45519025134b12e4fc')
    version('5.13.1', sha256='54b7f456341b89eeb3930e786837762ea67f235e886512496c4152ebe106d4af')
    version('5.13.0', sha256='0cdbffe5135926527b61cc3692dd301cd0328dd87eeaf1313e610787c46faff9')
    version('5.12.3', sha256='0db0fa37debab147450f9e052286f7a530404e2aaddc438e97a7dcdf56292110')

    # API files can be installed regardless if Qscintilla is installed or not
    variant('qsci_api', default=False, description='Install PyQt API file for QScintilla')

    # Without opengl support, I got the following error:
    # sip: QOpenGLFramebufferObject is undefined
    depends_on('qt@5:+opengl')
    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-enum34', type=('build', 'run'), when='^python@:3.3')
    depends_on('py-sip module=PyQt5.sip', type=('build', 'run'))
    depends_on('py-sip@:4.19.18 module=PyQt5.sip', type=('build', 'run'), when='@:5.13.0')

    # https://www.riverbankcomputing.com/static/Docs/PyQt5/installation.html
    def configure_args(self):
        args = [
            '--pyuic5-interpreter', self.spec['python'].command.path,
            '--sipdir', self.prefix.share.sip.PyQt5,
            '--stubsdir', join_path(
                self.prefix,
                self.spec['python'].package.site_packages_dir,
                'PyQt5'),
        ]
        if '+qsci_api' in self.spec:
            args.extend(['--qsci-api',
                         '--qsci-api-destdir', self.prefix.share.qsci])
        return args
