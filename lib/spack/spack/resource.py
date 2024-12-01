# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Describes an optional resource needed for a build.

Typically a bunch of sources that can be built in-tree within another
package to enable optional features.

"""


class Resource:
    """Represents an optional resource to be fetched by a package.

    Aggregates a name, a fetcher, a destination and a placement.
    """

    def __init__(self, name, fetcher, destination, placement):
        self.name = name
        self.fetcher = fetcher
        self.destination = destination
        self.placement = placement
