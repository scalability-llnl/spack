# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMystParser(PythonPackage):
    """A Sphinx and Docutils extension to parse MyST, a rich and
    extensible flavour of Markdown for authoring technical and
    scientific documentation."""

    homepage = "https://github.com/executablebooks/MyST-Parser"
    git = "https://github.com/executablebooks/MyST-Parser"
    pypi = "myst-parser/myst_parser-4.0.0.tar.gz"

    license("MIT")

    version("4.0.0", sha256="851c9dfb44e36e56d15d05e72f02b80da21a9e0d07cba96baf5e2d476bb91531")
    version("3.0.1", sha256="88f0cb406cb363b077d176b51c476f62d60604d68a8dcdf4832e080441301a87")
    version("3.0.0", sha256="0b4ae0b33a45800a748260cb40348c37089a8a456c35120609240bd1b32f9255")
    version("2.0.0", sha256="ea929a67a6a0b1683cdbe19b8d2e724cd7643f8aa3e7bb18dd65beac3483bead")
    version("1.0.0", sha256="502845659313099542bd38a2ae62f01360e7dd4b1310f025dd014dfc0439cdae")
    version("0.19.1", sha256="f2dc168ed380e01d77973ad22a64fff1377cc72a3d1ac4bced423f28258d0a42")
    version("0.19.0", sha256="5a278c02015ce89f282dfde2a6e43d0924d957ab57d83555fce1645448810577")
    version("0.18.1", sha256="79317f4bb2c13053dd6e64f9da1ba1da6cd9c40c8a430c447a7b146a594c246d")

    def url_for_version(self, version):
        prefix = self.url.rsplit("/", maxsplit=1)[0]
        package = "myst-parser" if version < Version("2.0.0") else "myst_parser"
        return f"{prefix}/{package}-{version}.tar.gz"

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("python@3.8:3", type=("build", "run"), when="@2:")
    depends_on("python@3.10:3", type=("build", "run"), when="@4:")

    depends_on("py-flit-core@3.4:3", type="build")

    depends_on("py-docutils@0.15:0.19", type=("build", "run"), when="@:1")
    depends_on("py-docutils@0.16:0.20", type=("build", "run"), when="@2:")
    depends_on("py-docutils@0.18:0.21", type=("build", "run"), when="@3:")
    depends_on("py-docutils@0.19:0.21", type=("build", "run"), when="@4:")

    depends_on("py-jinja2", type=("build", "run"))  # let sphinx decide version

    depends_on("py-markdown-it-py@1:2", type=("build", "run"), when="@:1")
    depends_on("py-markdown-it-py@3", type=("build", "run"), when="@2:")

    depends_on("py-mdit-py-plugins@0.3.1:0.3", type=("build", "run"), when="@0.18")
    depends_on("py-mdit-py-plugins@0.3.4:0.3", type=("build", "run"), when="@0.19:1")
    depends_on("py-mdit-py-plugins@0.4", type=("build", "run"), when="@2:3")
    depends_on("py-mdit-py-plugins@0.4.1:0.4", type=("build", "run"), when="@4:")

    depends_on("py-pyyaml", type=("build", "run"))

    depends_on("py-sphinx@4:5", type=("build", "run"), when="@0.18")
    depends_on("py-sphinx@5:6", type=("build", "run"), when="@0.19:1")
    depends_on("py-sphinx@6:7", type=("build", "run"), when="@2:3")
    depends_on("py-sphinx@7:8", type=("build", "run"), when="@4:")

    depends_on("py-typing-extensions", type=("build", "run"), when="@:1")
