# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Enchant(AutotoolsPackage):
    """Enchant is a library (and command-line program) that wraps a
    number of different spelling libraries and programs with a
    consistent interface."""

    homepage = "https://rrthomas.github.io/enchant/"
    url = "https://github.com/rrthomas/enchant/releases/download/v2.8.2/enchant-2.8.2.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.8.2", sha256="8f19535adb5577b83b00e02f330fe9b9eb40dd21f19e2899636fc4d3a7696375")
    version("2.8.1", sha256="ff79de470b8eb16f53849dc49f2bce8ca4eb7decabfc1349716fe12616e52f4e")
    version("2.8.0", sha256="c57add422237b8a7eed116a9a88d8be4f7b9281778fa36f03e1f2c051ecb0372")
    version("2.7.3", sha256="fe6ad4cbe8c71b9384ffdef962be52d4d2bd5ebfb6351435bb390543d4f78b1e")
    version("2.7.2", sha256="7cc3400a6657974a740b6e3c2568e2935c70e5302f07fadb2095366b75ecad6f")
    version("2.7.1", sha256="a1cb8239095d6b0bd99ba2dd012a1402cef1a194f5de1b7214bd528676a65229")
    version("2.7.0", sha256="2a073dc6ebe753196c0674a781ccf321bed25d1c6e43bffb97e2c92af420952c")
    version("2.6.9", sha256="d9a5a10dc9b38a43b3a0fa22c76ed6ebb7e09eb535aff62954afcdbd40efff6b")
    version("2.6.8", sha256="f565923062c77f3d58846f0558d21e6d07ca4a488c58812dfdefb35202fac7ae")
    version("2.6.7", sha256="a1c2e5b59acca000bbfb24810af4a1165733d407f2154786588e076c8cd57bfc")

    version("2.2.7", sha256="1b22976135812b35cb5b8d21a53ad11d5e7c1426c93f51e7a314a2a42cab3a09")
    version("2.2.6", sha256="8048c5bd26190b21279745cfecd05808c635bc14912e630340cd44a49b87d46d")
    version("2.2.5", sha256="ee8a663295c0e039b05d418af065ebcba9e539f785531e552e908030bec48164")
    version("2.2.4", sha256="f5d6b689d23c0d488671f34b02d07b84e408544b2f9f6e74fb7221982b1ecadc")
    version("2.2.3", sha256="abd8e915675cff54c0d4da5029d95c528362266557c61c7149d53fa069b8076d")
    version("2.2.2", sha256="661e0bd6e82deceb97fc94bea8c6cdbcd8ff631cfa9b7a8196de2e2aca13f54b")
    version("2.2.1", sha256="97f2e617b34c66a645b9cfebe33700456c31ca2f4677eb827b364c0d9a7f4e5e")
    version("2.2.0", sha256="2f91ea06992c923ac9b72c9c6d0a7c855aef1e9a4991350d83236723c8412467")
    version("2.1.3", sha256="086f37cdecd42eacd0e1dc291f5410d9ca2c5ed2cd9cd9367729e3d2d18a8550")
    version("2.1.2", sha256="039563bbb7340f320bd9237dac92303b3e7768152b08fc0d554d6957ae7183d8")
    version("2.1.1", sha256="5fad0a1e82ddfed91647e93da5955fc76249760fd51865648a36074dc97d526c")
    version("2.1.0", sha256="2cdda2d9edb62ad895c34be35c598d56ac5b9b9298f3dfdaa2b40a1914d1db7e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("hunspell", default=True, description="Enables hunspell backend")

    depends_on("glib")
    depends_on("aspell")
    depends_on("hunspell", when="+hunspell")
    depends_on("groff", type="build", when="@2.6.7:")

    def configure_args(self):
        spec = self.spec
        args = ["--with-aspell", "--with-aspell-dir={0}".format(spec["aspell"].prefix)]

        args += self.with_or_without("hunspell")
        if spec.satisfies("+hunspell"):
            args.append("--with-hunspell-dir={0}".format(spec["hunspell"].prefix))

        return args
