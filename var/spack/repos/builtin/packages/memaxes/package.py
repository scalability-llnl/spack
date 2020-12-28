# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Memaxes(Package):
    """MemAxes is a visualizer for sampled memory trace data."""

    homepage = "https://github.com/llnl/MemAxes"

    version('0.5', sha256='9858f0f675b50e347d0b88545558e5d6b4333347c762b15d399b8d8004d7b68b',
            url='https://github.com/llnl/MemAxes/archive/v0.5.tar.gz')

    depends_on('cmake@2.8.9:', type='build')
    depends_on("qt@5:")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..', *std_cmake_args)
            make()
            make("install")
