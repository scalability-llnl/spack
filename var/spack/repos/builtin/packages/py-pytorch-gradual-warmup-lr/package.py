# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytorchGradualWarmupLr(PythonPackage):
    """Gradually warm-up (increasing) learning rate for pytorch's optimizer."""

    homepage = "https://github.com/ildoonet/pytorch-gradual-warmup-lr"
    url = "https://github.com/ildoonet/pytorch-gradual-warmup-lr/archive/v0.3.2.tar.gz"

    license("MIT")

    version("0.3.2", sha256="3ff3ccd0f5130a3c2ffe3bf7e43e7f85d599e0de3ccb42a1704809222e069a18")
    version("0.3.1", sha256="3070c7999dc8b6322089ed6a7fc375e1ef2661524097bf461016013b21177819")
    version("0.3", sha256="a4a6066461ec5a00e49bb3afa956f9135684b46006f0dcb46f39a19b57d49acb")
    version("0.2", sha256="83dded13e630d4f8c3b247f49d1271ebecdff0a53979ba2a1f361b3479ff5b61")
    version("0.1.1", sha256="aaac344996570a680171d1dc164254a51c870a3f5e9c9b28ad5d66de2a4e3c80")
    version("0.1", sha256="830e0e16a415700543ba7622af82238c4e41013de513b6d14417fb438128c84d")

    depends_on("py-setuptools", type="build")
