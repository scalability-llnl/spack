# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import shutil
import re


class Ghostscript(AutotoolsPackage):
    """An interpreter for the PostScript language and for PDF."""

    homepage = "http://ghostscript.com/"
    url = "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs926/ghostscript-9.26.tar.gz"

    executables = [r'^gs$']

    version('9.54.0', sha256='0646bb97f6f4d10a763f4919c54fa28b4fbdd3dff8e7de3410431c81762cade0')
    version('9.53.3', sha256='6eaf422f26a81854a230b80fd18aaef7e8d94d661485bd2e97e695b9dce7bf7f')
    version('9.50', sha256='0f53e89fd647815828fc5171613e860e8535b68f7afbc91bf89aee886769ce89')
    version('9.27', sha256='9760e8bdd07a08dbd445188a6557cb70e60ccb6a5601f7dbfba0d225e28ce285')
    version('9.26', sha256='831fc019bd477f7cc2d481dc5395ebfa4a593a95eb2fe1eb231a97e450d7540d')
    version('9.21', sha256='02bceadbc4dddeb6f2eec9c8b1623d945d355ca11b8b4df035332b217d58ce85')
    version('9.18', sha256='5fc93079749a250be5404c465943850e3ed5ffbc0d5c07e10c7c5ee8afbbdb1b')

    depends_on('pkgconfig', type='build')
    depends_on('krb5', type='link')

    depends_on('freetype@2.4.2:')
    depends_on('jpeg')
    depends_on('lcms')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('zlib')
    depends_on('libxext')
    depends_on('gtkplus')

    patch('nogoto.patch', when='%fj@:4.1.0')

    # Related bug report: https://bugs.ghostscript.com/show_bug.cgi?id=702985
    # Patch source: https://git.ghostscript.com/?p=ghostpdl.git;a=commitdiff;h=41ef9a0bc36b
    patch("https://git.ghostscript.com/?p=ghostpdl.git;a=commitdiff_plain;h=41ef9a0bc36b",
          when='@:9.53.3^freetype@2.10.3:',
          sha256="254532a8561afddb5b39c1c30526676559ed9f0b87c1e9985eb797a59c98a3dd")

    def url_for_version(self, version):
        baseurl = "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs{0}/ghostscript-{1}.tar.gz"
        return baseurl.format(version.joined, version.dotted)

    def patch(self):
        """Ghostscript comes with all of its dependencies vendored.
        In order to build with Spack versions of these dependencies,
        we have to remove these vendored dependencies.

        Note that this approach is also recommended by Linux from Scratch:
        http://www.linuxfromscratch.org/blfs/view/svn/pst/gs.html
        """
        directories = ['freetype', 'jpeg', 'libpng', 'zlib']
        if self.spec.satisfies('@:9.21'):
            directories.append('lcms2')
        else:
            directories.append('lcms2mt')
        for directory in directories:
            shutil.rmtree(directory)

        filter_file('ZLIBDIR=src',
                    'ZLIBDIR={0}'.format(self.spec['zlib'].prefix.include),
                    'configure.ac', 'configure',
                    string=True)

    def configure_args(self):
        return [
            '--disable-compile-inits',
            '--enable-dynamic',
            '--with-system-libtiff',
        ]

    def build(self, spec, prefix):
        make()
        make('so')

    def install(self, spec, prefix):
        make('install')
        make('soinstall')

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--help', output=str, error=str)
        match = re.search(r'GPL Ghostscript (\S+)', output)
        return match.group(1) if match else None
