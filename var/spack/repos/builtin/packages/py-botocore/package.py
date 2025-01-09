# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBotocore(PythonPackage):
    """Low-level, data-driven core of boto 3."""

    homepage = "https://github.com/boto/botocore"
    pypi = "botocore/botocore-1.13.44.tar.gz"

    version("1.34.162", sha256="adc23be4fb99ad31961236342b7cbf3c0bfc62532cd02852196032e8c0d682f3")
    version("1.34.44", sha256="b0f40c54477e8e0a5c43377a927b8959a86bb8824aaef2d28db7c9c367cdefaa")
    version("1.31.41", sha256="4dad7c5a5e70940de54ebf8de3955450c1f092f43cacff8103819d1e7d5374fa")
    version("1.29.84", sha256="a36f7f6f8eae5dbd4a1cc8cb6fc747f6315500541181eff2093ee0529fc8e4bc")
    version("1.29.76", sha256="c2f67b6b3f8acf2968eafca06526f07b9fb0d27bac4c68a635d51abb675134a7")
    version("1.29.56", sha256="ca4d6403d745218270a20d9ca3ca9a33e3ad2fabb59a96ed8d6e1a824b274c86")
    version("1.29.26", sha256="f71220fe5a5d393c391ed81a291c0d0985f147568c56da236453043f93727a34")
    version("1.28.5", sha256="f322d7b62163219ffeb787a116d318273dfb7243c3b49d95f5bfff8daa1df4e0")
    version("1.27.96", sha256="fc0a13ef6042e890e361cf408759230f8574409bb51f81740d2e5d8ad5d1fbea")
    version("1.27.59", sha256="eda4aed6ee719a745d1288eaf1beb12f6f6448ad1fa12f159405db14ba9c92cf")
    version("1.26.10", sha256="5df2cf7ebe34377470172bd0bbc582cf98c5cbd02da0909a14e9e2885ab3ae9c")
    version("1.25.13", sha256="d99381bda4eed5896b74f6250132e2e6484c2d6e406b1def862113ffdb41c523")
    version("1.24.46", sha256="89a203bba3c8f2299287e48a9e112e2dbe478cf67eaac26716f0e7f176446146")
    version("1.23.54", sha256="4bb9ba16cccee5f5a2602049bc3e2db6865346b2550667f3013bdf33b0a01ceb")
    version("1.22.12", sha256="fc59b55e8c5dde64b017b2f114c25f8cce397b667e812aea7eafb4b59b49d7cb")
    version("1.21.65", sha256="6437d6a3999a189e7d45b3fcd8f794a46670fb255ae670c946d3f224caa8b46a")
    version("1.21.12", sha256="8710d03b9de3e3d94ed410f3e83809ca02050b091100d68c22ff7bf986f29fb6")
    version("1.20.112", sha256="d0b9b70b6eb5b65bb7162da2aaf04b6b086b15cc7ea322ddc3ef2f5e07944dcf")
    version("1.20.27", sha256="4477803f07649f4d80b17d054820e7a09bb2cb0792d0decc2812108bc3759c4a")
    version("1.19.63", sha256="d3694f6ef918def8082513e5ef309cd6cd83b612e9984e3a66e8adc98c650a92")
    version("1.19.52", sha256="dc5ec23deadbe9327d3c81d03fddf80805c549059baabd80dea605941fe6a221")
    version("1.13.50", sha256="765a5c637ff792239727c327b221ed5a4d851e9f176ce8b8b9eca536425c74d4")
    version("1.13.44", sha256="a4409008c32a3305b9c469c5cc92edb5b79d6fcbf6f56fe126886b545f0a4f3f")
    version("1.13.38", sha256="15766a367f39dba9de3c6296aaa7da31030f08a0117fd12685e7df682d8acee2")
    version("1.12.253", sha256="3baf129118575602ada9926f5166d82d02273c250d0feb313fc270944b27c48b")
    version("1.12.169", sha256="25b44c3253b5ed1c9093efb57ffca440c5099a2d62fa793e8b6c52e72f54b01e")

    depends_on("py-setuptools", type="build")
    depends_on("py-jmespath@0.7.1:0", type=("build", "run"), when="@:1.23")
    depends_on("py-jmespath@0.7.1:1", type=("build", "run"))
    depends_on("py-docutils@0.10:0.15", type=("build", "run"), when="@:1.17")
    depends_on("py-python-dateutil@2.1:2", type=("build", "run"))
    depends_on("py-urllib3@1.20:1.25", type=("build", "run"), when="@:1.14.11")
    depends_on("py-urllib3@1.20:1.25", type=("build", "run"), when="@1.14.12:1.18")
    depends_on("py-urllib3@1.25.4:1.25", type=("build", "run"), when="@1.19.0:1.19.15")
    depends_on("py-urllib3@1.25.4:1.26", type=("build", "run"), when="@1.19.16:1.31.61")
    depends_on("py-urllib3@1.25.4:1.26", type=("build", "run"), when="@1.31.62: ^python@:3.9")
    depends_on(
        "py-urllib3@1.25.4:2.0", type=("build", "run"), when="@1.31.62:1.34.62 ^python@3.10:"
    )
    depends_on(
        "py-urllib3@1.25.4:2.1,2.2.1:2", type=("build", "run"), when="@1.34.63: ^python@3.10:"
    )
