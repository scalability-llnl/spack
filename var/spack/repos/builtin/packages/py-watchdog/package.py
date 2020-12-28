# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWatchdog(PythonPackage):
    """Python library and shell utilities to monitor filesystem events."""

    homepage = "https://github.com/gorakhargosh/watchdog"
    url      = "https://github.com/gorakhargosh/watchdog/archive/v0.10.3.tar.gz"

    version('0.10.3', sha256='f7e5040b483cc9a8618a4e72c11a527b42434a0766ea96dce633e8b44b1369de')
    version('0.10.2', sha256='4dba861f5e6960c8063ad68137772ff35f1516ea47d64b53042dabd2d8f8dbdc')
    version('0.10.1', sha256='972c6050eb5d275b582c75e6ff71ef562a6c3be6361d6d9b37110e0ba718994d')
    version('0.10.0', sha256='39e2966b8c9596e45b463815668989b87c7d205e47c7e6e4a7db9a58354b99ff')
    version('0.9.0',  sha256='e8a32701dff43a4e671a40acf92f55a8fffd8ca74333b75436d63a94d104faef')
    version('0.8.3',  sha256='e9a27d0ab121fc86217ab833e778c76880aad4ecdb623796f4b7aee9925394ed')
    version('0.8.2',  sha256='386e882c8bc7df8a3c4c8803e6fcf2f7cf836c9a8867ff9d91b4af19d262d023')
    version('0.8.1',  sha256='05e5d8acd5061aff789359cd8f25a85ba4c848a8feded3fc68f9c57f0b181373')
    version('0.8.0',  sha256='5abac06e63ad8d5b001626a16bfdd1b918637aa8d85cf933e68de2e627b56053')
    version('0.7.1',  sha256='d795fa85ce9252eeb2294a5182c99013433aeb736cc7a1fc9e14e1e2a1a19690')

    depends_on('python@2.7,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pyyaml',       type=('build', 'run'))
