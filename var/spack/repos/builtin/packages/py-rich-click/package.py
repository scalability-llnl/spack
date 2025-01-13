# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRichClick(PythonPackage):
    """The intention of rich-click is to provide attractive help output
    from click, formatted with rich, with minimal customisation required."""

    homepage = "https://github.com/ewels/rich-click"
    pypi = "rich-click/rich_click-1.8.5.tar.gz"

    license("MIT")

    version("1.8.5", sha256="a3eebe81da1c9da3c32f3810017c79bd687ff1b3fa35bfc9d8a3338797f1d1a1")
    version("1.7.4", sha256="7ce5de8e4dc0333aec946113529b3eeb349f2e5d2fafee96b9edf8ee36a01395")
    version("1.6.1", sha256="f8ff96693ec6e261d1544e9f7d9a5811c5ef5d74c8adb4978430fc0dac16777e")
    version("1.5.2", sha256="a57ca70242cb8b372a670eaa0b0be48f2440b66656deb4a56e6aadc1bbb79670")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-click@7:", type=("build", "run"))
    depends_on("py-rich@10.7.0:", type=("build", "run"))
    depends_on("py-importlib-metadata", type=("build", "run"), when="^python@:3.7")
    depends_on("py-typing-extensions@4", type=("build", "run"), when="@1.8.0:")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/r/rich-click/{0}-{1}.tar.gz"
        if version >= Version("1.8.0"):
            name = "rich_click"
        else:
            name = "rich-click"
        return url.format(name, version)
