# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRuamelYamlClib(PythonPackage):
    """C version of reader, parser and emitter for ruamel.yaml derived from
    libyaml."""

    homepage = "https://sourceforge.net/p/ruamel-yaml-clib/code/ci/default/tree/"
    pypi = "ruamel.yaml.clib/ruamel.yaml.clib-0.2.0.tar.gz"

    license("MIT")

    version("0.2.7", sha256="1f08fd5a2bea9c4180db71678e850b995d2a5f4537be0e94557668cf0f5f9497")
    version("0.2.0", sha256="b66832ea8077d9b3f6e311c4a53d06273db5dc2db6e8a908550f3c14d67e718c")

    depends_on("c", type="build")  # generated

    depends_on("python", type=("build", "link", "run"))
    # to prevent legacy-install-failure
    depends_on("python@:3.9", when="@0.2.0", type=("build", "link", "run"))
    depends_on("py-setuptools@28.7.0:", type="build")

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%oneapi") or self.spec.satisfies(" %apple-clang@15:"):
                flags.append("-Wno-error=incompatible-function-pointer-types")
        return (flags, None, None)
