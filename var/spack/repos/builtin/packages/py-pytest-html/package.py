# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestHtml(PythonPackage):
    """pytest-html is a plugin for pytest that generates
    a HTML report for test results
    """

    homepage = "https://github.com/pytest-dev/pytest-html"
    pypi = "pytest-html/pytest-html-3.1.1.tar.gz"
    git = "https://github.com/pytest-dev/pytest-html.git"

    version("3.2.0", sha256="c4e2f4bb0bffc437f51ad2174a8a3e71df81bbc2f6894604e604af18fbe687c3")
    version("3.1.1", sha256="3ee1cf319c913d19fe53aeb0bc400e7b0bc2dbeb477553733db1dad12eb75ee3")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm+toml@3.5.0:", type="build")
    depends_on("py-setuptools-scm-git-archive@1.1:", type="build")
    depends_on("py-wheel@0.33.6:", type="build")
    depends_on("py-pytest@5.0:5,6.0.1:", type=("build", "run"))
    depends_on("py-pytest-metadata", type=("build", "run"))

    # https://github.com/spack/spack/pull/38989
    # py-pytest@7.2 removed py-py dependency, but now py-pytest conflicts with py-py. And
    # py-pytest-htm@:3 requires py-py.
    # One workaround is to always add py-py *before* py-pytest in PYTHONPATH, but we cannot ensure
    # that. So don't allow this configuration, pending py-pytest-html@4.
    conflicts("^py-pytest@7.2:", when="@:3")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        # Simplest test: pytest will load pytest-html plugin
        output = python("-m", "pytest", "-VV", output=str, error=str)
        assert self.prefix in output, f"Missing pytest-html in {output!r}"
