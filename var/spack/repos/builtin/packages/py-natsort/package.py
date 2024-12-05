# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNatsort(PythonPackage):
    """Simple yet flexible natural sorting in Python."""

    homepage = "https://github.com/SethMMorton/natsort"
    url = "https://github.com/SethMMorton/natsort/archive/5.2.0.zip"

    license("MIT")

    version("8.4.0", sha256="e42c6730e93382f743e09eb24b8d48034d81d089bd259183a88e2c4190e3db90")
    version("8.2.0", sha256="0ce4562913d89a6f413fc68c9937cb0fc32be1268f73ac4b68e2646aeae458c6")
    version("7.1.1", sha256="ada96d9ca0db0d44b891718ff7baff5ac34cf5b6d9def356c0f7a8ea67ae2113")
    version("7.1.0", sha256="c3de32c8e5e91cf4f2dd1655b4c167ca4676cc28ce397050fc8d229582a71f0d")
    version("7.0.1", sha256="1a422a344d089f7a2acba788087ca6253ca47a544bda677721f99516cdfd8668")
    version("7.0.0", sha256="0a5ff72173091e69d67c4711616713ddf090980ab11cbe4a1f269be3e697678a")
    version("6.2.1", sha256="f14b62b37c78387e38cf1421867e8b5aed849b67d46f2351ee187ef4e9e814e1")
    version("6.2.0", sha256="4a9587bfd3559900b64727be380236160e4c5a16b5a3643f5001d0bcfb0d63eb")
    version("6.1.0", sha256="51f1ef44cbe4537fdb70ec55f3584f70ea2070fc37915239ecb0595c1ff055f9")
    version("6.0.0", sha256="39c46bf2f4dc17fd0ea6210932eeaf7c806cac79dd354295d70e9b44f75a096b")
    version("5.5.0", sha256="62e8fa3d7697b922e1d786b531a68bd07a7f6ba10a3bdf79a0bf52ef2cdccc41")
    version("5.4.1", sha256="077ce724aa0c27df2bbcaef9c9f096c99ccd62eb4fffe68512c46edc3b714452")
    version("5.2.0", sha256="0ae15082842e8a3598750b4bbaa4f7c138caf004e59c7040429d56bf9e9631bd")
    version("5.1.1", sha256="6467eeca268d9accb2e3149acace49649f865b0051a672006a64b20597f04561")
    version("5.1.0", sha256="79279792cc97a0005b2075ed2bc9b8a3e25e5edffe43ee2fb26b116283f5dab4")
    version("5.0.3", sha256="408f6fa87f6bbe3e09b255286d4db7b678bf22d6a5cd1651d05bfc1f99792a2e")
    version("5.0.2", sha256="6315d94b6651edd9bf1e29cfd513a0349ec46a38ed38d33121a11d5162dbe556")
    version("5.0.1", sha256="fe915cd4ddc90182947758b77873dda42935d5493819df8439f2daef01ffaacb")
    version("5.0.0", sha256="b46b3569ac69e8f4a88f1a479d108872857538c7564226c32df1fd75e809c240")
    version("4.0.4", sha256="14e5ddaf689de2f5ac33aa7963554fa2944b019f526ece1036d74fe60528531b")
    version("4.0.3", sha256="8824792d7ebc37a57010e1ba301244653f8655ea20ddab6b0d546cf1d9ffedda")
    version("4.0.1", sha256="1c1d29150938ca71f0943363a06765dbb2cea01f9c4d760ba880cc65f39baba0")

    depends_on("py-setuptools", type=("build"))
