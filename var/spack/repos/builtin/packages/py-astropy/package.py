# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAstropy(PythonPackage):
    """The Astropy Project is a community effort to develop a single core
    package for Astronomy in Python and foster interoperability between
    Python astronomy packages."""

    homepage = 'http://www.astropy.org/'
    url = 'https://pypi.io/packages/source/a/astropy/astropy-3.2.1.tar.gz'

    version('3.2.1', sha256='706c0457789c78285e5464a5a336f5f0b058d646d60f4e5f5ba1f7d5bf424b28')
    version('2.0.14', sha256='618807068609a4d8aeb403a07624e9984f566adc0dc0f5d6b477c3658f31aeb6')
    version('1.1.2', sha256='6f0d84cd7dfb304bb437dda666406a1d42208c16204043bc920308ff8ffdfad1')
    version('1.1.post1', sha256='64427ec132620aeb038e4d8df94d6c30df4cc8b1c42a6d8c5b09907a31566a21')

    variant('extras', default=False, description='Enable extra functionality')

    # Required dependencies
    depends_on('python@3.6:', when='@4.0:', type=('build', 'run'))
    depends_on('python@3.5:', when='@3.0:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@2.0:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.3:', when='@1.2:', type=('build', 'run'))
    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.13:', when='@3.1:', type=('build', 'run'))
    depends_on('py-numpy@1.10:', when='@3.0:', type=('build', 'run'))
    depends_on('py-numpy@1.9:', when='@2.0:', type=('build', 'run'))
    depends_on('py-numpy@1.7:', when='@1.2:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))

    # Optional dependencies
    depends_on('py-scipy', when='+extras', type=('build', 'run'))
    depends_on('py-h5py', when='+extras', type=('build', 'run'))
    depends_on('py-beautifulsoup4', when='+extras', type=('build', 'run'))
    depends_on('py-html5lib', when='+extras', type=('build', 'run'))
    depends_on('py-bleach', when='+extras', type=('build', 'run'))
    depends_on('py-pyyaml', when='+extras', type=('build', 'run'))
    depends_on('py-pandas', when='+extras', type=('build', 'run'))
    depends_on('py-bintrees', when='+extras', type=('build', 'run'))
    depends_on('py-sortedcontainers', when='+extras', type=('build', 'run'))
    depends_on('py-pytz', when='+extras', type=('build', 'run'))
    depends_on('py-jplephem', when='+extras', type=('build', 'run'))
    depends_on('py-matplotlib@2.0:', when='+extras', type=('build', 'run'))
    depends_on('py-scikit-image', when='+extras', type=('build', 'run'))
    depends_on('py-mpmath', when='+extras', type=('build', 'run'))
    depends_on('py-asdf@2.3:', when='+extras', type=('build', 'run'))
    depends_on('py-bottleneck', when='+extras', type=('build', 'run'))
    depends_on('py-pytest', when='+extras', type=('build', 'run'))

    # System dependencies
    depends_on('erfa')
    depends_on('wcslib')
    depends_on('cfitsio')
    depends_on('expat')

    def build_args(self, spec, prefix):
        args = [
            '--use-system-libraries',
            '--use-system-erfa',
            '--use-system-wcslib',
            '--use-system-cfitsio',
            '--use-system-expat'
        ]

        if 'wcslib' in spec:
            args.extend(['--with-wcslib={0}'.format(
                        spec['wcslib'].headers.directories[0]),])

        if spec.satisfies('^python@3:'):
            args.extend(['-j', str(make_jobs)])

        return args

    @property
    def headers(self):
        hdrs = find_headers('wcslib',self.prefix.include, recursive=False)
        if not hdrs:
            hdrs = find_headers('wcslib',self.prefix, recursive=True)
        if not hdrs:
            hdrs = find_headers('wcslib',join_path(self.prefix.include, 'wcslib'),
                                recursive=True)
        return hdrs or None
