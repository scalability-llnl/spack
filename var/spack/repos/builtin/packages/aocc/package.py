# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Aocc(Package):
    '''
    The AOCC compiler system is a high performance,
    production quality code generation tool.
    The AOCC environment provides various options to developers when
    building and optimizing C, C++, and Fortran applications
    targeting 32-bit and 64-bit Linux platforms.
    The AOCC compiler system offers a high level of advanced optimizations,
    multi-threading and processor support that includes global optimization,
    vectorization, inter-procedural analyses, loop transformations,
    and code generation.
    AMD also provides highly optimized libraries,
    which extract the optimal performance from
    each x86 processor core when utilized.
    The AOCC Compiler Suite simplifies and accelerates development and
    tuning for x86 applications.
    Please install only if you agree to terms and conditions depicted
    under : http://developer.amd.com/wordpress/media/files/AOCC_EULA.pdf
    Example for installation: \'spack install aocc +license-agreed\'
    '''
    family = 'compiler'
    homepage = "https://developer.amd.com/amd-aocc/"

    maintainers = ['amd-toolchain-support']

    version(ver="3.0.0", sha256='4ff269b1693856b9920f57e3c85ce488c8b81123ddc88682a3ff283979362227',
            url='http://developer.amd.com/wordpress/media/files/aocc-compiler-3.0.0.tar')
    version(ver="2.3.0", sha256='9f8a1544a5268a7fb8cd21ac4bdb3f8d1571949d1de5ca48e2d3309928fc3d15',
            url='http://developer.amd.com/wordpress/media/files/aocc-compiler-2.3.0.tar')
    version(ver="2.2.0", sha256='500940ce36c19297dfba3aa56dcef33b6145867a1f34890945172ac2be83b286',
            url='http://developer.amd.com/wordpress/media/files/aocc-compiler-2.2.0.tar')

    # Licensing
    license_required = True
    license_comment = '#'
    license_files = ['AOCC_EULA.pdf']
    license_url = 'http://developer.amd.com/wordpress/media/files/AOCC_EULA.pdf'
    install_example = "spack install aocc +license-agreed"

    depends_on('libxml2')
    depends_on('zlib')
    depends_on('ncurses')
    depends_on('libtool')
    depends_on('texinfo')

    variant('license-agreed', default=False,
            description='Agree to terms and conditions depicted under : {0}'
            .format(license_url))

    @run_before('install')
    def abort_without_license_agreed(self):
        license_url = 'http://developer.amd.com/wordpress/media/files/AOCC_EULA.pdf'
        install_example = "spack install aocc +license-agreed"
        if not self.spec.variants['license-agreed'].value:
            raise InstallError("\n\n\nNOTE:\nUse +license-agreed " +
                               "during installation " +
                               "to accept terms and conditions " +
                               "depicted under following link \n" +
                               " {0}\n".format(license_url) +
                               "Example: \'{0}\' \n".format(install_example))

    def install(self, spec, prefix):
        print("Installing AOCC Compiler ... ")
        install_tree('.', prefix)
