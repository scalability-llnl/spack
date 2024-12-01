# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLogilabCommon(PythonPackage):
    """Common modules used by Logilab projects"""

    homepage = "https://www.logilab.org/project/logilab-common"
    pypi = "logilab-common/logilab-common-1.2.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.4.2", sha256="cdda9ed0deca7c68f87f7a404ad742e47aaa1ca5956d12988236a5ec3bda13a0")
    version("1.2.0", sha256="d4e5cec3be3a89f06ff05e359a221e69bd1da33cb7096cad648ddcccea8465b7")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-six@1.4.0:", type=("build", "run"))
