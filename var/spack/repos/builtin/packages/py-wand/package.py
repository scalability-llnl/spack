# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWand(PythonPackage):
    """Wand is a ctypes-based simple ImageMagick binding for Python."""

    homepage = "https://docs.wand-py.org"
    pypi = "Wand/Wand-0.5.6.tar.gz"

    license("MIT")

    version("0.6.13", sha256="f5013484eaf7a20eb22d1821aaefe60b50cc329722372b5f8565d46d4aaafcca")
    version("0.6.11", sha256="b661700da9f8f1e931e52726e4fc643a565b9514f5883d41b773e3c37c9fa995")
    version("0.5.9", sha256="6eaca78e53fbe329b163f0f0b28f104de98edbd69a847268cc5d6a6e392b9b28")
    version("0.5.6", sha256="d06b59f36454024ce952488956319eb542d5dc65f1e1b00fead71df94dbfcf88")
    version("0.4.2", sha256="a0ded99a9824ddd82617a4b449164e2c5c93853aaff96f9e0bab8b405d62ca7c")

    depends_on("py-setuptools", type="build")
    # provides libmagickwand
    depends_on("imagemagick")

    def setup_build_environment(self, env):
        env.set("MAGICK_HOME", self.spec["imagemagick"].prefix)
