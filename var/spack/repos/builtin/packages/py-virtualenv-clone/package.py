# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVirtualenvClone(PythonPackage):
    """A script for cloning a non-relocatable virtualenv."""

    homepage = "https://github.com/edwardgeorge/virtualenv-clone"
    url      = "https://pypi.io/packages/source/v/virtualenv-clone/virtualenv-clone-0.2.6.tar.gz"

    version('0.2.6', sha256='6b3be5cab59e455f08c9eda573d23006b7d6fb41fae974ddaa2b275c93cc4405')

    depends_on('python@2.6:')
    # not just build-time, requires pkg_resources
    depends_on('py-setuptools', type=('build', 'run'))
