# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyExtensionHelpers(PythonPackage):
    """The extension-helpers package includes convenience helpers to
    assist with building Python packages with compiled C/Cython
    extensions. It is developed by the Astropy project but is intended
    to be general and usable by any Python package."""

    homepage = 'https://github.com/astropy/astropy-helpers'
    url = 'https://pypi.io/packages/source/e/extension-helpers/extension-helpers-0.1.tar.gz'

    depends_on('py-setuptools', type='build')

    version('0.1', sha256='ac8a6fe91c6d98986a51a9f08ca0c7945f8fd70d95b662ced4040ae5eb973882')
