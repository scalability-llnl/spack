# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyEmbeddingReader(PythonPackage):
    """Embedding reader is a module to make it easy to read efficiently a large
    collection of embeddings stored in any file system."""

    homepage = "https://github.com/rom1504/embedding-reader"
    # PyPI source is missing requirements.txt
    url = "https://github.com/rom1504/embedding-reader/archive/refs/tags/1.7.0.tar.gz"

    license("MIT", checked_by="alex391")

    version("1.7.0", sha256="3bae324a06d795ea025317fdcfeb6ef1632e37786bf171973e83543700bbef73")

    depends_on("py-setuptools", type="build")
    depends_on("py-tqdm@4.62.3:4", type=("build", "run"))
    depends_on("py-fsspec@2022.1.0:", type=("build", "run"))
    depends_on("py-numpy@1.19.5:1", type=("build", "run"))
    depends_on("py-pandas@1.1.5:2", type=("build", "run"))
    depends_on("py-pyarrow@6.0.1:15", type=("build", "run"))
