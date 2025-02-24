# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHfTransfer(PythonPackage):
    """Speed up file transfers with the Hugging Face Hub."""

    homepage = "https://github.com/huggingface/hf_transfer"
    pypi = "hf_transfer/hf_transfer-0.1.8.tar.gz"

    license("Apache-2.0")

    version("0.1.8", sha256="26d229468152e7a3ec12664cac86b8c2800695fd85f9c9a96677a775cc04f0b3")

    with default_args(type="build"):
        depends_on("py-maturin@1.4:1")
