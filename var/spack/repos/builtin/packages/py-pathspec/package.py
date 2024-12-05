# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPathspec(PythonPackage):
    """pathspec extends the test loading and running features of unittest,
    making it easier to write, find and run tests."""

    homepage = "https://github.com/cpburnz/python-pathspec"
    pypi = "pathspec/pathspec-0.8.1.tar.gz"

    license("MPL-2.0")

    version("0.11.1", sha256="2798de800fa92780e33acca925945e9a19a133b715067cf165b8866c15a31687")
    version("0.11.0", sha256="64d338d4e0914e91c1792321e6907b5a593f1ab1851de7fc269557a21b30ebbc")
    version("0.10.3", sha256="56200de4077d9d0791465aa9095a01d421861e405b5096955051deefd697d6f6")
    version("0.10.2", sha256="8f6bf73e5758fd365ef5d58ce09ac7c27d2833a8d7da51712eac6e27e35141b0")
    version("0.10.1", sha256="7ace6161b621d31e7902eb6b5ae148d12cfd23f4a249b9ffb6b9fee12084323d")
    version("0.9.0", sha256="e564499435a2673d586f6b2130bb5b95f04a3ba06f81b8f895b651a3c76aabb1")
    version("0.8.1", sha256="86379d6b86d75816baba717e64b1a3a3469deb93bb76d613c9ce79edc5cb68fd")
    version("0.5.5", sha256="72c495d1bbe76674219e307f6d1c6062f2e1b0b483a5e4886435127d0df3d0d3")
    version("0.3.4", sha256="7605ca5c26f554766afe1d177164a2275a85bb803b76eba3428f422972f66728")

    depends_on("python@3.7:", when="@0.10:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-flit-core@3.2:3", when="@0.11:", type="build")
    depends_on("py-setuptools@40.8:", when="@0.10", type="build")
    depends_on("py-setuptools@39.2:", when="@0.9", type="build")
    depends_on("py-setuptools", when="@:0.10", type="build")
