# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Evtgen(CMakePackage):
    """EvtGen is a Monte Carlo event generator that simulates
    the decays of heavy flavour particles, primarily B and D mesons."""

    homepage = "https://evtgen.hepforge.org/"
    url = "https://evtgen.hepforge.org/downloads?f=EvtGen-02.00.00.tar.gz"

    tags = ["hep"]

    maintainers("vvolkl")

    version("02.02.03", sha256="b642700b703190e3304edb98ff464622db5d03c1cfc5d275ba4a628227d7d6d0")
    version("02.02.02", sha256="e543d1213cd5003124139d0dc7eee9247b0b9d44154ff8a88bac52ba91c5dfc9")
    version("02.02.01", sha256="1fcae56c6b27b89c4a2f4b224d27980607442185f5570e961f6334a3543c6e77")
    version("02.02.00", sha256="0c626e51cb17e799ad0ffd0beea5cb94d7ac8a5f8777b746aa1944dd26071ecf")
    version("02.00.00", sha256="02372308e1261b8369d10538a3aa65fe60728ab343fcb64b224dac7313deb719")

    depends_on("cxx", type="build")  # generated

    variant("pythia8", default=True, description="Build with pythia8")
    variant("tauola", default=False, description="Build with tauola")
    variant("photos", default=False, description="Build with photos")
    variant("sherpa", default=False, description="build with sherpa")
    variant("hepmc3", default=False, description="Link with hepmc3 (instead of hepmc)")

    patch("evtgen-2.0.0.patch", when="@02.00.00 ^pythia8@8.304:")

    depends_on("hepmc", when="~hepmc3")
    depends_on("hepmc3", when="+hepmc3")
    depends_on("pythia8@:8.309", when="@:02.02.00 +pythia8")
    depends_on("pythia8", when="+pythia8")
    depends_on("tauola~hepmc3", when="+tauola~hepmc3")
    depends_on("photos~hepmc3", when="+photos~hepmc3")
    depends_on("tauola+hepmc3", when="+tauola+hepmc3")
    depends_on("photos+hepmc3", when="+photos+hepmc3")
    depends_on("sherpa@2:", when="@02.02.01: +sherpa")
    depends_on("sherpa@:2", when="@:02 +sherpa")

    conflicts(
        "^pythia8+evtgen",
        when="+pythia8",
        msg="Building pythia with evtgen bindings and "
        "evtgen with pythia bindings results in a circular dependency "
        "that cannot be resolved at the moment! "
        "Use evtgen+pythia8^pythia8~evtgen.",
    )

    @property
    def root_cmakelists_dir(self):
        # deal with inconsistent intermediate folders of tarballs
        # 02.00.00 only has 'R02-00-00'
        # but 02.02.00 has 'EvtGen/R02-02-00'
        if self.spec.satisfies("@02.02.00:"):
            return "R" + str(self.version).replace(".", "-")
        else:
            return ""

    def cmake_args(self):
        args = []

        args.append(self.define_from_variant("EVTGEN_PYTHIA", "pythia8"))
        args.append(self.define_from_variant("EVTGEN_TAUOLA", "tauola"))
        args.append(self.define_from_variant("EVTGEN_PHOTOS", "photos"))
        args.append(self.define_from_variant("EVTGEN_SHERPA", "sherpa"))
        args.append(self.define_from_variant("EVTGEN_HEPMC3", "hepmc3"))

        return args

    def patch(self):
        # gcc on MacOS doesn't recognize `-shared`, should use `-dynamiclib`;
        # the `-undefined dynamic_lookup` flag enables weak linking on Mac
        # Patch taken from CMS recipe:
        # https://github.com/cms-sw/cmsdist/blob/IB/CMSSW_12_1_X/master/evtgen.spec#L48
        if not self.spec.satisfies("%gcc platform=darwin"):
            return

        filter_file("-shared", "-dynamiclib -undefined dynamic_lookup", "make.inc")

    def setup_run_environment(self, env):
        env.set("EVTGEN", self.prefix.share)
