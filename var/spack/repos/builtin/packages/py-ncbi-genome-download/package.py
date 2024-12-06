# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNcbiGenomeDownload(PythonPackage):
    """Scripts to download genomes from the NCBI FTP servers"""

    homepage = "https://github.com/kblin/ncbi-genome-download/"
    pypi = "ncbi-genome-download/ncbi-genome-download-0.3.1.tar.gz"

    license("Apache-2.0")

    version("0.3.1", sha256="74675e94f184b8d80429641b27ed6d46ed81028d95156337de6d09f8dd739c6e")

    depends_on("py-setuptools", type="build")
    depends_on("py-appdirs", type=("build", "run"))
    depends_on("py-requests@2.4.3:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
