# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class LocationtypeSolverSetup(object):
    """Additional setup to generate symbols, locations, and types.

    This model can be added to the spack solve by adding the extra_setup for
    "locationtype". The driver is shared between the two.
    """
    name = "locationtype"

    def __init__(self):

        # This is the default logic program
        self.lp = ["locationtype.lp"]

        # These additional programs are currently required, generated
        # by an analyzer "abi_type_location." In a production version of
        # this model, we would derive this from elsewhere.
        self.needs = "abi-type-location.lp"

    def setup(self, driver, specs, tests=False):
        """Generate an ASP program with relevant constraints for specs.

        Currently we are generating all needed facts with an analyzer.
        """
        pass
