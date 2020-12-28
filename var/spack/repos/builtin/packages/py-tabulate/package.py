# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTabulate(PythonPackage):
    """Pretty-print tabular data"""

    homepage = "https://bitbucket.org/astanin/python-tabulate"
    url      = "https://pypi.io/packages/source/t/tabulate/tabulate-0.8.6.tar.gz"

    version('0.8.7', sha256='db2723a20d04bcda8522165c73eea7c300eda74e0ce852d9022e0159d7895007')
    version('0.8.6', sha256='5470cc6687a091c7042cee89b2946d9235fe9f6d49c193a4ae2ac7bf386737c8')
    version('0.8.3', sha256='8af07a39377cee1103a5c8b3330a421c2d99b9141e9cc5ddd2e3263fea416943')
    version('0.7.7', sha256='83a0b8e17c09f012090a50e1e97ae897300a72b35e0c86c0b53d3bd2ae86d8c6')

    depends_on('py-setuptools', type='build')
