# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Diamond(CMakePackage):
    """DIAMOND is a sequence aligner for protein and translated DNA searches,
    designed for high performance analysis of big sequence data."""

    homepage = "https://ab.inf.uni-tuebingen.de/software/diamond"
    url      = "https://github.com/bbuchfink/diamond/archive/v0.9.14.tar.gz"

    version('2.0.4', sha256='94e8fe72bdc28b83fd0f2d90c439b58b63b38263aa1a3905582ef68f614ae95d')
    version('0.9.25', sha256='65298f60cf9421dcc7669ce61642611cd9eeffc32f66fd39ebfa25dd64416808')
    version('0.9.23', sha256='0da5cdd5e5b77550ec0eaba2c6c431801cdd10d31606ca12f952b57d3d31db92')
    version('0.9.22', sha256='35e518cfa0ac2fbc57e422d380bdb5123c6335742dd7965b76c34c95f241b729')
    version('0.9.21', sha256='3f10e089c24d24f3066f3a58fa01bf356c4044e0a0bcab081b9bf1a8d946c9b1')
    version('0.9.20', sha256='5cf629baf135f54dc93728e3618ae08c64c1ecb81b3f2d2d48fcfd1c010ed8f0')
    version('0.9.19', sha256='fab783f51af9010666f2b569f438fb38843d0201fe0c0e167db5b70d12459e30')
    version('0.9.14', sha256='de870a7806ac0aa47b97c9b784dd7201e2c8e11a122003bde440d926211b911e')
    version('0.8.38', sha256='582a7932f3aa73b0eac2275dd773818665f0b067b32a79ff5a13b0e3ca375f60')
    version('0.8.26', sha256='00d2be32dad76511a767ab8e917962c0ecc572bc808080be60dec028df45439f')

    depends_on('zlib')

    conflicts('target=aarch64:', when='@:0.9.25')

    # fix error [-Wc++11-narrowing]
    # Ref: https://github.com/bbuchfink/diamond/commit/155e076d662b0e9268e2b00bef6d33d90aede7ff
    patch('fix_narrowing_error.patch', when='@:0.9.25')
