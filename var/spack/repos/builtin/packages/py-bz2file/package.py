# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBz2file(PythonPackage):
    """Python library for reading and writing bzip2-compressed files."""

    homepage = "https://github.com/nvawda/bz2file"
    url      = "https://pypi.io/packages/source/b/bz2file/bz2file-0.98.tar.gz"

    version('0.98', sha256='64c1f811e31556ba9931953c8ec7b397488726c63e09a4c67004f43bdd28da88')
