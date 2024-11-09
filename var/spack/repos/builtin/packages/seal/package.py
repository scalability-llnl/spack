# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Seal(CMakePackage):
    """Microsoft SEAL is an easy-to-use open-source (MIT licensed)
    homomorphic encryption library developed by the Cryptography and Privacy
    Research Group at Microsoft. Microsoft SEAL is written in modern standard
    C++ and is easy to compile and run in many different environments. For
    more information about the Microsoft SEAL project, see sealcrypto.org."""

    homepage = "https://github.com/microsoft/SEAL"
    url = "https://github.com/microsoft/SEAL/archive/refs/tags/v3.7.1.tar.gz"

    maintainers("wohlbier")

    license("MIT")

    version("4.1.1", sha256="af9bf0f0daccda2a8b7f344f13a5692e0ee6a45fea88478b2b90c35648bf2672")
    version("3.7.1", sha256="6737177bfb582cc1a2863ef1e96cc6c39b119257e7192981a3190eb79e0fcfd3")
    version("3.7.0", sha256="06ea835d6c9cdbbc4edb72a8db4bd4b1115995f075774043b9f31938d0624543")
    version("3.6.6", sha256="85a63188a5ccc8d61b0adbb92e84af9b7223fc494d33260fa17a121433790a0e")
    version("3.6.5", sha256="77bfcb4a8b785206c419cdf7aff8c200250691518eeddc958f874d1f567b2872")
    version("3.6.4", sha256="7392574fe3b757d5ced8cc973b23a7b69be0cd35b6e778b3c2447598e9ece5b3")
    version("3.6.3", sha256="aeecdf79afba5f83d1828b3525760c04e52928614038e9a860773943d5d14558")
    version("3.6.2", sha256="1e2a97deb1f5b543640fc37d7b4737cab2a9849f616c13ff40ad3be4cf29fb9c")
    version("3.6.1", sha256="e399c0df7fb60ad450a0ccfdc81b99d19308d0fc1f730d4cad4748dfb2fdb516")
    version("3.6.0", sha256="79c0e45bf301f4577a7633b14e8b26e37eefc89fd4f6a29d13f87e5f22a372ad")
    version("3.5.9", sha256="23bf3bf7ae1dae5dae271244a5baa66fa01856c52e263fe8368c3a40f2399fc7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
