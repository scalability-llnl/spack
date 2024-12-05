# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

pycmake_versions = {
    "3.27.9": "d8a40eef1268c91e5b520b28fd5fe0591d750e48e44276dbfd493a14ee595c41",
    "3.22.2": "b5bd5eeb488b13cf64ec963800f3d979eaeb90b4382861b86909df503379e219",
    "3.21.4": "30fa5ed8a5ad66dcd263adb87f3ce3dc2d0ec0ac3958f5becff577e4b62cd065",
    "3.18.0": "52b98c5ee70b5fa30a8623e96482227e065292f78794eb085fdf0fecb204b79b",
}


class PyCmake(PythonPackage):
    """CMake is an open-source, cross-platform family of tools designed to
    build, test and package software.

    Deprecated: use cmake instead.
    """

    homepage = "https://cmake.org"
    git = "https://github.com/scikit-build/cmake-python-distributions.git"
    pypi = "cmake/cmake-3.22.2.tar.gz"

    license("Apache-2.0")

    for v, sha in pycmake_versions.items():
        version(v, sha256=sha, deprecated=True)

    depends_on("ninja", type="build")
    depends_on("py-scikit-build@0.12:", type="build")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm+toml", when="@3.27.9:", type="build")
    # in newer pip versions --install-option does not exist
    depends_on("py-pip@:23.0", type="build")
    depends_on("git", type="build")

    for v in pycmake_versions.keys():
        depends_on(f"cmake@{v}", type=("build", "link", "run"), when=f"@{v}")

    # see:
    #   https://github.com/scikit-build/cmake-python-distributions/issues/227
    #   https://github.com/spack/spack/pull/28760#issuecomment-1029362288
    for v in pycmake_versions.keys():
        resource(
            name="cmake-src",
            git="https://gitlab.kitware.com/cmake/cmake.git",
            commit="v{0}".format(v),
            when="@{0}".format(v),
            destination="cmake-src",
            placement="cmake-src",
        )

    def install_options(self, spec, prefix):
        return ["-DBUILD_CMAKE_FROM_SOURCE=ON", "-DCMakeProject_SOURCE_DIR=cmake-src"]

    def setup_build_environment(self, env):
        if self.run_tests:
            env.set(
                "SKBUILD_CONFIGURE_OPTIONS",
                # BootstrapTest is already exlcude upstream,
                # The rest are (non-understood) known failures, disabled to get test suite working
                # todo: investigate test failures / check if still needed in newer versions
                "-DRUN_CMAKE_TEST=ON -DRUN_CMAKE_TEST_EXCLUDE=BootstrapTest|CompileWarningAsError"
                "|GET_RUNTIME_DEPENDENCIES",
            )
        else:
            env.set("SKBUILD_CONFIGURE_OPTIONS", "-DRUN_CMAKE_TEST=OFF")
