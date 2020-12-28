# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class RustBindgen(Package):
    """The rust programming language toolchain"""
    homepage = "http://www.rust-lang.org"
    url = "https://github.com/servo/rust-bindgen/archive/v0.20.5.tar.gz"

    version('0.20.5', sha256='4f5236e7979d262c43267afba365612b1008b91b8f81d1efc6a8a2199d52bb37')

    extends("rust")
    depends_on("llvm")

    def install(self, spec, prefix):
        env = dict(os.environ)
        env['LIBCLANG_PATH'] = os.path.join(spec['llvm'].prefix, 'lib')
        cargo('install', '--root', prefix, env=env)
