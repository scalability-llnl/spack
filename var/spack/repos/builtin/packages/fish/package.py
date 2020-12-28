# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Fish(CMakePackage):
    """fish is a smart and user-friendly command line shell for OS X, Linux, and
    the rest of the family.
    """

    homepage = "https://fishshell.com/"
    url      = "https://github.com/fish-shell/fish-shell/releases/download/3.1.2/fish-3.1.2.tar.gz"
    git      = "https://github.com/fish-shell/fish-shell.git"
    list_url = homepage

    version('master', branch='master')
    version('3.1.2', sha256='d5b927203b5ca95da16f514969e2a91a537b2f75bec9b21a584c4cd1c7aa74ed')
    version('3.1.0', sha256='e5db1e6839685c56f172e1000c138e290add4aa521f187df4cd79d4eab294368')
    version('3.0.0', sha256='ea9dd3614bb0346829ce7319437c6a93e3e1dfde3b7f6a469b543b0d2c68f2cf')

    variant('docs', default=False, description='Build documentation')

    # https://github.com/fish-shell/fish-shell#dependencies-1
    depends_on('cmake@3.2:', type='build')
    depends_on('ncurses')
    depends_on('pcre2@10.21:')
    depends_on('gettext')
    depends_on('py-sphinx', when='+docs', type='build')
    depends_on('python@3.3:', type='test')
    depends_on('py-pexpect', type='test')

    # https://github.com/fish-shell/fish-shell/issues/7310
    patch('codesign.patch', when='@3.1.2 platform=darwin')

    executables = ['^fish$']

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'fish, version (\S+)', output)
        return match.group(1) if match else None

    def setup_build_environment(self, env):
        env.append_flags('LDFLAGS', self.spec['ncurses'].libs.link_flags)

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS=ON',
            '-DMAC_CODESIGN_ID=OFF',
            '-DPCRE2_LIB=' + self.spec['pcre2'].libs[0],
            '-DPCRE2_INCLUDE_DIR=' + self.spec['pcre2'].headers.directories[0],
        ]

        if '+docs' in self.spec:
            args.append('-DBUILD_DOCS=ON')
        else:
            args.append('-DBUILD_DOCS=OFF')

        return args
