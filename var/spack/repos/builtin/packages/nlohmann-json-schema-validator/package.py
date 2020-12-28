# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NlohmannJsonSchemaValidator(CMakePackage):
    """JSON schema validator for JSON for Modern C++"""

    homepage = "https://github.com/pboettch/json-schema-validator"
    url      = "https://github.com/pboettch/json-schema-validator/archive/2.1.0.tar.gz"
    git      = "https://github.com/pboettch/json-schema-validator.git"

    version('master', branch='master')
    version('2.1.0', sha256='83f61d8112f485e0d3f1e72d51610ba3924b179926a8376aef3c038770faf202')
    version('2.0.0', sha256='ca8e4ca5a88c49ea52b5f5c2a08a293dbf02b2fc66cb8c09d4cce5810ee98b57')
    version('1.0.0', sha256='4bdcbf6ce98eda993d8a928dbe97a03f46643395cb872af875a908156596cc4b')

    depends_on('cmake@3.2:', type='build')
    depends_on('nlohmann-json')

    def cmake_args(self):
        args = ['-DBUILD_SHARED_LIBS:BOOL=ON']
        return args
