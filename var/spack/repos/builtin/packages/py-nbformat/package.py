# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyNbformat(PythonPackage):
    """The Jupyter Notebook format"""

    homepage = "https://github.com/jupyter/nbformat"
    url      = "https://pypi.io/packages/source/n/nbformat/nbformat-5.0.7.tar.gz"

    version('5.0.7', sha256='54d4d6354835a936bad7e8182dcd003ca3dc0cedfee5a306090e04854343b340')
    version('4.4.0', sha256='f7494ef0df60766b7cabe0a3651556345a963b74dbc16bc7c18479041170d402')
    version('4.1.0', sha256='dbf6c0ed0cb7c5a7184536368f1dd1ada2d48fd6f016e0f9e9b69236e28c0857')
    version('4.0.1', sha256='5261c957589b9dfcd387c338d59375162ba9ca82c69e378961a1f4e641285db5')
    version('4.0.0', sha256='daf9b990e96863d120aff123361156a316757757b81a8070eb6945e4a9774b2d')

    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('py-traitlets@4.1:', type=('build', 'run'))
    depends_on('py-jsonschema@2.4.0:2.4.999,2.5.1:', type=('build', 'run'))
    depends_on('py-jupyter-core', type=('build', 'run'))
