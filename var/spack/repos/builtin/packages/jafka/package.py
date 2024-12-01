# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jafka(Package):
    """
    Jafka is a distributed publish-subscribe messaging system.
    """

    homepage = "https://github.com/adyliu/jafka"
    url = "https://github.com/adyliu/jafka/releases/download/3.0.6/jafka-3.0.6.tgz"

    license("Apache-2.0")

    version("3.0.6", sha256="89c9456360ace5d43c3af52b5d2e712fc49be2f88b1b3dcfe0c8f195a3244e17")
    version("3.0.5", sha256="43f1b4188a092c30f48f9cdd0bddd3074f331a9b916b6cb566da2e9e40bc09a7")
    version("3.0.4", sha256="a5334fc9280764f9fd4b5eb156154c721f074c1bcc1e5496189af7c06cd16b45")
    version("3.0.3", sha256="226e902af7754bb0df2cc0f30195e4f8f2512d9935265d40633293014582c7e2")
    version("3.0.2", sha256="c7194476475a9c3cc09ed5a4e84eecf47a8d75011f413b26fd2c0b66c598f467")
    version("3.0.1", sha256="3a75e7e5bb469b6d9061985a1ce3b5d0b622f44268da71cab4a854bce7150d41")
    version("3.0.0", sha256="4c4bacdd5fba8096118f6e842b4731a3f7b3885514fe1c6b707ea45c86c7c409")
    version("1.6.2", sha256="fbe5d6a3ce5e66282e27c7b71beaeeede948c598abb452abd2cae41149f44196")

    depends_on("java@7:", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)
