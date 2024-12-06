# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClickOptionGroup(PythonPackage):
    """click-option-group is a Click-extension package that adds option groups missing in Click."""

    homepage = "https://github.com/click-contrib/click-option-group/"

    pypi = "click-option-group/click-option-group-0.5.6.tar.gz"

    license("BSD-3-Clause")

    version("0.5.6", sha256="97d06703873518cc5038509443742b25069a3c7562d1ea72ff08bfadde1ce777")
    version("0.5.5", sha256="78ee474f07a0ca0ef6c0317bb3ebe79387aafb0c4a1e03b1d8b2b0be1e42fc78")
    version("0.5.4", sha256="d4b8d808a1998f0f277ebe13c33d64863a5b2a619b1e54f67bc6e3723d91b910")
    version("0.5.3", sha256="a6e924f3c46b657feb5b72679f7e930f8e5b224b766ab35c91ae4019b4e0615e")
    version("0.5.2", sha256="743733a0f564438b6b761f49ddf37d845f9a662294ecabe0e832e597208bcf31")
    version("0.5.1", sha256="764eb49094dc864e28afbf36c6bb140d09ef714a915c0c5972c982113ed70fab")
    version("0.5.0", sha256="07cc8fec3adfd2cd2af99c2105cefcefa730e0281669753cc9ab6f6515a108d0")
    version("0.4.0", sha256="7867689533ea52cb3494a2ea02d77c42494583d99746ff1dd24674f6ec208820")
    version("0.3.0", sha256="36c7f30ef1f3c0d3d378aa8805004d93dec6e97010e4dae4ec66bde4e906c2fa")

    depends_on("python@3.6:3", type=("build", "run"))

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-click@7:8", type=("build", "run"))
