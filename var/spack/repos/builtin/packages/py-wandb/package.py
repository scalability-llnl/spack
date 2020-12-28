# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWandb(PythonPackage):
    """A tool for visualizing and tracking your machine
       learning experiments."""

    homepage = "https://github.com/wandb/"
    url      = "https://github.com/wandb/client/archive/v0.10.1.tar.gz"

    version('0.10.1', sha256='abd334cd1460ac1f6e5aa959d3e04c46cd246f96cfc3323fc0572916760d32ab')

    depends_on('py-setuptools', type='build')
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-gitpython', type=('build', 'run'))
    depends_on('py-gql', type=('build', 'run'))
    depends_on('py-nvidia-ml-py3', type=('build', 'run'))
    depends_on('py-python-dateutil', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-shortuuid', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-watchdog', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-psutil', type=('build', 'run'))
    depends_on('py-sentry-sdk', type=('build', 'run'))
    depends_on('py-subprocess32', type=('build', 'run'))
    depends_on('py-dockerpy-creds', type=('build', 'run'))
    depends_on('py-configparser', type=('build', 'run'))
