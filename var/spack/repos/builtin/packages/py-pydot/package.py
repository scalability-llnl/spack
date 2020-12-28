# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydot(PythonPackage):
    """Python interface to Graphviz's Dot language"""

    homepage = "https://github.com/erocarrera/pydot/"
    url      = "https://pypi.io/packages/source/p/pydot/pydot-1.2.3.tar.gz"

    version('1.4.1', sha256='d49c9d4dd1913beec2a997f831543c8cbd53e535b1a739e921642fe416235f01')
    version('1.2.3', sha256='edb5d3f249f97fbd9c4bb16959e61bc32ecf40eee1a9f6d27abe8d01c0a73502')
    version('1.2.2', sha256='04a97a885ed418dcc193135cc525fa356cad8b16719293295a149b30718ce400')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyparsing@2.1.4:', type=('build', 'run'))
    depends_on('graphviz', type=('build', 'run'))
