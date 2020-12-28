# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribMermaid(PythonPackage):
    """This extension allows you to embed
    `Mermaid <http://knsv.github.io/mermaid/>`_ graphs in your documents,
    including general flowcharts, sequence and gantt diagrams."""

    homepage = "https://github.com/mgaitan/sphinxcontrib-mermaid"
    url = "https://files.pythonhosted.org/packages/8e/0a/8a97b65608a63c43a99a9d6a37a5baff853f306e8506bf21ce54bb50d4f3/sphinxcontrib-mermaid-0.4.0.tar.gz"

    version('0.4.0', sha256='0ee45ba45b9575505eacdd6212e4e545213f4f93dfa32c7eeca32720dbc3b468')
    version('0.3.1', sha256='649738afc3022d25a742a928f7b4146cf6024b1d8bb49017962713d2de78123c', extension='zip')

    depends_on('py-sphinx@1.7:')
