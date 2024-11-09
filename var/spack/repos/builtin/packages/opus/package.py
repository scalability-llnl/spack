# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Opus(AutotoolsPackage):
    """Opus is a totally open, royalty-free, highly versatile audio codec."""

    homepage = "https://opus-codec.org/"
    url = "http://downloads.xiph.org/releases/opus/opus-1.1.4.tar.gz"

    license("BSD-3-Clause")

    version("1.5.2", sha256="65c1d2f78b9f2fb20082c38cbe47c951ad5839345876e46941612ee87f9a7ce1")
    version("1.5.1", sha256="b84610959b8d417b611aa12a22565e0a3732097c6389d19098d844543e340f85")
    version("1.5", sha256="d8230bbeb99e6d558645aaad25d79de8f4f28fdcc55f8af230050586d62c4f2c")
    version("1.4", sha256="c9b32b4253be5ae63d1ff16eea06b94b5f0f2951b7a02aceef58e3a3ce49c51f")
    version("1.3.1", sha256="65b58e1e25b2a114157014736a3d9dfeaad8d41be1c8179866f144a2fb44ff9d")
    version("1.3", sha256="4f3d69aefdf2dbaf9825408e452a8a414ffc60494c70633560700398820dc550")
    version("1.2.1", sha256="cfafd339ccd9c5ef8d6ab15d7e1a412c054bf4cb4ecbbbcc78c12ef2def70732")
    version("1.2", sha256="77db45a87b51578fbc49555ef1b10926179861d854eb2613207dc79d9ec0a9a9")
    version("1.1.5", sha256="eb84981ca0f40a3e5d5e58d2e8582cb2fee05a022825a6dfe14d14b04eb563e4")
    version("1.1.4", sha256="9122b6b380081dd2665189f97bfd777f04f92dc3ab6698eea1dbb27ad59d8692")
    version("1.1.3", sha256="58b6fe802e7e30182e95d0cde890c0ace40b6f125cffc50635f0ad2eef69b633")
    version("1.1.2", sha256="0e290078e31211baa7b5886bcc8ab6bc048b9fc83882532da4a1a45e58e907fd")
    version("1.1.1", sha256="9b84ff56bd7720d5554103c557664efac2b8b18acc4bbcc234cb881ab9a3371e")
    version("1.1", sha256="b9727015a58affcf3db527322bf8c4d2fcf39f5f6b8f15dbceca20206cbe1d95")
    version("1.0.3", sha256="191a089c92dbc403de6980463dd3604b65beb12d283c607e246c8076363cb49c")
    version("1.0.2", sha256="da615edbee5d019c1833071d69a4782c19f178cf9ca1401375036ecef25cd78a")
    version("1.0.1", sha256="80fa5c3caf2ac0fd68f8a22cce1564fc46b368c773a17554887d0066fe1841ef")
    version("1.0.0", sha256="9250fcc74472d45c1e14745542ec9c8d09982538aefed56962495614be3e0d2d")
    version("0.9.14", sha256="b1cad6846a8f819a141009fe3f8f10c946e8eff7e9c2339cd517bb136cc59eae")
    version("0.9.10", sha256="4e379a98ba95bbbfe9087ef10fdd05c8ac9060b6d695f587ea82a7b43a0df4fe")
    version("0.9.9", sha256="2f62359f09151fa3b242040dc9b4c5b6bda15557c5daea59c8420f1a2ff328b7")
    version("0.9.8", sha256="4aa30d2e0652ffb4a7a22cc8a29c4ce78267626f560a2d9213b1d2d4e618cf36")
    version("0.9.7", sha256="1b69772c31c5cbaa43d1dfa5b1c495fc29712e8e0ff69d6f8ad46459e5c6715f")
    version("0.9.6", sha256="3bfaeb25f4b4a625a0bc994d6fc6f6776a05193f60099e0a99f7530c6b256309")
    version("0.9.5", sha256="53801066fa97329768e7b871fd1495740269ec46802e1c9051aa7e78c6edee5b")
    version("0.9.3", sha256="d916e34c18a396eb7dffc47af754f441af52a290b761e20db9aedb65928c699e")
    version("0.9.2", sha256="6e85c1b57e1d7b7dfe2928bf92586b96b73a9067e054ede45bd8e6d24bd30582")
    version("0.9.1", sha256="206221afc47b87496588013bd4523e1e9f556336c0813f4372773fc536dd4293")
    version("0.9.0", sha256="b2f75c4ac5ab837845eb028413fae2a28754bfb0a6d76416e2af1441ef447649")

    depends_on("c", type="build")  # generated
