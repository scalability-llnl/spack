# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AsciidocPy3(AutotoolsPackage):
    """Python 3 port of Asciidoc Python.
    AsciiDoc is a text document format for writing notes,
    documentation, articles, books, ebooks, slideshows,
    web pages, man pages and blogs. AsciiDoc files can
    be translated to many formats including HTML, PDF,
    EPUB, man page."""

    homepage = "https://github.com/asciidoc/asciidoc-py3"
    url = "https://github.com/asciidoc/asciidoc-py3/releases/download/9.0.2/asciidoc-9.0.2.tar.gz"

    version("9.1.0", sha256="fd499fcf51317b1aaf27336fb5e919c44c1f867f1ae6681ee197365d3065238b")
    version("9.0.5", sha256="1a20647eb62ca37bc8107affab968caa0f674f0e962b497d1674391f636c7038")
    version("9.0.4", sha256="400368a43f3eee656d7f197382cd3554b50fb370ef2aea6534f431692a356c66")
    version("9.0.3", sha256="d99c8be8e8a9232742253c2d87c547b2efd4bbd3f0c1e23ef14898ad0fff77c4")
    version("9.0.2", sha256="185fd68e47034c4dd892e1d4ae64c81152bc049e9bdc7d1ad63f927d35810a3b")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("libxml2", type=("build", "run"))
    depends_on("libxslt", type=("build", "run"))
    depends_on("docbook-xml", type=("build", "run"))
    depends_on("docbook-xsl", type=("build", "run"))
