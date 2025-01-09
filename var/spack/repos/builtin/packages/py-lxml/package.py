# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLxml(PythonPackage):
    """lxml is the most feature-rich and easy-to-use library for processing
    XML and HTML in the Python language."""

    homepage = "https://lxml.de/"
    pypi = "lxml/lxml-4.6.1.tar.gz"
    git = "https://github.com/lxml/lxml"

    license("BSD-3-Clause")

    version("5.3.0", sha256="4e109ca30d1edec1ac60cdbe341905dc3b8f55b16855e03a54aaf59e51ec8c6f")
    version("5.2.2", sha256="bb2dc4898180bea79863d5487e5f9c7c34297414bad54bcd0f0852aee9cfdb87")
    version("4.9.2", sha256="2455cfaeb7ac70338b3257f41e21f0724f4b5b0c0e7702da67ee6c3640835b67")
    version("4.9.1", sha256="fe749b052bb7233fe5d072fcb549221a8cb1a16725c47c37e42b0b9cb3ff2c3f")
    version("4.9.0", sha256="520461c36727268a989790aef08884347cd41f2d8ae855489ccf40b50321d8d7")
    version("4.8.0", sha256="f63f62fc60e6228a4ca9abae28228f35e1bd3ce675013d1dfb828688d50c6e23")
    version("4.6.4", sha256="daf9bd1fee31f1c7a5928b3e1059e09a8d683ea58fb3ffc773b6c88cb8d1399c")
    version("4.6.3", sha256="39b78571b3b30645ac77b95f7c69d1bffc4cf8c3b157c435a34da72e78c82468")
    version("4.6.1", sha256="c152b2e93b639d1f36ec5a8ca24cde4a8eefb2b6b83668fcd8e83a67badcb367")
    version("4.5.2", sha256="cdc13a1682b2a6241080745b1953719e7fe0850b40a5c71ca574f090a1391df6")
    version("4.4.2", sha256="eff69ddbf3ad86375c344339371168640951c302450c5d3e9936e98d6459db06")
    version("4.4.1", sha256="c81cb40bff373ab7a7446d6bbca0190bccc5be3448b47b51d729e37799bb5692")
    version("4.3.3", sha256="4a03dd682f8e35a10234904e0b9508d705ff98cf962c5851ed052e9340df3d90")
    version("4.2.5", sha256="36720698c29e7a9626a0dc802ef8885f8f0239bfd1689628ecd459a061f2807f")
    version("3.7.3", sha256="aa502d78a51ee7d127b4824ff96500f0181d3c7826e6ee7b800d068be79361c7")
    version("2.3", sha256="eea1b8d29532739c1383cb4794c5eacd6176f0972b59e8d29348335b87ff2e66")

    depends_on("c", type="build")  # generated

    variant("html5", default=False, description="Enable html5lib backend")
    variant("htmlsoup", default=False, description="Enable BeautifulSoup4 backend")
    variant("cssselect", default=False, description="Enable cssselect module")

    depends_on("py-setuptools", type="build")

    depends_on("libxml2@2.9.2:", type=("build", "link", "run"))
    depends_on("libxslt@1.1.27:", type=("build", "link", "run"))
    depends_on("py-html5lib", when="+html5", type=("build", "run"))
    depends_on("py-beautifulsoup4", when="+htmlsoup", type=("build", "run"))
    depends_on("py-cssselect@0.7:", when="+cssselect", type=("build", "run"))
    depends_on("py-cython@3.0.11:", type="build", when="@5.3:")
    depends_on("py-cython@3.0.10:", type="build", when="@5.2:")
    depends_on("py-cython@3.0.9:", type="build", when="@5.1.1:")
    depends_on("py-cython@3.0.8:", type="build", when="@5:")
    depends_on("py-cython@0.29.7:", type="build")
