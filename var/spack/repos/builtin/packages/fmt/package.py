# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fmt(CMakePackage):
    """fmt (formerly cppformat) is an open-source formatting library.
    It can be used as a safe alternative to printf or as a fast alternative
    to C++ IOStreams."""

    homepage = "http://fmtlib.net/latest/index.html"
    url      = "https://github.com/fmtlib/fmt/releases/download/7.1.0/fmt-7.1.0.zip"

    version('7.1.0', sha256='308af4e36ee3ab527b51014a2a5d862682c84f5d16f7a597aea34c84853cbcb0')
    version('6.1.2', sha256='63650f3c39a96371f5810c4e41d6f9b0bb10305064e6faf201cbafe297ea30e8')
    version('5.3.0', sha256='4c0741e10183f75d7d6f730b8708a99b329b2f942dad5a9da3385ab92bb4a15c')
    version('5.2.1', sha256='43894ab8fe561fc9e523a8024efc23018431fa86b95d45b06dbe6ddb29ffb6cd')
    version('5.2.0', sha256='c016db7f825bce487a7929e1edb747b9902a2935057af6512cad3df3a080a027')
    version('5.1.0', sha256='77ef9fea638dc846e484409fbc1ea710bb9bcea042e7b35b8805041bf7655ad5')
    version('5.0.0', sha256='8dd58daf13e7e8adca99f8725ef3ae598f9c97efda7d6d8d4c49db5047879097')
    version('4.1.0', sha256='9d49bf02ceb9d0eec51144b203b63b77e69d3798bb402fb82e7d0bdb06c79eeb')
    version('4.0.0', sha256='10a9f184d4d66f135093a08396d3b0a0ebe8d97b79f8b3ddb8559f75fe4fcbc3')
    version('3.0.2', sha256='51407b62a202b29d1a9c0eb5ecd4095d30031aea65407c42c25cb10cb5c59ad4')
    version('3.0.1', sha256='4c9af0dc919a8ae7022b44e1a03c435e42d65c866f44667d8d920d342b098550')
    version('3.0.0', sha256='1b050b66fa31b74f1d75a14f15e99e728ab79572f176a53b2f8ad7c201c30ceb')

    variant('cxxstd',
            default='11',
            values=('98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building')
    variant('pic', default=True, description='Enable generation of position-independent code')

    depends_on('cmake@3.1.0:', type='build')

    # Supported compilers/standards are detailed here:
    # http://fmtlib.net/latest/index.html#portability
    conflicts('%gcc@:4.3.999', when='@5:')
    conflicts('%llvm@:2.8.999', when='@5:')
    # 5 and above require C++11
    conflicts('cxxstd=98', when='@5:')
    # 5.0.0 enables C++14 auto return types in C++11 mode
    conflicts('cxxstd=11', when='@5.0.0')
    # 4.1 fails with C++17 (https://github.com/fmtlib/fmt/issues/722)
    conflicts('cxxstd=17', when='@4.1.0')

    # Use CMAKE_CXX_STANDARD to define C++ flag, as in later versions
    patch('fmt-use-cmake-cxx-standard_3.0.0.patch', when='@3.0.0')

    # Remove hardcoding of "-std=c++11/0x" in INTERFACE_COMPILE_OPTIONS
    patch('fmt-no-export-cpp11flag_3.0.0.patch', when='@3.0.0:3.0.1')

    # Only allow [[attributes]] on C++11 and higher
    patch('fmt-attributes-cpp11_4.1.0.patch', when='@4.1.0')

    def cmake_args(self):
        spec = self.spec
        args = []

        if '+pic' in spec:
            args.extend([
                '-DCMAKE_C_FLAGS={0}'.format(self.compiler.cc_pic_flag),
                '-DCMAKE_CXX_FLAGS={0}'.format(self.compiler.cxx_pic_flag)
            ])

        args.append('-DCMAKE_CXX_STANDARD={0}'.format(
                    spec.variants['cxxstd'].value))
        # Require standard at configure time to guarantee the
        # compiler supports the selected standard.
        args.append('-DCMAKE_CXX_STANDARD_REQUIRED=ON')

        # When cxxstd is 98, must disable FMT_USE_CPP11
        if 'cxxstd=98' in spec:
            args.append('-DFMT_USE_CPP11=OFF')

        # Can't build docs without doxygen+python+virtualenv
        # and call to build "doc" target
        args.append("-DFMT_DOC=OFF")

        return args
