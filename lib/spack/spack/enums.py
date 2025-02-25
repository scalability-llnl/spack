# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Enumerations used throughout Spack"""
import enum


class InstallRecordStatus(enum.Flag):
    """Enum flag to facilitate querying status from the DB"""

    INSTALLED = enum.auto()
    DEPRECATED = enum.auto()
    MISSING = enum.auto()
    ANY = INSTALLED | DEPRECATED | MISSING
