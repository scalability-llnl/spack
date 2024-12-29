# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightly(PythonPackage):
    """A deep learning package for self-supervised learning."""

    homepage = "https://www.lightly.ai/"
    # https://github.com/lightly-ai/lightly/issues/1146
    url = "https://github.com/lightly-ai/lightly/archive/refs/tags/v1.4.1.tar.gz"

    maintainers("adamjstewart")

    license("MIT")

    version("1.5.11", sha256="2c19c0e5841b7477323ef3ffca234a60a57c0aaf6753a55c2a75d72cde9c0719")
    version("1.5.0", sha256="db49e2bafe3bc70df7f3248ad08bef4948e957c1bc5cde3769ec2b190b51eedb")
    version("1.4.26", sha256="7bbcf0a358f23659eb4089043c559c4584ef339266b1c0a9a2598c3100f2f3b8")
    version("1.4.25", sha256="c16449ee5788a7ac98dd78c1fa32702a426c718519d79522d726469d6ca119a0")
    version("1.4.18", sha256="41794f6815db178b031236793b379e5573e074fdf730506872b73766396a6bdf")
    version("1.4.17", sha256="1533ddf28c8a08b3eafd404964d03f9a62fe76405fcf8dc7206ca4093725285e")
    version("1.4.16", sha256="9bd2af53e144e4f9823409cd33b39651f579ed671ff242a1445640c9df504d92")
    version("1.4.15", sha256="9b02f523b35621a98c3e87efdda735897b726b39cf4a8bf106769f54b3df154e")
    version("1.4.14", sha256="edbad4c95866fea6951a4fc5e851518f3afb2ff19381648accb4e1a005366720")
    version("1.4.13", sha256="d3819d75b85534f98603743486b263eb1dc62cd5b20de30d5bad07227f1e0d98")
    version("1.4.12", sha256="66aea90f096c474b26515bafbef728632516d6f8f13ab5caba38b09903d1b86e")
    version("1.4.11", sha256="3c767a15368c4294a14067a93a4b07e91bd45295313f1e132f28d00270bb69d0")
    version("1.4.10", sha256="77381c913d06f3c02ad7b36a0434bfd7e27a738648f555a51c9912d80dd11125")
    version("1.4.9", sha256="33c7988b41447c9beeb1781805ad24c8a61aa174e1a37b0b95d8e91e4a7c7f96")
    version("1.4.8", sha256="3af5d8da0ac981f362bd61cbd4935dadbc32d24995c40ac2a511e6d743a03fd7")
    version("1.4.7", sha256="dce719996d9b01b2a3c652e9cbab3ff80d078c4ed86d1adb39220d20e1f3fdf2")
    version("1.4.6", sha256="1c8b904a96fadaefbaa00296eea0ac1e8b50cb10e94595c74b0abada5f4f5a64")
    version("1.4.5", sha256="67b1de64950ff5bc35ef86fec3049f437ed1c9cb4a191c43b52384460207535f")
    version(
        "1.4.4",
        sha256="e726120437ee61754da8e1c384d2ed27d9a7004e037c74d98e3debbc98cbd4a4",
        deprecated=True,
    )
    version(
        "1.4.3",
        sha256="ff2cfded234bc5338519bdb2de774c59a55200159f4429b009b7a3923bc0be0e",
        deprecated=True,
    )
    version(
        "1.4.2",
        sha256="bae451fcd04fbd3cc14b044a2583ae24591533d4a8a6ff51e5f1477f9a077648",
        deprecated=True,
    )
    version(
        "1.4.1",
        sha256="4c64657639c66ee5c8b4b8d300fc9b5287dc7e14a260f3a2e04917dca7f57f5b",
        deprecated=True,
    )

    with default_args(type="build"):
        depends_on("py-setuptools@21:", when="@1.4.2:")
        depends_on("py-setuptools-scm", when="@1.5.11:")

    with default_args(type=("build", "run")):
        depends_on("py-certifi@14.05.14:")
        depends_on("py-hydra-core@1:")
        depends_on("py-lightly-utils@0.0")
        depends_on("py-numpy@1.18.1:")
        depends_on("py-python-dateutil@2.5.3:")
        depends_on("py-requests@2.23:")
        depends_on("py-six@1.10:")
        depends_on("py-tqdm@4.44:")
        depends_on("py-torch")
        depends_on("py-torch@:1", when="@:1.4.1")
        depends_on("py-torchvision")
        depends_on("py-pytorch-lightning@1.0.4:")
        depends_on("py-pytorch-lightning@1.0.4:1", when="@:1.4.1")
        depends_on("py-urllib3@1.25.3:", when="@1.4.8:")
        depends_on("py-urllib3@1.15.1:")
        depends_on("py-pydantic@1.10.5:", when="@1.5.11:")
        depends_on("py-pydantic@1.10.5:1", when="@1.4.8:1.5.0")
        depends_on("py-aenum@3.1.11:", when="@1.4.8:")

        # Historical dependencies
        depends_on("py-setuptools@21:", when="@1.4.8,1.4.15:1.4.25")
        depends_on("py-setuptools@21:65.5.1", when="@:1.4.1")

        # https://github.com/lightly-ai/lightly/issues/1558
        depends_on("py-numpy@:1", when="@:1.5.10")

        # https://github.com/lightly-ai/lightly/issues/1153
        depends_on("py-torch+distributed", when="@:1.4.4")

    # https://github.com/microsoft/torchgeo/issues/1824
    conflicts("py-timm@:0.9.8", when="@1.4.26")
