# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Snakemake(PythonPackage):
    """Snakemake is an MIT-licensed workflow management system."""

    homepage = "https://snakemake.readthedocs.io/en/stable/"
    pypi = "snakemake/snakemake-6.12.3.tar.gz"
    maintainers = ['marcusboden']

    version('7.2.0', sha256='ccb4cb8e28d9248d1c2689a68a667ad8855bbe93571abc3c8f56570db091bc27')
    version('7.0.2', sha256='d988ea1914203452dc93200c0d54f283f806b109934534cc4448f9359fa185c8')
    version('6.15.5', sha256='e3297898f96c358b2c1a883aeb0f3540f983943cd564511510b9112a37fcf1f4')
    version('6.15.1', sha256='a219601d57037f565ead9963e6bd8d04d3bdd985d172371e54197dcbdba79865')
    version('6.13.1', sha256='22f57dcd8b1ca8a30aaa45c5d2c0f56d381d4731abd0988f24f9de46b7d9827c')
    version('6.12.3', sha256='af86af9a540da3dceb05dad1040f1d3d733e6a695f8b3f8c30f8cf3bc6570a88')
    version('3.11.2', sha256='f7a3b586bc2195f2dce4a4817b7ec828b6d2a0cff74a04e0f7566dcd923f9761', deprecated=True)

    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-wrapt', type=('build', 'run'))

    depends_on('python@3.3:3.6', when='@:5', type=('build', 'run'))

    with when('@7:'):
        depends_on('python@3.7:', type=('build', 'run'))
        depends_on('py-yte@1', type=('build', 'run'))
        depends_on('py-jinja2@3', type=('build', 'run'))
        depends_on('py-retry', type=('build', 'run'))

    with when('@6:'):
        depends_on('python@3.5:', type=('build', 'run'))
        depends_on('py-pyyaml', type=('build', 'run'))
        depends_on('py-configargparse', type=('build', 'run'))
        depends_on('py-appdirs', type=('build', 'run'))
        depends_on('py-datrie', type=('build', 'run'))
        depends_on('py-jsonschema', type=('build', 'run'))
        depends_on('py-docutils', type=('build', 'run'))
        depends_on('py-gitpython', type=('build', 'run'))
        depends_on('py-psutil', type=('build', 'run'))
        depends_on('py-nbformat', type=('build', 'run'))
        depends_on('py-toposort', type=('build', 'run'))
        depends_on('py-connectionpool@0.0.3:', type=('build', 'run'))
        depends_on('py-pulp@2.0:', type=('build', 'run'))
        depends_on('py-smart-open@3.0:', type=('build', 'run'))
        depends_on('py-filelock', type=('build', 'run'))
        depends_on('py-stopit', type=('build', 'run'))
        depends_on('py-tabulate', type=('build', 'run'))
        depends_on('py-ratelimiter', type=('build', 'run'))

        variant('reports', default=False, description='Generate self-contained HTML reports')
        with when('+reports'):
            depends_on('py-jinja2', type=('build', 'run'))
            depends_on('py-networkx', type=('build', 'run'))
            depends_on('py-pygments', type=('build', 'run'))
            depends_on('py-pygraphviz', type=('build', 'run'))

        variant('google-cloud', default=False, description='Enable Google Cloud execution')
        with when('+google-cloud'):
            depends_on('py-oauth2client', type=('build', 'run'))
            depends_on('py-google-crc32c', type=('build', 'run'))
            depends_on('py-google-api-python-client', type=('build', 'run'))
            depends_on('py-google-cloud-storage', type=('build', 'run'))
