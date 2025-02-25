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


class ConfigScopePriority(enum.IntEnum):
    """Priorities of the different kind of config scopes used by Spack"""

    BUILTIN = 0
    CONFIG_FILES = 1
    CUSTOM = 2
    ENVIRONMENT = 3
    COMMAND_LINE = 4
