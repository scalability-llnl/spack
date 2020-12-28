# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyEnvisage(PythonPackage):
    """Envisage is a Python-based framework for building extensible
    applications, that is, applications whose functionality can be extended by
    adding "plug-ins". Envisage provides a standard mechanism for features to
    be added to an application, whether by the original developer or by someone
    else. In fact, when you build an application using Envisage, the entire
    application consists primarily of plug-ins. In this respect, it is similar
    to the Eclipse and Netbeans frameworks for Java applications."""

    homepage = "https://docs.enthought.com/envisage"
    url      = "https://pypi.io/packages/source/e/envisage/envisage-4.9.2.tar.gz"

    version('4.9.2', sha256='ed9580ac6ea17b333f1cce5b94656aed584798d56d8bd364f996a06fe1ac32eb')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-apptools', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-traits', type=('build', 'run'))
