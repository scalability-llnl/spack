# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIpywidgets(PythonPackage):
    """IPython widgets for the Jupyter Notebook"""

    homepage = "https://github.com/ipython/ipywidgets"
    url      = "https://github.com/ipython/ipywidgets/archive/5.2.2.tar.gz"

    version('7.5.1', sha256='e4253384886aabbaf10966916a2cf9ffa72551bd045d536fa2a379f14b50cec3')
    version('7.4.2', sha256='f156165e8a855ed862fdf48e72700bdcd6956d089a2018c5b36d358255d45b2b')
    version('5.2.2', sha256='d61ab8bb12b90981a3a6010429816d70eaa041e622043207bcb74239b664d4f3')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('py-ipython@4:', type=('build', 'run'))
    depends_on('py-ipython@4:5', type=('build', 'run'), when='^python@:3.2')
    depends_on('py-ipykernel@4.2.2:', type=('build', 'run'))
    depends_on('py-ipykernel@4.5.1:', type=('build', 'run'), when='@6:')
    depends_on('py-traitlets@4.2.1:', type=('build', 'run'))
    depends_on('py-traitlets@4.3.1:', type=('build', 'run'), when='@6:')
    depends_on('py-nbformat@4.2.0:', type=('build', 'run'), when='@6:')
    depends_on('py-widgetsnbextension@1.2.6:1.9', type=('build', 'run'),
               when='@5.2.2')
    depends_on('py-widgetsnbextension@3.4.0:3.4.999', type=('build', 'run'),
               when='@7.4.2')
    depends_on('py-widgetsnbextension@3.5.0:3.5.999', type=('build', 'run'),
               when='@7.5.1')
