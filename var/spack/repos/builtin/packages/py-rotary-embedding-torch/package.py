# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRotaryEmbeddingTorch(PythonPackage):
    """A standalone library for adding rotary embeddings to transformers in Pytorch,
    following its success as relative positional encoding. Specifically it will make
    rotating information into any axis of a tensor easy and efficient, whether they
    be fixed positional or learned. This library will give you state of the art
    results for positional embedding, at little costs."""

    homepage = "https://github.com/lucidrains/rotary-embedding-torch"
    pypi = "rotary-embedding-torch/rotary-embedding-torch-0.5.3.tar.gz"

    maintainers("meyersbs")

    version("0.5.3", sha256="45db29b19bd7025f09d202752c26bf6921b05d8b5a977cfcdc625ce96ddf2b5c")

    depends_on("py-setuptools", type="build")
    depends_on("py-beartype", type=("build", "run"))
    depends_on("py-einops@0.7:", type=("build", "run"))
    depends_on("py-torch@2.0:", type=("build", "run"))
