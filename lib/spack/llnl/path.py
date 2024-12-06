# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Path primitives that just require Python standard library."""
import functools
import sys
from typing import List, Optional
from urllib.parse import urlparse


class Path:
    """Enum to identify the path-style."""

    unix: int = 0
    windows: int = 1
    platform_path: int = windows if sys.platform == "win32" else unix


def format_os_path(path: str, mode: int = Path.unix) -> str:
    """Formats the input path to use consistent, platform specific separators.

    Absolute paths are converted between drive letters and a prepended '/' as per platform
    requirement.

    Parameters:
        path: the path to be normalized, must be a string or expose the replace method.
        mode: the path file separator style to normalize the passed path to.
            Default is unix style, i.e. '/'
    """
    if not path:
        return path
    if mode == Path.windows:
        path = path.replace("/", "\\")
    else:
        path = path.replace("\\", "/")
    return path


def convert_to_posix_path(path: str) -> str:
    """Converts the input path to POSIX style."""
    return format_os_path(path, mode=Path.unix)


def convert_to_platform_path(path: str) -> str:
    """Converts the input path to the current platform's native style."""
    return format_os_path(path, mode=Path.platform_path)


def path_to_os_path(*parameters: str) -> List[str]:
    """Takes an arbitrary number of positional parameters, converts each argument of type
    string to use a normalized filepath separator, and returns a list of all values.
    """

    def _is_url(path_or_url: str) -> bool:
        if "\\" in path_or_url:
            return False
        url_tuple = urlparse(path_or_url)
        return bool(url_tuple.scheme) and len(url_tuple.scheme) > 1

    result = []
    for item in parameters:
        if isinstance(item, str) and not _is_url(item):
            item = convert_to_platform_path(item)
        result.append(item)
    return result


def system_path_filter(_func=None, arg_slice: Optional[slice] = None):
    """Filters function arguments to account for platform path separators.
    Optional slicing range can be specified to select specific arguments

    This decorator takes all (or a slice) of a method's positional arguments
    and normalizes usage of filepath separators on a per platform basis.

    Note: `**kwargs`, urls, and any type that is not a string are ignored
    so in such cases where path normalization is required, that should be
    handled by calling path_to_os_path directly as needed.

    Parameters:
        arg_slice: a slice object specifying the slice of arguments
            in the decorated method over which filepath separators are
            normalized
    """

    def holder_func(func):
        @functools.wraps(func)
        def path_filter_caller(*args, **kwargs):
            args = list(args)
            if arg_slice:
                args[arg_slice] = path_to_os_path(*args[arg_slice])
            else:
                args = path_to_os_path(*args)
            return func(*args, **kwargs)

        return path_filter_caller

    if _func:
        return holder_func(_func)
    return holder_func


def sanitize_win_longpath(path: str) -> str:
    """Strip Windows extended path prefix from strings
    Returns sanitized string.
    no-op if extended path prefix is not present"""
    return path.lstrip("\\\\?\\")
