# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# Important feature: a set of salome-xxx packages must have all the same version
# - except salome-med that is also fixed but by another number version

from spack.package import *


class SalomeConfiguration(Package):
    """salome-configuration is a part of SALOME platform and define general
    build tools for the platform."""

    maintainers("franciskloss")

    homepage = "https://www.salome-platform.org"
    git = "https://git.salome-platform.org/gitpub/tools/configuration.git"

    version("9.13.0", tag="V9_13_0", commit="1c9b00436fc0e8264742460ebc102ae7d1970e97")
    version("9.12.0", tag="V9_12_0", commit="61ed79521f31363ba4aeedcd59812a4838c076aa")
    version("9.11.0", tag="V9_11_0", commit="33fc859a523e9f84cabaae2c55fdc64d1be11ec0")
    version("9.10.0", tag="V9_10_0", commit="25f724f7a6c0000330a40c3851dcd8bc2493e1fa")
    version("9.9.0", tag="V9_9_0", commit="5e61c7330cb2e0ff39e0bf4ba7b65d1d26c824ac")
    version("9.8.0", tag="V9_8_0", commit="f1b2929d32953ac4d2056d564dab62e2e8d7c2a5")
    version("9.7.0", tag="V9_7_0", commit="b1430e72bc252867289b45de9a94041841fade06")
    version("9.6.0", tag="V9_6_0", commit="02e621fc9e24b4eab20f82ef921859013bf024b4")
    version("9.5.0", tag="V9_5_0", commit="96ecd4927604943dc80ead4aaf732a9d0215b70c")
    version("9.4.0", tag="V9_4_0", commit="057e00d65a86f058dd4b0f82a866fcc66d81ed63")
    version("9.3.0", tag="V9_3_0", commit="de7bac0ee58007a9501fffa7c1488de029b19cdc")

    patch("SalomeMacros.patch", working_dir="./cmake")
    patch("FindSalomeHDF5.patch", working_dir="./cmake", when="@:9.7.0")

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("CONFIGURATION_ROOT_DIR", self.prefix)

    def install(self, spec, prefix):
        install_tree(".", prefix)
