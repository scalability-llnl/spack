# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class VotcaTools(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
       Applications (VOTCA) is a package intended to reduce the amount of
       routine work when doing systematic coarse-graining of various
       systems. The core is written in C++.

       This package contains the basic tools library of VOTCA.
    """
    homepage = "http://www.votca.org"
    url      = "https://github.com/votca/tools/tarball/v1.4"
    git      = "https://github.com/votca/tools.git"
    maintainers = ['junghans']

    version('master', branch='master')
    version('stable', branch='stable')
    version('2021', sha256='b84f68ba4a8bfae7b06b61e1e078dcbfb3b340c516da3be39ef545152da00ccd')
    version('1.6.4', sha256='aa79ef4617a80ba3ca063932d5ee0d5767c0285b4b613abd373ad3c986ab9f4c')
    version('1.6.3', sha256='b4ba63861f4342070d81309992f76c4cc798dffeab894bff64799881e75b3cc2')
    version('1.6.2', sha256='1b31e0dd7550b80b963e6714d671f3516d68ebc1e75068a5d827a6e8b4f1759a')
    version('1.6.1', sha256='3e8f51d484cb3fdfbeb851aab387807ba4c40aecef8317c90182da68ad282dcc')
    version('1.6', sha256='cfd0fedc80fecd009f743b5df47777508d76bf3ef294a508a9f11fbb42efe9a5')
    version('1.5.1', sha256='4be4fe25a2910e24e1720cd9022d214001d38196033ade8f9d6e618b4f47d5c4')
    version('1.5', sha256='a82a6596c24ff06e79eab17ca02f4405745ceeeb66369693a59023ad0b62cf22')
    version('1.4.1', sha256='b6b87f6bec8db641a1d8660422ca44919252a69494b32ba6c8c9ac986bae9a65')
    version('1.4', sha256='41638122e7e59852af61d391b4ab8c308fd2e16652f768077e13a99d206ec5d3')

    # https://github.com/votca/tools/pull/229, fix mkl in exported target
    patch("https://github.com/votca/tools/pull/229.patch", sha256="250d0b679e5d3104e3c8d6adf99751b71386c7ed4cbdae1c75408717ef3f401f", when="@1.6:1.6.0+mkl")

    variant('mkl', default=False, description='Build with MKL support')
    conflicts('+mkl', when='@1.4:1.5.9999')

    depends_on("cmake@2.8:", type='build')
    depends_on("expat")
    depends_on("fftw-api@3")
    depends_on("gsl", when="@1.4:1.4.9999")
    depends_on("eigen@3.3:", when="@stable,1.5:")
    depends_on("boost")
    depends_on("sqlite", when="@1.4:1.5.9999")
    depends_on('mkl', when='+mkl')

    def cmake_args(self):
        args = [
            '-DWITH_RC_FILES=OFF'
        ]

        if '~mkl' in self.spec:
            args.append('-DCMAKE_DISABLE_FIND_PACKAGE_MKL=ON')

        return args
