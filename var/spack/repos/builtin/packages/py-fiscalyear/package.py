# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFiscalyear(PythonPackage):
    """fiscalyear is a small, lightweight Python module providing helpful
    utilities for managing the fiscal calendar. It is designed as an extension
    of the built-in datetime and calendar modules, adding the ability to query
    the fiscal year and fiscal quarter of a date or datetime object."""

    homepage = "https://github.com/adamjstewart/fiscalyear"
    url      = "https://pypi.io/packages/source/f/fiscalyear/fiscalyear-0.2.0.tar.gz"
    git      = "https://github.com/adamjstewart/fiscalyear.git"

    maintainers = ['adamjstewart']

    version('master', branch='master')
    version('0.2.0', sha256='f513616aeb03046406c56d7c69cd9e26f6a12963c71c1410cc3d4532a5bfee71')
    version('0.1.0', sha256='3fde4a12eeb72da446beb487e078adf1223a92d130520e589b82d7d1509701a2')

    depends_on('python@2.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
