# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStevedore(PythonPackage):
    """Manage Dynamic Plugins for Python Applications."""

    homepage = "https://docs.openstack.org/stevedore/latest/"
    pypi = "stevedore/stevedore-1.28.0.tar.gz"

    license("Apache-2.0")

    version("5.4.0", sha256="79e92235ecb828fe952b6b8b0c6c87863248631922c8e8e0fa5b17b232c4514d")
    version("5.3.0", sha256="9a64265f4060312828151c204efbe9b7a9852a0d9228756344dbc7e4023e375a")
    version("5.2.0", sha256="46b93ca40e1114cea93d738a6c1e365396981bb6bb78c27045b7587c9473544d")
    version("5.1.0", sha256="a54534acf9b89bc7ed264807013b505bf07f74dbe4bcfa37d32bd063870b087c")
    version("5.0.0", sha256="2c428d2338976279e8eb2196f7a94910960d9f7ba2f41f3988511e95ca447021")
    version("4.0.0", sha256="f82cc99a1ff552310d19c379827c2c64dd9f85a38bcd5559db2470161867b786")
    version("3.5.0", sha256="f40253887d8712eaa2bb0ea3830374416736dc8ec0e22f5a65092c1174c44335")
    version("1.28.0", sha256="f1c7518e7b160336040fee272174f1f7b29a46febb3632502a8f2055f973d60b")

    depends_on("python@2.6:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@3.5.0:")
    depends_on("python@3.8:", type=("build", "run"), when="@4.0.0:")

    depends_on("py-setuptools", type="build")

    depends_on("py-six@1.10.0:", type=("build", "run"), when="@:3.4")
    depends_on("py-pbr@2.0.0:2.1.0", type=("build", "run"), when="@:3.4")
    depends_on("py-pbr@2.0.0:", type=("build", "run"), when="@3.5.0:")
