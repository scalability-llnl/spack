# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util import tty
from spack.package import *


class Mercurial(PythonPackage):
    """Mercurial is a free, distributed source control management tool."""

    homepage = "https://www.mercurial-scm.org"
    url      = "https://www.mercurial-scm.org/release/mercurial-5.3.tar.gz"

    version('5.3',   sha256='e57ff61d6b67695149dd451922b40aa455ab02e01711806a131a1e95c544f9b9')
    version('5.1.2', sha256='15af0b090b23649e0e53621a88dde97b55a734d7cb08b77d3df284db70d44e2e')
    version('5.1.1', sha256='35fc8ba5e0379c1b3affa2757e83fb0509e8ac314cbd9f1fd133cf265d16e49f')
    version('4.9.1', sha256='1bdd21bb87d1e05fb5cd395d488d0e0cc2f2f90ce0fd248e31a03595da5ccb47')
    version('4.4.1', sha256='8f2a5512d6cc2ffb08988aef639330a2f0378e4ac3ee0e1fbbdb64d9fff56246')
    version('4.1.2', sha256='09415253fb409a77e19b9951532a3c22c4e07e74bab80652527064617daab194')
    version('3.9.1', sha256='625e4fc7e85ec2278c2828bdc547fce74091b3bbe4d9eeeba2d61af51195df74')
    version('3.9',   sha256='834f25dcff44994198fb8a7ba161a6e24204dbd63c8e6270577e06e6cedbdabc')
    version('3.8.4', sha256='4b2e3ef19d34fa1d781cb7425506a05d4b6b1172bab69d6ea78874175fdf3da6')
    version('3.8.3', sha256='f84556cdf9a331984261549d9d08143ab9da33d7c03f0aa323b0ee52d0782a4c')
    version('3.8.2', sha256='cb78b16956140625266a8a6d1fadc7c868969d994086e1ec60279a66bf20bffd')
    version('3.8.1', sha256='face1f058de5530b56b0dfd3b4d0b23d89590c588605c06f3d18b79e8c30d594')

    depends_on('python@2.6:2.8', when='@:4.2.99', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5.3:3.5.999,3.6.2:', when='@4.3:', type=('build', 'run'))
    depends_on('py-setuptools', when='@3.6:', type='build')
    depends_on('py-docutils', type='build')
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-certifi',  type=('build', 'run'))

    def setup_build_environment(self, env):
        # Python 3 support is still experimental, explicitly allow
        env.set('HGALLOWPYTHON3', True)
        env.set('HGPYTHON3', True)
        # Setuptools is still opt-in, explicitly enable
        env.set('FORCE_SETUPTOOLS', True)

    @run_after('install')
    def post_install(self):
        prefix = self.prefix

        # Install man pages
        mkdirp(prefix.man.man1)
        mkdirp(prefix.man.man5)
        mkdirp(prefix.man.man8)
        with working_dir('doc'):
            install('hg.1', prefix.man.man1)
            install('hgignore.5', prefix.man.man5)
            install('hgrc.5', prefix.man.man5)
            install('hg-ssh.8', prefix.man.man8)

        # Install completion scripts
        contrib = prefix.contrib
        mkdir(contrib)
        with working_dir('contrib'):
            install('bash_completion', contrib.bash_completion)
            install('zsh_completion',  contrib.zsh_completion)

    @run_after('install')
    def configure_certificates(self):
        """Configuration of HTTPS certificate authorities
        https://www.mercurial-scm.org/wiki/CACertificates"""

        etc_dir = self.prefix.etc.mercurial
        mkdirp(etc_dir)

        hgrc_filename = etc_dir.hgrc

        # Use certifi to find the location of the CA certificate
        print_str = self.spec['python'].package.print_string('certifi.where()')
        certificate = python('-c', 'import certifi; ' + print_str, output=str)

        if not certificate:
            tty.warn('CA certificate not found. You may not be able to '
                     'connect to an HTTPS server. If your CA certificate '
                     'is in a non-standard location, you should add it to '
                     '{0}.'.format(hgrc_filename))
        else:
            # Write the global mercurial configuration file
            with open(hgrc_filename, 'w') as hgrc:
                hgrc.write('[web]\ncacerts = {0}'.format(certificate))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """Sanity-check setup."""

        hg = Executable(self.prefix.bin.hg)

        hg('debuginstall')
        hg('version')
