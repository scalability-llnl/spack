# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyThinc(PythonPackage):
    """Thinc: Practical Machine Learning for NLP in Python."""

    homepage = "https://github.com/explosion/thinc"
    pypi = "thinc/thinc-7.4.1.tar.gz"

    license("MIT")

    version("7.4.1", sha256="0139fa84dc9b8d88af15e648fc4ae13d899b8b5e49cb26a8f4a0604ee9ad8a9e")
    version("7.4.0", sha256="523e9be1bfaa3ed1d03d406ce451b6b4793a9719d5b83d2ea6b3398b96bc58b8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-murmurhash@0.28:1.0", type=("build", "run"))
    depends_on("py-cymem@2.0.2:2.0", type=("build", "run"))
    depends_on("py-preshed@1.0.1:3.0", type=("build", "run"))
    depends_on("py-blis@0.4.0:0.4", type=("build", "run"))
    depends_on("py-wasabi@0.0.9:1.0", type=("build", "run"))
    depends_on("py-srsly@0.0.6:1.0", type=("build", "run"))
    depends_on("py-catalogue@0.0.7:1.0", type=("build", "run"))
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-plac@0.9.6:1.1", type=("build", "run"))
    depends_on("py-tqdm@4.10:4", type=("build", "run"))
