# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


# package has a Makefile, but only to build examples
class Pegtl(CMakePackage):
    """The Parsing Expression Grammar Template Library (PEGTL) is a
        zero-dependency C++11 header-only library for creating parsers
        according to a Parsing Expression Grammar (PEG).
    """

    homepage = "https://github.com/taocpp/PEGTL"
    url      = "https://github.com/taocpp/PEGTL/tarball/2.1.4"
    git      = "https://github.com/taocpp/PEGTL.git"

    version('master', branch='master')
    version('2.8.3', sha256='370afd0fbe6d73c448a33c10fbe4a7254f92077f5a217317d0a32a9231293015')
    version('2.1.4', sha256='d990dccc07b4d9ba548326d11c5c5e34fa88b34fe113cb5377da03dda29f23f2')
    version('2.0.0', sha256='5aae0505077e051cae4d855c38049cc6cf71103a6cc8d0ddef01a576e8a60cc0')

    # Ref: https://github.com/taocpp/PEGTL/blob/master/src/example/pegtl/json_classes.hpp
    patch('change_to_virtual_destructor.patch', when='@:2.4')
