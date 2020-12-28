# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyWasabi(PythonPackage):
    """wasabi: A lightweight console printing and formatting toolkit."""

    homepage = "https://ines.io/"
    url      = "https://pypi.io/packages/source/w/wasabi/wasabi-0.6.0.tar.gz"

    version('0.6.0', sha256='b8dd3e963cd693fde1eb6bfbecf51790171aa3534fa299faf35cf269f2fd6063')

    depends_on('py-setuptools', type='build')
