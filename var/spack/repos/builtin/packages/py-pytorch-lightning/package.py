# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytorchLightning(PythonPackage):
    """PyTorch Lightning is the lightweight PyTorch wrapper for ML researchers."""

    homepage = "https://github.com/Lightning-AI/lightning"
    pypi = "pytorch-lightning/pytorch-lightning-1.2.10.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version("2.0.7", sha256="4e6bc1e1f7b0c69016ea2fe0616b18fa62bd3d8661c7ff02c11d317746cfc5f5")
    version("2.0.0", sha256="632dec9af8036f726904e691c505d7650658ef0f4054a062c9e6a940ca09dfd8")
    version("1.9.4", sha256="188a7f4468acf23512e7f4903253d86fc7929a49f0c09d699872e364162001e8")
    version("1.9.3", sha256="479164caea190d49ee2a218eef7e001888be56db912b417639b047e8f9ca8a07")
    version("1.9.2", sha256="e60303e258457ccf7ec37c46a616892691fe3fbb23ab12f5c02b8018f03bf223")
    version("1.9.1", sha256="45b1031f1bdf68d9350fa42e5ec01ff8492d5badda9685a2ae48e5fd8598510a")
    version("1.9.0", sha256="5b75fe936d16ef86dae22ea1cb0a73db281605cade682c0ef44e6508a99a0b37")
    version("1.8.6", sha256="c4af783579a1528e07f40dd9bd0128c162bbbcf74fe1ce4292fec63fa7e76ada")
    version("1.8.5", sha256="1c6fbd86923e73877521cdd21927f4da1d460719bbca2e04aec3d6b88d60a783")
    version("1.8.4", sha256="c2771f966fc1b909cdfd1d603a87b8c84a3d5ff7aacf35b2c0260f697ec0c8be")
    version("1.8.3", sha256="c12293da19810a08e4f81a40145760fb29514449ef5d294fa1ef741553cdf217")
    version("1.8.2", sha256="480f3396cd63888c4e5ec2f21c02fe662a2b035d9634e6f31fcf1197a36ebd15")
    version("1.8.1", sha256="5b60e5eb84dd16ee8dc408286f0074ab475bed385b09a702d678ccbde91e4818")
    version("1.8.0", sha256="deff9bc7978ecebc8f45e881adef65dc8d9f4554e88c3b064f80587f32ab158d")
    version("1.7.7", sha256="27c2dd01a18db2415168e3fa3775ccb5a1fa1e2961a50439ad9365507fe9d4ae")
    version("1.7.6", sha256="93266c83f8340c100e41b3777bbab26dd2c20b4df3deccce3b8a15652326b9c8")
    version("1.7.5", sha256="a5838ae990f0eef9a894fa863be3bc1f5594d2abba7848fb21317ba3e885d7cd")
    version("1.7.4", sha256="d80df235228a8f6d6b77df4bfa34b3d667d734bd40e960bb4ca553a2746523eb")
    version("1.7.3", sha256="605ab313e54992261db74df4a6a6d4d556f319ea8a08eff2f30d80e8b898eb14")
    version("1.7.2", sha256="76e4d1af70721fc9a294641668c905e2db76e866f7bf07a5e37f72fa3cb87141")
    version("1.7.1", sha256="bdf4815431e15581422154bafd2506f44d42baec8772b9eb36b9638436aa3728")
    version("1.7.0", sha256="f3be1500e3ba9ff06c4b8f74d66f02757a5ae73b4cd2f63f47137c501a0400e2")
    version("1.6.5", sha256="8d521f2619b9db2ada5bbaf9713330d01460e75a11e4bc0bc2ca25fd37c47c57")
    version("1.6.4", sha256="5459f2c3e67676ec59e94576d1499e9559d214e7df41eadd135db64b4ccf54b9")
    version("1.6.3", sha256="beb1f36a6dae91f5fef0959a04af1092dff4f3f4d99c20f0e033f84e615903e3")
    version("1.6.2", sha256="ccb5e8593837afc9ecf914ee66bf171ee0e08a8d6673531a617b0a61863a9611")
    version("1.6.1", sha256="280b9c7f84f9a6b6d2efb91c7b3caad50031e318d37cfe052f3047faf1f0a2de")
    version("1.6.0", sha256="1ab6f15750862cfbac48ad7be420050c8c353a060da7c2575f9e267158a33d42")
    version("1.5.3", sha256="a206169a0c4356366a7edadb5ebd2f38e9a611ff78265ce93b767662682f5620")
    version("1.4.1", sha256="1d1128aeb5d0e523d2204c4d9399d65c4e5f41ff0370e96d694a823af5e8e6f3")
    version("1.4.0", sha256="6529cf064f9dc323c94f3ce84b56ee1a05db1b0ab17db77c4d15aa36e34da81f")
    version("1.3.8", sha256="60b0a3e464d394864dae4c8d251afa7aa453644a19bb7672f5ee400343cdf7b0")
    version("1.2.10", sha256="2d8365e30ded0c20e73ce6e5b6028478ae460b8fd33727df2275666df005a301")

    # src/pytorch_lightning/__setup__.py
    depends_on("python@3.8:", when="@2:", type=("build", "run"))
    # https://github.com/Lightning-AI/pytorch-lightning/pull/20081
    depends_on("py-setuptools", type=("build", "run"))

    # requirements/pytorch/base.txt
    depends_on("py-numpy@1.17.2:", when="@1.3:", type=("build", "run"))
    depends_on("py-numpy@1.16.6:", when="@:1.2", type=("build", "run"))
    depends_on("py-torch@1.11:", when="@2:", type=("build", "run"))
    depends_on("py-torch@1.10:", when="@1.9:", type=("build", "run"))
    depends_on("py-torch@1.9:", when="@1.7:", type=("build", "run"))
    depends_on("py-torch@1.8:", when="@1.6:", type=("build", "run"))
    depends_on("py-torch@1.6:", when="@1.4:1.5", type=("build", "run"))
    depends_on("py-torch@1.4:", when="@:1.3", type=("build", "run"))
    depends_on("py-tqdm@4.57.0:", when="@1.6.3:", type=("build", "run"))
    depends_on("py-tqdm@4.41.0:", when="@:1.6.2", type=("build", "run"))
    depends_on("py-pyyaml@5.4:", when="@1.6:", type=("build", "run"))
    depends_on("py-pyyaml@5.1:", when="@1.4:1.5", type=("build", "run"))
    depends_on("py-pyyaml@5.1:5.4.1", when="@1.3", type=("build", "run"))
    depends_on("py-pyyaml@5.1:5.3,5.5:", when="@:1.2", type=("build", "run"))
    depends_on("py-fsspec@2021.06.1:+http", when="@1.8:", type=("build", "run"))
    depends_on("py-fsspec@2021.05.0:2021.05,2021.06.1:+http", when="@1.3:", type=("build", "run"))
    depends_on("py-fsspec@0.8.1:+http", when="@:1.2", type=("build", "run"))
    depends_on("py-torchmetrics@0.7:", when="@1.7:", type=("build", "run"))
    depends_on("py-torchmetrics@0.4.1:", when="@1.5:", type=("build", "run"))
    depends_on("py-torchmetrics@0.4.0:", when="@1.4", type=("build", "run"))
    depends_on("py-torchmetrics@0.2.0:", when="@1.3", type=("build", "run"))
    depends_on("py-torchmetrics@0.2.0", when="@:1.2", type=("build", "run"))
    depends_on("py-packaging@17.1:", when="@1.9:", type=("build", "run"))
    depends_on("py-packaging@17.0:", when="@1.3:", type=("build", "run"))
    depends_on("py-packaging", when="@:1.2", type=("build", "run"))
    depends_on("py-typing-extensions@4.0.0:", when="@1.6:", type=("build", "run"))
    depends_on("py-typing-extensions", when="@1.4:1.5", type=("build", "run"))
    depends_on("py-lightning-utilities@0.7:", when="@2:", type=("build", "run"))
    depends_on("py-lightning-utilities@0.6.0.post0:", when="@1.9.1:", type=("build", "run"))
    depends_on("py-lightning-utilities@0.4.2:", when="@1.9.0", type=("build", "run"))
    depends_on("py-lightning-utilities@0.3,0.4.1:", when="@1.8.4:1.8", type=("build", "run"))
    depends_on("py-lightning-utilities@0.3:", when="@1.8.0:1.8.3", type=("build", "run"))

    # Historical dependencies
    depends_on("py-lightning-lite@1.8.0", when="@1.8.0", type=("build", "run"))
    depends_on("py-future@0.17.1:", when="@:1.5", type=("build", "run"))
    depends_on("pil@:8.2,8.3.1:", when="@1.3", type=("build", "run"))
    depends_on("py-protobuf@:3.20.1", when="@1.6.4:1.6", type="build")
    depends_on("py-pydeprecate@0.3.1:", when="@1.6.4:1.7", type=("build", "run"))
    depends_on("py-pydeprecate@0.3.1:0.3", when="@1.6:1.6.3", type=("build", "run"))
    depends_on("py-pydeprecate@0.3.1", when="@1.4:1.5", type=("build", "run"))
    depends_on("py-pydeprecate@0.3.0", when="@1.3", type=("build", "run"))
    depends_on("py-tensorboardx@2.2:", when="@1.8.3:1.8", type=("build", "run"))
    depends_on("py-tensorboard@2.9.1:", when="@1.7:1.8.2", type=("build", "run"))
    depends_on("py-tensorboard@2.2.0:", when="@1.5:1.6", type=("build", "run"))
    depends_on("py-tensorboard@2.2.0:2.4,2.5.1:", when="@:1.4", type=("build", "run"))

    # https://github.com/Lightning-AI/lightning/issues/16637
    conflicts("^py-torch~distributed", when="@1.9.0")
    # https://github.com/Lightning-AI/lightning/issues/15494
    conflicts("^py-torch~distributed", when="@1.8.0")
    # https://github.com/Lightning-AI/lightning/issues/10348
    conflicts("^py-torch~distributed", when="@1.5.0:1.5.2")
