# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKombu(PythonPackage):
    """Messaging library for Python."""

    pypi = "kombu/kombu-4.3.0.tar.gz"

    license("BSD-3-Clause")

    version("5.3.5", sha256="30e470f1a6b49c70dc6f6d13c3e4cc4e178aa6c469ceb6bcd55645385fc84b93")
    version("5.3.4", sha256="0bb2e278644d11dea6272c17974a3dbb9688a949f3bb60aeb5b791329c44fadc")
    version("5.3.3", sha256="1491df826cfc5178c80f3e89dd6dfba68e484ef334db81070eb5cb8094b31167")
    version("5.3.2", sha256="0ba213f630a2cb2772728aef56ac6883dc3a2f13435e10048f6e97d48506dbbd")
    version("5.3.1", sha256="fbd7572d92c0bf71c112a6b45163153dea5a7b6a701ec16b568c27d0fd2370f2")
    version("5.3.0", sha256="d084ec1f96f7a7c37ba9e816823bdbc08f0fc7ddb3a5be555805e692102297d8")
    version("5.2.4", sha256="37cee3ee725f94ea8bb173eaab7c1760203ea53bbebae226328600f9d2799610")
    version("5.2.3", sha256="81a90c1de97e08d3db37dbf163eaaf667445e1068c98bfd89f051a40e9f6dbbd")
    version("5.2.2", sha256="0f5d0763fb916808f617b886697b2be28e6bc35026f08e679697fc814b48a608")
    version("5.2.1", sha256="f262a2adc71b53e5b7dad4933bbdee65d8766ca4df6a9043b13edaad2144aaec")
    version("5.1.0", sha256="01481d99f4606f6939cdc9b637264ed353ee9e3e4f62cfb582324142c41a572d")
    version("5.0.2", sha256="f4965fba0a4718d47d470beeb5d6446e3357a62402b16c510b6a2f251e05ac3c")
    version("4.6.11", sha256="ca1b45faac8c0b18493d02a8571792f3c40291cf2bcf1f55afed3d8f3aa7ba74")
    version("4.6.6", sha256="1760b54b1d15a547c9a26d3598a1c8cdaf2436386ac1f5561934bc8a3cbbbd86")
    version("4.5.0", sha256="389ba09e03b15b55b1a7371a441c894fd8121d174f5583bbbca032b9ea8c9edd")
    version("4.3.0", sha256="529df9e0ecc0bad9fc2b376c3ce4796c41b482cf697b78b71aea6ebe7ca353c8")

    depends_on("python@3.7:", type=("build", "run"), when="@5.2.3:")
    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))

    variant("redis", default=False, description="Use redis transport")

    depends_on("py-setuptools", type="build")
    depends_on("py-amqp@2.4", when="@4.3.0:4.5.0", type=("build", "run"))
    depends_on("py-amqp@2.5.0", when="@4.6.0:4.6.3", type=("build", "run"))
    depends_on("py-amqp@2.5.1", when="@4.6.4:4.6.5", type=("build", "run"))
    depends_on("py-amqp@2.5.2:2.5.99", when="@4.6.6:4.6.8", type=("build", "run"))
    depends_on("py-amqp@2.6.0:2.99", when="@4.6.9:5.0.1", type=("build", "run"))
    depends_on("py-amqp@5.0.0:5.0.5", when="@5.0.2:5.0.99", type=("build", "run"))
    depends_on("py-amqp@5.0.6:5.0.8", when="@5.1.0:5.2.2", type=("build", "run"))
    depends_on("py-amqp@5.0.9:5.1.0", when="@5.2.3:5.2.4", type=("build", "run"))
    depends_on("py-amqp@5.1.1:5.1.99", when="@5.3.0:5.3.5", type=("build", "run"))

    depends_on("py-vine", when="@5.1.0:", type=("build", "run"))
    depends_on("py-importlib-metadata@0.18:", type=("build", "run"), when="^python@:3.7")
    depends_on("py-cached-property", type=("build", "run"), when="^python@:3.7")

    depends_on("py-redis@3.4.1:3,4.0.2:", when="+redis", type=("build", "run"))
    depends_on("py-backports-zoneinfo@0.2.1:", when="^python@:3.8", type=("build", "run"))
