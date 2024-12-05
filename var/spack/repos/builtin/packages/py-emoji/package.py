# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEmoji(PythonPackage):
    """Emoji for Python."""

    homepage = "https://github.com/carpedm20/emoji/"
    pypi = "emoji/emoji-1.5.0.tar.gz"

    license("BSD-3-Clause")

    version("1.5.0", sha256="2eddd062f940924fb25a3108d84d77dc571927d91a419b4c30f37e253c791b19")

    depends_on("py-setuptools", type="build")
