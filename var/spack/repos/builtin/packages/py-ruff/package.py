# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRuff(PythonPackage):
    """An extremely fast Python linter, written in Rust."""

    homepage = "https://beta.ruff.rs/docs"
    pypi = "ruff/ruff-0.0.276.tar.gz"
    git = "https://github.com/astral-sh/ruff.git"

    license("MIT")
    maintainers("adamjstewart")

    version("0.6.5", sha256="4d32d87fab433c0cf285c3683dd4dae63be05fd7a1d65b3f5bf7cdd05a6b96fb")
    version("0.5.7", sha256="8dfc0a458797f5d9fb622dd0efc52d796f23f0a1493a9527f4e49a550ae9a7e5")
    version("0.4.5", sha256="286eabd47e7d4d521d199cab84deca135557e6d1e0f0d01c29e757c3cb151b54")
    version("0.4.0", sha256="7457308d9ebf00d6a1c9a26aa755e477787a636c90b823f91cd7d4bea9e89260")
    version("0.3.7", sha256="d5c1aebee5162c2226784800ae031f660c350e7a3402c4d1f8ea4e97e232e3ba")
    version("0.3.0", sha256="0886184ba2618d815067cf43e005388967b67ab9c80df52b32ec1152ab49f53a")
    version("0.1.6", sha256="1b09f29b16c6ead5ea6b097ef2764b42372aebe363722f1605ecbcd2b9207184")

    with default_args(type="build"):
        depends_on("py-maturin@1")

        # Found in Cargo.toml
        depends_on("rust@1.76:", when="@0.5.6:")
        depends_on("rust@1.71:")
