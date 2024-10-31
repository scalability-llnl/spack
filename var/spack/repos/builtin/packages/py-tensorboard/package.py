# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTensorboard(PythonPackage):
    """TensorBoard is a suite of web applications for inspecting and understanding
    your TensorFlow runs and graphs."""

    homepage = "https://github.com/tensorflow/tensorboard"
    url = "https://files.pythonhosted.org/packages/py3/t/tensorboard/tensorboard-2.9.1-py3-none-any.whl"
    list_url = "https://pypi.org/simple/tensorboard/"

    # Requires tensorflow
    skip_modules = ["tensorboard.summary._tf"]

    maintainers("aweits")

    license("Apache-2.0")

    version("2.17.0", sha256="859a499a9b1fb68a058858964486627100b71fcb21646861c61d31846a6478fb")
    version("2.16.2", sha256="9f2b4e7dad86667615c0e5cd072f1ea8403fc032a299f0072d6f74855775cc45")
    version("2.16.1", sha256="928b62567911a8eeb2ebeb7482a9e4599b35f6713a6f2c56655259c18a139569")
    version("2.16.0", sha256="263b909a2009cb3a79daa6abe64c1785cc317c25a54e4db2fecb6429ffc54c58")
    version("2.15.2", sha256="a6f6443728064d962caea6d34653e220e34ef8df764cb06a8212c17e1a8f0622")
    version("2.15.1", sha256="c46c1d1cf13a458c429868a78b2531d8ff5f682058d69ec0840b0bc7a38f1c0f")
    version("2.15.0", sha256="c05b4d02a3a9fd4bd6c25265087d52b49b790a871ddf98f4fb32fe97cbbc7ad0")
    version("2.14.1", sha256="3db108fb58f023b6439880e177743c5f1e703e9eeb5fb7d597871f949f85fd58")
    version("2.14.0", sha256="3667f9745d99280836ad673022362c840f60ed8fefd5a3e30bf071f5a8fd0017")
    version("2.13.0", sha256="ab69961ebddbddc83f5fa2ff9233572bdad5b883778c35e4fe94bf1798bd8481")
    version("2.12.3", sha256="b4a69366784bc347e02fbe7d847e01896a649ca52f8948a11005e205dcf724fb")
    version("2.12.2", sha256="811ab0d27a139445836db9fd4f974424602c3dce12379364d379bcba7c783a68")
    version("2.12.1", sha256="58f1c2a25b4829b9c48d2b1ec951dedc9325dcd1ea4b0f601d241d2887d0ed65")
    version("2.12.0", sha256="3cbdc32448d7a28dc1bf0b1754760c08b8e0e2e37c451027ebd5ff4896613012")
    version("2.11.2", sha256="cbaa2210c375f3af1509f8571360a19ccc3ded1d9641533414874b5deca47e89")
    version("2.11.1", sha256="0c7529f3f43691e8cc2ece8e564c2e103c51ade317c6af626d415239b5088018")
    version("2.11.0", sha256="a0e592ee87962e17af3f0dce7faae3fbbd239030159e9e625cce810b7e35c53d")
    version("2.10.1", sha256="fb9222c1750e2fa35ef170d998a1e229f626eeced3004494a8849c88c15d8c1c")
    version("2.10.0", sha256="76c91a5e8959cd2208cc32cb17a0cb002badabb66a06ac2af02a7810f49a59e3")
    version("2.9.1", sha256="baa727f791776f9e5841d347127720ceed4bbd59c36b40604b95fb2ae6029276")
    version("2.9.0", sha256="bd78211076dca5efa27260afacfaa96cd05c7db12a6c09cc76a1d6b2987ca621")
    version("2.8.0", sha256="65a338e4424e9079f2604923bdbe301792adce2ace1be68da6b3ddf005170def")
    version("2.7.0", sha256="239f78a4a8dff200ce585a030c787773a8c1184d5c159252f5f85bac4e3c3b38")
    version("2.6.0", sha256="f7dac4cdfb52d14c9e3f74585ce2aaf8e6203620a864e51faf84988b09f7bbdb")
    version("2.5.0", sha256="e167460085b6528956b33bab1c970c989cdce47a6616273880733f5e7bde452e")
    version("2.4.1", sha256="7b8c53c396069b618f6f276ec94fc45d17e3282d668979216e5d30be472115e4")
    version("2.4.0", sha256="cde0c663a85609441cb4d624e7255fd8e2b6b1d679645095aac8a234a2812738")
    version("2.3.0", sha256="d34609ed83ff01dd5b49ef81031cfc9c166bba0dabd60197024f14df5e8eae5e")
    version("2.2.0", sha256="bb6bbc75ad2d8511ba6cbd49e4417276979f49866e11841e83da8298727dbaed")

    with default_args(type=("build", "run")):
        depends_on("python@3.9:", when="@2.14:")
        depends_on("python@3.8:", when="@2.12:")
        depends_on("py-absl-py@0.4:")
        depends_on("py-grpcio@1.48.2:", when="@2.12:")
        depends_on("py-grpcio@1.24.3:", when="@2.3:")
        depends_on("py-grpcio@1.23.3:", when="@2.2")
        depends_on("py-markdown@2.6.8:")
        depends_on("py-numpy@1.12.0:")
        # https://github.com/tensorflow/tensorboard/pull/6871
        depends_on("py-numpy@:1")
        # https://github.com/tensorflow/tensorboard/pull/5138
        depends_on("py-numpy@:1.23", when="@:2.5")
        depends_on("py-protobuf@3.19.6:4", when="@2.17:")
        depends_on("py-protobuf@3.19.6:", when="@2.15.2:2.16")
        depends_on("py-protobuf@3.19.6:4.23", when="@2.12:2.15.1")
        depends_on("py-protobuf@3.9.2:3", when="@2.11")
        depends_on("py-protobuf@3.9.2:3.19", when="@2.9:2.10")
        depends_on("py-protobuf@3.6.0:3.19", when="@:2.8")
        depends_on("py-setuptools@41.0.0:")
        depends_on("py-six@1.10.0:", when="@:2.4,2.14:")
        depends_on("py-tensorboard-data-server@0.7", when="@2.12:")
        depends_on("py-tensorboard-data-server@0.6", when="@2.5:2.11")
        depends_on("py-werkzeug@1.0.1:", when="@2.9:")
        depends_on("py-werkzeug@0.11.15:")

        # Historical dependencies
        depends_on("py-google-auth@1.6.3:2", when="@2.7:2.15")
        depends_on("py-google-auth@1.6.3:1", when="@:2.6")
        depends_on("py-google-auth-oauthlib@0.5:1", when="@2.15")
        depends_on("py-google-auth-oauthlib@0.5:1.0", when="@2.12.1:2.14")
        depends_on("py-google-auth-oauthlib@0.4.1:0.4", when="@:2.12.0")
        depends_on("py-requests@2.21.0:2", when="@:2.15")
        depends_on("py-tensorboard-plugin-wit@1.6.0:", when="@:2.13")

    conflicts("^py-protobuf@4.24.0")
