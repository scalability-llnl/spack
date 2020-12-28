# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycurl(PythonPackage):
    """PycURL is a Python interface to libcurl. PycURL can be used to fetch
    objects identified by a URL from a Python program."""

    homepage = "http://pycurl.io/"
    url      = "https://pypi.io/packages/source/p/pycurl/pycurl-7.43.0.tar.gz"

    version('7.43.0', sha256='aa975c19b79b6aa6c0518c0cc2ae33528900478f0b500531dbcdbf05beec584c')

    depends_on('python@2.6:')
    depends_on('curl@7.19.0:')
