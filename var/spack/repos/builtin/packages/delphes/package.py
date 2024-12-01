# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Delphes(CMakePackage):
    """A high energy physics framework for fast simulation
    of a generic collider experiment.
    """

    homepage = "https://cp3.irmp.ucl.ac.be/projects/delphes"
    git = "https://github.com/delphes/delphes.git"
    url = "http://cp3.irmp.ucl.ac.be/downloads/Delphes-3.4.2.tar.gz"

    tags = ["hep"]

    maintainers("drbenmorgan", "vvolkl", "selvaggi")

    license("CC-BY-SA-4.0")

    version("master", branch="master")
    version("3.5.0", sha256="37685b945ef43aab09217d70b0ac7f9c5d3c2c27cf3b3f8d64c4e6eb5c5fd9aa")
    version("3.4.2", sha256="d46a7c5474de650befdb89377115feee31f1743107ceb3d8da699be9d48c097b")
    version("3.4.1", sha256="4b5a2aeac326643f45b6d45c39ba2302e323eeb86d8cb58843c6e73949b1208a")
    version("3.4.0", sha256="c0f9500663a0c3a5c1eddcee598a67b5bcfc9318303195c6cacc0590b4023fa1")
    version("3.3.3", sha256="404de818a6b7852b01187ccf598d8ac19d308b9361f128751ef003cde248ff00")
    version("3.3.2", sha256="b8dc066e480678bb50ea0b68d157c391d47f66c084bda602d3d498538e682622")
    version("3.3.1", sha256="d8fcaa9711b5892ba24b2c7be38158dedbe552b159961f9d29887b2cc7eb2e83")
    version("3.3.0", sha256="3fcdcd31827227ff3d0d56df908b12289c67aa6d01c5725a2a9441c200f3966f")
    version("3.2.0", sha256="3510b0852c750120425f9b014cada25d48b90b29c512b974a9ffbd7aa80ccde4")
    version("3.1.2", sha256="edfccc47f7666d3607e86db82c6c79cfb10716423b496f0c0bdd4060b717ea1d")
    version("3.1.1", sha256="c4128575b6103239ca13de392f47da2eaedfd93c3789b1ecb32eea09da3408e4")
    version("3.1.0", sha256="c37b07aea3e57b39d34bf07f8afd209e36b278cf3792cd6e970d96a2c3b114eb")
    version("3.0.12", sha256="55b4cf25f681c75457e33ad4ee615b9ab66317216675ca5f466ab256aa85cd16")
    version("3.0.11", sha256="870921c8070762dc56aa0b8e0e07d1756584399e8740c848d330fc0fcb5e0604")
    version("3.0.10", sha256="872a386baf298cab14e42aac198dbf7184a2ab7c28ee712448060e1dec078d34")
    version("3.0.9", sha256="d12592fe66062a51e513a8d070fe1f49b672a4328bad2aa5cdb682937391a639")
    version("3.0.8", sha256="8ab146ca3c163932ab21df9168d8ca86dbb1c3494b7bdc3e143743d769803c23")
    version("3.0.7", sha256="7f43c84bca38fb8a41d7840dd2d7fab52456182babaa1e528791d0f4e517aba8")
    version("3.0.6", sha256="9e225731d57d2a76d35886841f8eff121bb3a45560b16077bd8c351151581d88")
    version("3.0.5", sha256="ab64ec6d2476fbfa40562e7edb510a8ab4c4fe5be77a4353ebf315c2af181a80")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("pythia8", default=True, description="build with pythia8")

    depends_on("cmake", type="build")
    depends_on("root")
    depends_on("pythia8", when="+pythia8")

    def cmake_args(self):
        args = []
        args.append(f"-DCMAKE_CXX_STANDARD={self.spec['root'].variants['cxxstd'].value}")
        return args

    def setup_run_environment(self, env):
        # make the cards distributed with delphes more easily accessible
        env.set("DELPHES_DIR", self.prefix)
        env.set("DELPHES", self.prefix)
