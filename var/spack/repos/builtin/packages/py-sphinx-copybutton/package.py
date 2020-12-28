# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxCopybutton(PythonPackage):
    """A small sphinx extension to add a "copy" button to code blocks."""

    homepage = "https://github.com/choldgraf/sphinx-copybutton"
    url      = "https://files.pythonhosted.org/packages/b7/74/da355d8a909a7934b5f1711fce6f056e0c398094918dec3a23703662a0fe/sphinx-copybutton-0.2.12.tar.gz"

    version('0.2.12', sha256='9492883786984b6179c92c07ab0410237b26efa826adfa792acfd17b91a63e5c')

    depends_on('py-setuptools', type='build')
    depends_on('py-sphinx@1.8:')
