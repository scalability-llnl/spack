# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxslt(AutotoolsPackage):
    """Libxslt is the XSLT C library developed for the GNOME project. XSLT
    itself is a an XML language to define transformation for XML. Libxslt is
    based on libxml2 the XML C library developed for the GNOME project. It also
    implements most of the EXSLT set of processor-portable extensions functions
    and some of Saxon's evaluate and expressions extensions."""

    homepage = "http://www.xmlsoft.org/XSLT/index.html"
    url      = "http://xmlsoft.org/sources/libxslt-1.1.32.tar.gz"

    version('1.1.33', sha256='8e36605144409df979cab43d835002f63988f3dc94d5d3537c12796db90e38c8')
    version('1.1.32', sha256='526ecd0abaf4a7789041622c3950c0e7f2c4c8835471515fd77eec684a355460')
    version('1.1.29', sha256='b5976e3857837e7617b29f2249ebb5eeac34e249208d31f1fbf7a6ba7a4090ce')
    version('1.1.28', sha256='5fc7151a57b89c03d7b825df5a0fae0a8d5f05674c0e7cf2937ecec4d54a028c')
    version('1.1.26', sha256='55dd52b42861f8a02989d701ef716d6280bfa02971e967c285016f99c66e3db1')

    variant('crypto', default=True, description='Build libexslt with crypto support')
    variant('python', default=False, description='Build Python bindings')

    depends_on('pkgconfig@0.9.0:', type='build')
    depends_on('iconv')
    depends_on('libxml2')
    depends_on('libxml2+python', when='+python')
    depends_on('xz')
    depends_on('zlib')
    depends_on('libgcrypt', when='+crypto')

    depends_on('python+shared', when='+python')
    extends('python', when='+python')

    def configure_args(self):
        args = []

        if '+crypto' in self.spec:
            args.append('--with-crypto')
        else:
            args.append('--without-crypto')

        if '+python' in self.spec:
            args.append('--with-python={0}'.format(self.spec['python'].home))
        else:
            args.append('--without-python')

        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def import_module_test(self):
        if '+python' in self.spec:
            with working_dir('spack-test', create=True):
                python('-c', 'import libxslt')
