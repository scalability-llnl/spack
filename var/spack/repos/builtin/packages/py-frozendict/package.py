# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFrozendict(PythonPackage):
    """An immutable dictionary"""

    homepage = "https://github.com/Marco-Sulla/python-frozendict"
    pypi = "frozendict/frozendict-1.2.tar.gz"

    license("LGPL-3.0-only")

    version("2.3.10", sha256="aadc83510ce82751a0bb3575231f778bc37cbb373f5f05a52b888e26cbb92f79")
    version("2.3.4", sha256="15b4b18346259392b0d27598f240e9390fafbff882137a9c48a1e0104fb17f78")
    version("1.2", sha256="774179f22db2ef8a106e9c38d4d1f8503864603db08de2e33be5b778230f6e45")

    depends_on("c", type="build")  # generated

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    def setup_build_environment(self, env):
        # C extension is not supported for 3.11+. See also
        # https://github.com/Marco-Sulla/python-frozendict/issues/68
        if self.spec.satisfies("^python@3.11:"):
            env.set("FROZENDICT_PURE_PY", "1")
