# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsyncLru(PythonPackage):
    """Simple lru_cache for asyncio"""

    homepage = "https://github.com/wikibusiness/async_lru"
    pypi = "async-lru/async-lru-1.0.2.tar.gz"

    license("MIT")

    version("1.0.3", sha256="c2cb9b2915eb14e6cf3e717154b40f715bf90e596d73623677affd0d1fbcd32a")
    version("1.0.2", sha256="baa898027619f5cc31b7966f96f00e4fc0df43ba206a8940a5d1af5336a477cb")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/a/{0}/{0}-{1}.tar.gz"
        if version >= Version("1.0.3"):
            name = "async-lru"
        else:
            name = "async_lru"
        return url.format(name, version)
