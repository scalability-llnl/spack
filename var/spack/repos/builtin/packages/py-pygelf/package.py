# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygelf(PythonPackage):
    """Python logging handlers with GELF (Graylog Extended Log Format)
    support."""

    homepage = "https://github.com/keeprocking/pygelf"
    pypi = "pygelf/pygelf-0.3.6.tar.gz"

    # notify when the package is updated.
    maintainers("victorusu", "vkarak")

    license("MIT")

    version("0.4.0", sha256="3693da38794561d42b0556a78af7dcb22d92ea450125577e58089ab89a890ee5")
    version("0.3.6", sha256="3e5bc59e3b5a754556a76ff2c69fcf2003218ad7b5ff8417482fa1f6a7eba5f9")

    depends_on("python", type=("build", "run"))
    depends_on("py-setuptools", type="build")
