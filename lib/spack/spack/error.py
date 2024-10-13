# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import sys

import llnl.util.tty as tty

#: at what level we should write stack traces or short error messages
#: this is module-scoped because it needs to be set very early
debug = 0


class SpackError(Exception):
    """This is the superclass for all Spack errors.
    Subclasses can be found in the modules they have to do with.
    """

    def __init__(self, message, long_message=None):
        super().__init__()
        self.message = message
        self._long_message = long_message

        # for exceptions raised from child build processes, we save the
        # traceback as a string and print it in the parent.
        self.traceback = None

        # we allow exceptions to print debug info via print_context()
        # before they are caught at the top level. If they *haven't*
        # printed context early, we do it by default when die() is
        # called, so we need to remember whether it's been called.
        self.printed = False

    @property
    def long_message(self):
        return self._long_message

    def print_context(self):
        """Print extended debug information about this exception.

        This is usually printed when the top-level Spack error handler
        calls ``die()``, but it can be called separately beforehand if a
        lower-level error handler needs to print error context and
        continue without raising the exception to the top level.
        """
        if self.printed:
            return

        # basic debug message
        tty.error(self.message)
        if self.long_message:
            sys.stderr.write(self.long_message)
            sys.stderr.write("\n")

        # stack trace, etc. in debug mode.
        if debug:
            if self.traceback:
                # exception came from a build child, already got
                # traceback in child, so print it.
                sys.stderr.write(self.traceback)
            else:
                # run parent exception hook.
                sys.excepthook(*sys.exc_info())

        sys.stderr.flush()
        self.printed = True

    def die(self):
        self.print_context()
        sys.exit(1)

    def __str__(self):
        msg = self.message
        if self._long_message:
            msg += "\n    %s" % self._long_message
        return msg

    def __repr__(self):
        args = [repr(self.message), repr(self.long_message)]
        args = ",".join(args)
        qualified_name = inspect.getmodule(self).__name__ + "." + type(self).__name__
        return qualified_name + "(" + args + ")"

    def __reduce__(self):
        return type(self), (self.message, self.long_message)


class UnsupportedPlatformError(SpackError):
    """Raised by packages when a platform is not supported"""

    def __init__(self, message):
        super().__init__(message)


class NoLibrariesError(SpackError):
    """Raised when package libraries are requested but cannot be found"""

    def __init__(self, message_or_name, prefix=None):
        super().__init__(
            message_or_name
            if prefix is None
            else "Unable to locate {0} libraries in {1}".format(message_or_name, prefix)
        )


class NoHeadersError(SpackError):
    """Raised when package headers are requested but cannot be found"""


class SpecError(SpackError):
    """Superclass for all errors that occur while constructing specs."""


class UnsatisfiableSpecError(SpecError):
    """
    Raised when a spec conflicts with package constraints.

    For original concretizer, provide the requirement that was violated when
    raising.
    """

    def __init__(self, provided, required, constraint_type):
        # This is only the entrypoint for old concretizer errors
        super().__init__("%s does not satisfy %s" % (provided, required))

        self.provided = provided
        self.required = required
        self.constraint_type = constraint_type


class FetchError(SpackError):
    """Superclass for fetch-related errors."""


class NoSuchPatchError(SpackError):
    """Raised when a patch file doesn't exist."""


class PatchDirectiveError(SpackError):
    """Raised when the wrong arguments are suppled to the patch directive."""


class PatchLookupError(NoSuchPatchError):
    """Raised when a patch file cannot be located from sha256."""


class SpecSyntaxError(Exception):
    """Base class for Spec syntax errors"""


class PackageError(SpackError):
    """Raised when something is wrong with a package definition."""

    def __init__(self, message, long_msg=None):
        super().__init__(message, long_msg)


class NoURLError(PackageError):
    """Raised when someone tries to build a URL for a package with no URLs."""

    def __init__(self, cls):
        super().__init__("Package %s has no version with a URL." % cls.__name__)


class InstallError(SpackError):
    """Raised when something goes wrong during install or uninstall.

    The error can be annotated with a ``pkg`` attribute to allow the
    caller to get the package for which the exception was raised.
    """

    def __init__(self, message, long_msg=None, pkg=None):
        super().__init__(message, long_msg)
        self.pkg = pkg


class ConfigError(SpackError):
    """Superclass for all Spack config related errors."""


class StopPhase(SpackError):
    """Pickle-able exception to control stopped builds."""

    def __reduce__(self):
        return _make_stop_phase, (self.message, self.long_message)


def _make_stop_phase(msg, long_msg):
    return StopPhase(msg, long_msg)
