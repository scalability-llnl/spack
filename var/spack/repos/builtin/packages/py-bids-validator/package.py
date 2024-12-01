# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBidsValidator(PythonPackage):
    """Validator for the Brain Imaging Data Structure"""

    homepage = "https://github.com/bids-standard/bids-validator"
    pypi = "bids-validator/bids-validator-1.7.2.tar.gz"

    version("1.13.1", sha256="7205ce4e68fba172215332c786f1ac1665025b702b6dff2b1e158f00a2df9890")
    version("1.11.0", sha256="408c56748b7cf98cf7c31822f33a8d89c5e6e7db5254c345107e8d527576ff53")
    version("1.9.8", sha256="ff39799bb205f92d6f2c322f0b8eff0d1c0288f4291a0b18fce61afa4dfd7f3e")
    version("1.9.4", sha256="4bf07d375f231a2ad2f450beeb3ef6c54f93194fd993aa5157d57a8fba48ed50")
    version("1.8.9", sha256="01fcb5a8fe6de1280cdfd5b37715103ffa0bafb3c739ca7f5ffc41e46549612e")
    version("1.8.4", sha256="63e7a02c9ddb5505a345e178f4e436b82c35ec0a177d7047b67ea10ea3029a68")
    version("1.7.2", sha256="12398831a3a3a2ed7c67e693cf596610c23dd23e0889bfeae0830bbd1d41e5b9")

    depends_on("python@3.8:", when="@1.12:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
