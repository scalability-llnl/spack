# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCaroline(RPackage):
    """A Collection of Database, Data Structure, Visualization, andUtility
    Functions for R.

    The caroline R library contains dozens of functions useful for: database
    migration (dbWriteTable2), database style joins & aggregation (nerge,
    groupBy & bestBy), data structure conversion (nv, tab2df), legend table
    making (sstable & leghead), plot annotation (labsegs & mvlabs), data
    visualization (violins, pies & raPlot), character string manipulation (m &
    pad), file I/O (write.delim), batch scripting and more. The package's
    greatest contributions lie in the database style merge, aggregation and
    interface functions as well as in it's extensive use and propagation of
    row, column and vector names in most functions."""

    cran = "caroline"

    license("Artistic-2.0")

    version("0.9.2", sha256="04dfc574b5f763b8c09e57b68657b8ae7e6aae36083dd71819c96f971d660297")
    version("0.9.0", sha256="7231daacf2f0e89d9363ea919071f8352ae487011f56e84a4054de11a9243ac8")
    version("0.8.0", sha256="58f464711f7279ca2aa173e6ce29d3308e01db37dccefbbf14cd7720c0231976")
    version("0.7.6", sha256="e7ba948f7d87f091b498dd0eec2ca4fdad7af4e2bbb67e0945c2f0d3f2eadda9")

    depends_on("r@1.8.0:", type=("build", "run"))
    depends_on("r@2.0.0:", type=("build", "run"), when="@0.9.0:")
