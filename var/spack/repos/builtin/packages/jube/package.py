# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jube(PythonPackage):
    """The Juelich benchmarking environment (JUBE) provides a script based
    framework to easily create benchmark sets, run those sets on different
    computer systems and evaluate the results."""

    homepage = "https://www.fz-juelich.de/jsc/jube/"
    url      = "https://apps.fz-juelich.de/jsc/jube/jube2/download.php?version=2.2.2"

    version('2.4.0', sha256='87c02555f3d1a8ecaff139cf8e7a7167cabd1049c8cc77f1bd8f4484e210d524', extension='tar.gz')
    version('2.3.0', sha256='6051d45af2ff35031ccc460185fbfa61f7f36ea14f17a0d51a9e62cd7af3709a', extension="tar.gz")
    version('2.2.2', sha256='135bc03cf07c4624ef2cf581ba5ec52eb44ca1dac15cffb83637e86170980477', extension="tar.gz")
    version('2.2.1', sha256='68751bf2e17766650ccddb7a5321dd1ac8b34ffa3585db392befbe9ff180ddd9', extension="tar.gz")
    version('2.2.0', sha256='bc825884fc8506d0fb7b3b5cbb5ad4c7e82b1fe1d7ec861ca33699adfc8100f1', extension="tar.gz")
    version('2.1.4', sha256='13da3213db834ed2f3a04fedf20a24c4a11b76620e18fed0a0bbcb7484f980bb', extension="tar.gz")
    version('2.1.3', sha256='ccc7af95eb1e3f63c52a26db08ef9986f7cc500df7a51af0c5e14ed4e7431ad6', extension="tar.gz")
    version('2.1.2', sha256='4ff1c4eabaaa71829e46e4fb4092a88675f8c2b6708d5ec2b12f991dd9a4de2d', extension="tar.gz")
    version('2.1.1', sha256='0c48ce4cb9300300d115ae428b1843c4229a54eb286ab0ced953e96ed3f2b9b2', extension="tar.gz")
    version('2.1.0', sha256='eb9c542b9eb760ea834459a09f8be55891e993a40e277d325bc093b040921e23', extension="tar.gz")
    version('2.0.1', sha256='ef3c4de8b2353ec0ee229428b1ef1912bc3019b72d4e78be00eecd1f384aeec0', extension="tar.gz")
    version('2.0.0', sha256='ecfe8717bc61f35f333bc24d27b39e78e67c596e23512bdd97c9b4f28491f0b3', extension="tar.gz")

    variant(
        'resource_manager', default='none',
        description='Select resource manager templates',
        values=('none', 'loadleveler', 'lsf', 'moab', 'pbs', 'slurm'),
        multi=False
    )

    depends_on('py-setuptools', type='build')

    def setup_run_environment(self, env):
        if not self.spec.variants['resource_manager'].value == 'none':
            env.prepend_path('JUBE_INCLUDE_PATH', join_path(
                self.prefix.platform,
                self.spec.variants['resource_manager'].value))
