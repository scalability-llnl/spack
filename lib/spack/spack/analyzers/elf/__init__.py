# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""The Elf analyzer is matched to pyelftools, which not only outputs elf symbols,
but also includes a subset of Dwarf DIEs (if they are available)."""


from ..analyzer_base import AnalyzerBase
import llnl.util.tty as tty
import os


class Elf(AnalyzerBase):

    name = "elf"
    outfile = "abi-facts.lp"
    description = "Dwarf and ELF Symbols in a logic program for a library."

    def run(self):
        """
        Prepare pyelftools for usage, load the spec, and generate facts.

        We write it out to the analyzers folder, with key as the analyzer name.
        """
        from .asp import generate_facts

        # Create the output directory if it doesn't exist.
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        outfile = os.path.join(self.output_dir, self.outfile)
        tty.info("Writing result to %s" % outfile)
        generate_facts(self.spec, outfile)
        return {self.name: outfile}

    def save_result(self, result, overwrite=False):
        """
        Read saved fact results and upload to monitor server.

        We haven't written this yet because we don't know what we would want
        to upload.
        """
        pass
