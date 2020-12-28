# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClustershell(PythonPackage):
    """Scalable cluster administration Python framework - Manage node sets
    node groups and execute commands on cluster nodes in parallel.
    """

    homepage = "http://cea-hpc.github.io/clustershell/"
    url      = "https://github.com/cea-hpc/clustershell/archive/v1.8.tar.gz"

    version('1.8', sha256='ad5a13e2d107b4095229810c35365e22ea94dfd2baf4fdcfcc68ce58ee37cee3')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyyaml')
