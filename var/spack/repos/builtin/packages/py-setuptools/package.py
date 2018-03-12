##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class PySetuptools(PythonPackage):
    """A Python utility that aids in the process of downloading, building,
       upgrading, installing, and uninstalling Python packages."""

    homepage = "https://pypi.python.org/pypi/setuptools"
    url      = "https://pypi.io/packages/source/s/setuptools/setuptools-25.2.0.tar.gz"

    import_modules = ['pkg_resources', 'setuptools', 'setuptools.command']

    version('38.5.2', 'b4c7f29c8079bdf2f0f355cdcd999e69',
            url="https://pypi.python.org/packages/e0/02/2b14188e06ddf61e5b462e216b15d893e8472fca28b1b0c5d9272ad7e87c/setuptools-38.5.2.zip")
    version('35.0.2', 'c368b4970d3ad3eab5afe4ef4dbe2437',
            url="https://pypi.io/packages/source/s/setuptools/setuptools-35.0.2.zip")
    version('34.4.1', '5f9b07aeaafd29eac2548fc0b89a4934',
            url="https://pypi.io/packages/source/s/setuptools/setuptools-34.4.1.zip")
    version('34.2.0', '41b630da4ea6cfa5894d9eb3142922be',
            url="https://pypi.io/packages/source/s/setuptools/setuptools-34.2.0.zip")
    version('25.2.0', 'a0dbb65889c46214c691f6c516cf959c')
    version('20.7.0', '5d12b39bf3e75e80fdce54e44b255615')
    version('20.6.7', '45d6110f3ec14924e44c33411db64fe6')
    version('20.5',   'fadc1e1123ddbe31006e5e43e927362b')
    version('19.2',   '78353b1f80375ca5e088f4b4627ffe03')
    version('18.1',   'f72e87f34fbf07f299f6cb46256a0b06')
    version('16.0',   '0ace0b96233516fc5f7c857d086aa3ad')
    version('11.3.1', '01f69212e019a2420c1693fb43593930')

    depends_on('python@2.6:2.8,3.3:')

    # Previously, setuptools vendored all of its dependencies to allow
    # easy bootstrapping. As of version 34.0.0, this is no longer done
    # and the dependencies need to be installed externally.
    depends_on('py-packaging@16.8:', when='@34.0.0:', type=('build', 'run'))
    depends_on('py-six@1.6.0:',      when='@34.0.0:', type=('build', 'run'))
    depends_on('py-appdirs@1.4.0:',  when='@34.0.0:', type=('build', 'run'))
