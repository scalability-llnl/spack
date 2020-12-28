# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAbipy(PythonPackage):
    """Python package to automate ABINIT calculations and analyze
    the results."""

    homepage = "https://github.com/abinit/abipy"
    url      = "https://pypi.io/packages/source/a/abipy/abipy-0.2.0.tar.gz"

    version('0.2.0', sha256='c72b796ba0f9ea4299eac3085bede092d2652e9e5e8074d3badd19ef7b600792')

    variant('gui',     default=False, description='Build the GUI')
    variant('ipython', default=False, description='Build IPython support')

    extends('python', ignore='bin/(feff_.*|gaussian_analyzer|get_environment|html2text|nc3tonc4|nc4tonc3|ncinfo|pmg|pydii|tabulate|tqdm)')

    depends_on('python@2.7:')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython',     type='build')

    depends_on('py-six',                 type=('build', 'run'))
    depends_on('py-prettytable',         type=('build', 'run'))
    depends_on('py-tabulate',            type=('build', 'run'))
    depends_on('py-apscheduler@2.1.0',   type=('build', 'run'))
    depends_on('py-pydispatcher@2.0.5:', type=('build', 'run'))
    depends_on('py-tqdm',                type=('build', 'run'))
    depends_on('py-html2text',           type=('build', 'run'))
    depends_on('py-pyyaml@3.11:',        type=('build', 'run'))
    depends_on('py-pandas',              type=('build', 'run'))
    depends_on('py-numpy@1.9:',          type=('build', 'run'))
    depends_on('py-scipy@0.14:',         type=('build', 'run'))
    depends_on('py-spglib',              type=('build', 'run'))
    depends_on('py-pymatgen@4.7.2:',     type=('build', 'run'))
    depends_on('py-netcdf4',             type=('build', 'run'))
    depends_on('py-matplotlib@1.5:',     type=('build', 'run'))
    depends_on('py-seaborn',             type=('build', 'run'))

    depends_on('py-wxpython', type=('build', 'run'), when='+gui')
    depends_on('py-wxmplot',  type=('build', 'run'), when='+gui')

    depends_on('py-ipython',  type=('build', 'run'), when='+ipython')
    depends_on('py-jupyter',  type=('build', 'run'), when='+ipython')
    depends_on('py-nbformat', type=('build', 'run'), when='+ipython')

    def build_args(self, spec, prefix):
        args = []

        if '+ipython' in spec:
            args.append('--with-ipython')

        return args
