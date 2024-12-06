# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUrllib3SecureExtra(PythonPackage):
    """Marker library to detect whether urllib3 was installed with the deprecated [secure] extra"""

    homepage = "https://github.com/urllib3/urllib3-secure-extra"
    pypi = "urllib3-secure-extra/urllib3-secure-extra-0.1.0.tar.gz"

    version("0.1.0", sha256="ee9409cbfeb4b8609047be4c32fb4317870c602767e53fd8a41005ebe6a41dff")

    depends_on("py-flit-core@3.2:3", type="build")
