# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRuamelYaml(PythonPackage):
    """
    a YAML parser/emitter that supports roundtrip preservation of comments,
    seq/map flow style, and map key order
    """

    homepage = "https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree"
    pypi = "ruamel.yaml/ruamel.yaml-0.16.10.tar.gz"

    license("MIT")

    version("0.17.32", sha256="ec939063761914e14542972a5cba6d33c23b0859ab6342f61cf070cfc600efc2")
    version("0.17.16", sha256="1a771fc92d3823682b7f0893ad56cb5a5c87c48e62b5399d6f42c8759a583b33")
    version("0.16.10", sha256="099c644a778bf72ffa00524f78dd0b6476bca94a1da344130f4bf3381ce5b954")
    version("0.16.5", sha256="412a6f5cfdc0525dee6a27c08f5415c7fd832a7afcb7a0ed7319628aed23d408")
    version("0.11.7", sha256="c89363e16c9eafb9354e55d757723efeff8682d05e56b0881450002ffb00a344")

    # from `supported` in __init__.py
    depends_on("python@3.7:", when="@0.17.22:", type=("build", "run"))
    # from setup.py
    depends_on("py-setuptools@28.7:", when="@0.17:", type=("build"))
    depends_on("py-setuptools", type="build")
    # from __init__.py
    depends_on("py-ruamel-yaml-clib@0.2.7:", when="@0.17.23: ^python@:3.11", type=("build", "run"))
    depends_on(
        "py-ruamel-yaml-clib@0.1.2:", when="@0.16:0.17.22 ^python@:3.8", type=("build", "run")
    )

    @run_after("install")
    def fix_import_error(self):
        if str(self.spec["python"].version.up_to(1)) == "2":
            touch = which("touch")
            touch(join_path(python_purelib, "ruamel", "__init__.py"))
