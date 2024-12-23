# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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
    version("1.8.4", sha256="0f49471f04439269d0e66a6f43120f52d11d594869a2a0be600cfb12eb0616b9")
    version("1.8.3", sha256="6d75bdfa7aa9ed2c467789a0688bc6da23fbe3a143e19aa6ad3f8bac113d2ab3")
    version("1.8.2", sha256="8e29bdede858b59aa2859a1ab1c4ccbd39ed7ed5870262dae756fba6b5dc72e8")
    version("1.8.1", sha256="73c2ec88a66d7bf6b8c32783539d1c9c92c7c75847f14186092d27f83b206e8a")
    version("1.8.0", sha256="f8cad0d67d286d6cd6fc9f69f2d6f25c6c4c2d99fb9d6cb3b8987b593dbe6fa8")
    version("1.7.4", sha256="7ce5de8e4dc0333aec946113529b3eeb349f2e5d2fafee96b9edf8ee36a01395")
    version("1.7.3", sha256="bced1594c497dc007ab49508ff198bb437c576d01291c13a61658999066481f4")
    version("1.7.2", sha256="22f93439a3d65f4a04e07cd584f4d01d132d96899766af92ed287618156abbe2")
    version("1.7.1", sha256="660c8ea345343f47c5de88f62afa34a19d9f4c7accdd9c6e39dc17eece6affcd")
    version("1.7.0", sha256="ab34e5d9f7733c4e6072f4de79eb3b35ac9ae78e692ea8a543f3b2828b30fee4")
    version("1.6.1", sha256="f8ff96693ec6e261d1544e9f7d9a5811c5ef5d74c8adb4978430fc0dac16777e")
    version("1.6.0", sha256="33799c31f8817101f2eb8fe90e95d2c2acd428a567ee64358ca487f963f75e9c")
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
