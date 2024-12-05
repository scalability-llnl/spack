# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.path


def get_projection(projections, spec):
    """
    Get the projection for a spec from a projections dict.
    """
    all_projection = None
    for spec_like, projection in projections.items():
        if spec.satisfies(spec_like):
            return spack.util.path.substitute_path_variables(projection)
        elif spec_like == "all":
            all_projection = spack.util.path.substitute_path_variables(projection)
    return all_projection
