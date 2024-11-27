# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPymummer(PythonPackage):
    """Python3 module for running MUMmer and reading the output"""

    homepage = "https://github.com/sanger-pathogens/pymummer"

    pypi = "pymummer/pymummer-0.11.0.tar.gz"

    version("0.11.0", sha256="199b8391348ff83760e9f63fdcee6208f8aa29da6506ee1654f1933e60665259")
    version("0.10.3", sha256="986555d36828bd90bf0e63d9d472e5b20c191f0e51123b5252fa924761149fc2")
    version("0.10.2", sha256="80ea1af917d8a683460a9dbe75a54a099515d0a8f0a74dd7eeced41adbb9f460")
    version("0.10.1", sha256="04a06d2faecf5b972b3a60e1493520e384cb10dd5c00bf7d643a1d059c4e8f87")
    version("0.10.0", sha256="bec0649cf0e4016949f49b46b789697f8cff043d5dfc6b6bb54ddff2cba83679")
    version("0.9.0", sha256="9c1fd30623202889a45d2d5124c24d0e4fcf1746aed82d22b292b6d6c5568e26")
    version("0.8.1", sha256="8e6d9759bedb216453eb7e94a2ea3b79a39b96fde716a35b4aadcf523ca1f313")
    version("0.8.0", sha256="dbb2817cb63873a408ba3e818d17d068633d401b21db9881503358a23792b4f3")
    version("0.7.1", sha256="7aab311c60fcb9fc5a2bce658e949d80f4801e73107eb2e835f46caed02cfedf")
    version("0.7.0", sha256="2d02cb60e6aa8e1fcfc5e07c36ce3bcf52cf447e6315cd6371a549adc20529d9")

    depends_on("py-setuptools", type="build")
    depends_on("mummer", type=("build", "run"))
    depends_on("py-pyfastaq@3.10.0:", type=("build", "run"))
