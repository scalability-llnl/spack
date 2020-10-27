# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RustBindgen(CargoPackage):
    """bindgen automatically generates Rust FFI bindings to C (and some C++)
    libraries."""

    homepage = "https://rust-lang.github.io/rust-bindgen/"
    crates_io = "bindgen"
    git = "https://github.com/rust-lang/rust-bindgen.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.55.1', sha256='75b13ce559e6433d360c26305643803cb52cfbabbc2b9c47ce04a58493dfb443')

    depends_on('llvm@6.0:', type=('build', 'run'))

    # rust-bindgen has a dependency on libclang - add path
    def setup_build_environment(self, env):
        env.append_flags(
            'LLVM_CONFIG_PATH',
            join_path(self.spec['llvm'].prefix.bin, 'llvm-config'))
