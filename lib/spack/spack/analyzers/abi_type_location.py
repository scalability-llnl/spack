# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import llnl.util.tty as tty

from .analyzer_base import AnalyzerBase

import os


class AbiTypeLocation(AnalyzerBase):

    name = "abi_type_location"
    outfile = "abi-type-location.lp"
    description = "Extract types and locations into a logic program."

    def run(self):
        """
        Run the analyzer to extract types and locations.
        """
        from .elf.asp import generate_facts

        # Create the output directory if it doesn't exist.
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        outfile = os.path.join(self.output_dir, self.outfile)
        tty.info("Writing result to %s" % outfile)
        generate_facts(self.spec, outfile, details=True)
        return {self.name: outfile}

    def save_result(self, result, overwrite=False):
        """
        Read saved fact results and upload to monitor server.

        We haven't written this yet because we don't know what we would want
        to upload.
        """
        pass
