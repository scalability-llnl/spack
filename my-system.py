# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.environment as ev
import spack.config as config
from spack.spec import Spec

import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="Collect details for simulating this system elsewhere")
    parser.add_argument("dest", help="Put all simulation resources in this dir (for target system to use)")
    args = parser.parse_args()

    if os.path.exists(args.dest):
        raise ValueError(f"Dest already exists: {args.dest}")


if __name__ == "__main__":
    main()