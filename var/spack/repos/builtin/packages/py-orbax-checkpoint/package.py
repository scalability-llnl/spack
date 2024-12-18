# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOrbaxCheckpoint(PythonPackage):
    """Orbax includes a checkpointing library oriented towards JAX users, supporting a variety
    of different features required by different frameworks, including asynchronous checkpointing
    various types, and various storage formats. We aim to provide a highly customizable and
    composable API which maximizes flexibility for diverse use cases.
    """

    homepage = "https://github.com/google/orbax"
    pypi = "orbax_checkpoint/orbax_checkpoint-0.5.3.tar.gz"

    license("Apache-2.0")

    version("0.5.3", sha256="1572904cbbfe8513927e0d80f80b730e0ef2f680332d3c2810d8443532938b45")

    depends_on("py-flit-core@3.5:3", type="build")

    with default_args(type=("build", "run")):
        depends_on("python@3.9:")
        depends_on("py-absl-py")
        depends_on("py-etils+epath+epy")
        depends_on("py-typing-extensions")
        depends_on("py-msgpack")
        depends_on("py-jax@0.4.9:")
        depends_on("py-jaxlib")
        depends_on("py-numpy")
        depends_on("py-pyyaml")
        depends_on("py-tensorstore@0.1.51:")
        depends_on("py-nest-asyncio")
        depends_on("py-protobuf")
