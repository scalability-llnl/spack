# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHypothesis(PythonPackage):
    """A library for property based testing."""

    homepage = "https://github.com/HypothesisWorks/hypothesis-python"
    pypi = "hypothesis/hypothesis-4.41.2.tar.gz"

    license("MPL-2.0")

    version("6.96.2", sha256="524a0ac22c8dfff640f21f496b85ee193a470e8570ab7707b8e3bfccd7da34a6")
    version("6.23.1", sha256="23a1b0488aec5719e2f9e399342e10f30d497cbb9fd39470ef0975c1b502ae35")
    version("5.3.0", sha256="c9fdb53fe3bf1f8e7dcca1a7dd6e430862502f088aca2903d141511212e79429")
    version("4.57.1", sha256="3c4369a4b0a1348561048bcda5f1db951a1b8e2a514ea8e8c70d36e656bf6fa0")
    version("4.41.2", sha256="6847df3ffb4aa52798621dd007e6b61dbcf2d76c30ba37dc2699720e2c734b7a")
    version("4.24.3", sha256="fd90a319f409f34a173156ca704d6c0c6c0bb30a2e43dbf26aced2c75569e5d5")
    version("4.7.2", sha256="87944c6379f77634474b88abbf1e5ed5fe966637cc926131eda5e2af5b54a608")
    version("3.7.0", sha256="0fea49d08f2d5884f014151a5af6fb48d862f6ad567ffc4a2e84abf2f186c423")

    variant("django", default=False, description="Enable django support")
    variant("numpy", default=False, description="Enable numpy support")
    variant("pandas", default=False, description="Enable pandas support")

    depends_on("py-setuptools@36.2:", type="build")
    depends_on("py-attrs@22.2:", when="@6.96:", type=("build", "run"))
    depends_on("py-attrs@19.2:", when="@4.38.2:", type=("build", "run"))
    depends_on("py-attrs@16.0:", when="@3.44.22:", type=("build", "run"))
    depends_on("py-attrs", when="@3.28.0:", type=("build", "run"))
    depends_on("py-exceptiongroup@1:", when="@6.96: ^python@:3.10", type=("build", "run"))
    depends_on("py-sortedcontainers@2.1:2", type=("build", "run"), when="@4.57.1:")

    depends_on("py-django@3.2:", type="run", when="@6.96: +django")
    depends_on("py-django@2.2:", type="run", when="+django")
    depends_on("py-pytz@2014.1:", type="run", when="+django")
    depends_on("py-numpy@1.17.3:", type="run", when="@6.96: +numpy")
    depends_on("py-numpy@1.9.0:", type="run", when="+numpy")
    # https://github.com/HypothesisWorks/hypothesis/issues/3950
    depends_on("py-numpy@:1", when="@:6.100.1+numpy", type="run")
    depends_on("py-pandas@1.1:", type="run", when="@6.96: +pandas")
    depends_on("py-pandas@0.25:", type="run", when="+pandas")

    @property
    def skip_modules(self):
        modules = []
        if "+django" not in self.spec:
            modules.append("hypothesis.extra.django")
        if "+pandas" not in self.spec:
            modules.append("hypothesis.extra.pandas")
        return modules
