# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyGemini(PythonPackage):
    """GEMINI (GEnome MINIng) is a flexible framework for exploring genetic
    variation in the context of the wealth of genome annotations available
    for the human genome.
    """

    homepage = "https://gemini.readthedocs.org"
    url      = "https://github.com/arq5x/gemini/archive/v0.30.2.tar.gz"

    maintainers = ['robqiao']

    version('0.30.2', sha256='c7af06a4cc475a846aeeb3cd7fcfb39d6cdd0b76e3b07abab2e5e6e68a3fe431')
    version('0.30.1', sha256='af835ca33bc6d7865def2467c34cb1d539ec542f9514044435bd2252b25a046d')
    version('0.30.0', sha256='a55d0c77342bf650f7e1300cb6ba485407ea3b42f4137a5197248d397a026030')
    version('0.20.1', sha256='cd84aa45ace7a9ffb13ba4176122eab5b9fcc0445b1c0944ecec017f88f2b7f1')
    version('0.20.0', sha256='640b40186fa00f54c1a0cdfab3fc3076b1d3bdf5c6327fcb2a0c51aa1b05878b')
    version('0.19.1', sha256='1154bcb48b1bc78819c5a5e710f5cb0747b01fa0f3113e6081a5a2747c8703e5')
    version('0.19.0', sha256='5146d1b5ed52139c50473aa3625d8df29f2db6d198cfd2c966469e7d585cccf2')
    version('0.18.3', sha256='7c2f99069385547c656021fbb43e0bae4f9fb8a56ad3f6a61235b44fbc1ba6eb')
    version('0.18.2', sha256='cf8a83d48d966a800aa2569076d52c307f4d8264a6ae804c176d61e705c0017e')
    version('0.18.1', sha256='1d3d3b9d47555e1f62c1a870d8fd2ecbfc0bed25910cab31af5b585db3144a68')

    depends_on('python@2.5:2.8', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('tabix', type=('build', 'run'))
    depends_on('grabix', type=('build', 'run'))
    depends_on('bedtools2', type=('build', 'run'))

    depends_on('py-numpy@1.7.1:', type=('build', 'run'))
    depends_on('py-inheritance@0.1.3:', type=('build', 'run'))
    depends_on('py-geneimpacts@0.1.3:', type=('build', 'run'))
    depends_on('py-cython@0.22.1:', type=('build', 'run'))
    depends_on('py-sqlalchemy@1:', type=('build', 'run'))
    depends_on('py-pysam@0.6:', type=('build', 'run'))
    depends_on('py-cyvcf2@0.7.2:', type=('build', 'run'))
    depends_on('py-pyyaml@3.10:', type=('build', 'run'))
    depends_on('py-pybedtools@0.6.2:', type=('build', 'run'))
    depends_on('py-jinja2@2.7.1:', type=('build', 'run'))
    depends_on('py-networkx@1.10:', type=('build', 'run'))
    depends_on('py-bottle@0.11.6:', type=('build', 'run'))
    depends_on('py-ipyparallel@4.0:', type=('build', 'run'))
    depends_on('py-ipython-cluster-helper@0.5.1:', type=('build', 'run'))
    depends_on('py-bx-python@0.7.1:', type=('build', 'run'))
    depends_on('py-pandas@0.11.0:', type=('build', 'run'))
    depends_on('py-openpyxl@1.6.1:1.999', type=('build', 'run'))
    depends_on('py-scipy@0.12.0:', type=('build', 'run'))
    depends_on('py-unidecode@0.04.14:', type=('build', 'run'))
    depends_on('py-cyordereddict@0.2.2', type=('build', 'run'))
    depends_on('py-bcolz@0.11.3:', type=('build', 'run'))
    depends_on('py-numexpr@2.4.3:', type=('build', 'run'))
