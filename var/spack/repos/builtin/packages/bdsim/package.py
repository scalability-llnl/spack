# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Bdsim(CMakePackage):
    """Beam Delivery Simulation (BDSIM) is a C++ program that utilises the Geant4 toolkit
    to simulate both the transport of particles in an accelerator and their
    interaction with the accelerator material"""

    homepage = "http://www.pp.rhul.ac.uk/bdsim/manual/index.html"
    url = "https://github.com/bdsim-collaboration/bdsim/archive/refs/tags/v1.7.7.tar.gz"
    git = "https://github.com/bdsim-collaboration/bdsim.git"

    tags = ["hep"]

    maintainers("gganis")

    license("GPL-3.0-or-later")

    version("master", branch="master")
    version("1.7.7", sha256="8923a197c97984e32651f877c35c3f759ca8d20b661aaec200b83dbd72e4d7d9")
    version("1.7.6", sha256="7740d9fb3bcc9856a36b74130fae68def878d86c6f7e4a54c9d7a2db8dd770bc")
    version("1.7.0", sha256="519bdede40470907d3305556ed5cf9523a2d7c0446db764338741d0ca43a86b4")
    version("1.6.0", sha256="c0149a68d3c2436e036e8f71a13a251a2d88afe51e4387fe43ebd31a96bb3d7d")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake")
    depends_on("geant4")
    depends_on("geant4@:10.7.3", when="@:1.6.0")
    depends_on("root")
    depends_on("clhep")
    depends_on("flex")
    depends_on("bison")

    # The C++ standard is set to be the same as the one used for ROOT
