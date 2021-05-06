# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Chapel(AutotoolsPackage):
    """Chapel is a modern programming language that is parallel, productive,
       portable, scalable and open-source."""

    homepage = "https://chapel-lang.org/"
    url      = "https://github.com/chapel-lang/chapel/archive/refs/tags/1.24.1.tar.gz"

    version('1.24.1', sha256='9250824b8efa038941bc08314bbdddf6368e0b86a66a0e8c86169a0eb425e536')
    version('1.24.0', sha256='c54882b21f2c79e47156e1bd512b2460a2934e38d5edd081c93cf410a266e536')
    version('1.23.0', sha256='9350261afd9421254c516bcdd899ca5a431c011b79893029625c8d70fa157452')
    version('1.22.1', sha256='dc3afeb2a873059ac6cdc25e2167d9d677f96ce247bf66ec589c577db05fba5b')
    version('1.22.0', sha256='b0a4d25ee38483d172678bec9a28d267d5da04a2fcaa2e8d9d399f88cc8bf170')
    version('1.21.0', sha256='38914b0765836fda0f2ad4dbd0c1ec95ea4cb4bac7238a3f82640239c3c196fa')
    version('1.20.0', sha256='723283f3d6cecb8f7a1c53ec688864c24f299cf960f3ab6b5d7d580c64e662d4')
    version('1.19.0', sha256='702390a9b6b8a5c03ddaad94b92273a153e9bd7801fd735e3e63252ee3527e38')
    version('1.18.0', sha256='5640b9e8206781a06aa71e77d216c6673ad41ef8b5d225100800457f534e4cf4')
