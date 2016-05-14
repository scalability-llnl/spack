##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
__all__ = ['Executable', 'which', 'ProcessError']

import os
import sys
import re
import subprocess
import inspect

import llnl.util.tty as tty
import spack
import spack.error


class Executable(object):
    """Class representing a program that can be run on the command line."""
    def __init__(self, name):
        self.exe = name.split(' ')
        self.returncode = None

        if not self.exe:
            raise ProcessError("Cannot construct executable for '%s'" % name)


    def add_default_arg(self, arg):
        self.exe.append(arg)


    @property
    def command(self):
        return ' '.join(self.exe)


    def __call__(self, *args, **kwargs):
        """Run this executable in a subprocess.

        Arguments
          args
            command line arguments to the executable to run.

        Optional arguments

          fail_on_error

            Raise an exception if the subprocess returns an
            error. Default is True.  When not set, the return code is
            avaiale as `exe.returncode`.

          ignore_errors

            An optional list/tuple of error codes that can be
            *ignored*.  i.e., if these codes are returned, this will
            not raise an exception when `fail_on_error` is `True`.

          output, error

            These arguments allow you to specify new stdout and stderr
            values.  They default to `None`, which means the
            subprocess will inherit the parent's file descriptors.

            You can set these to:
            - python streams, e.g. open Python file objects, or os.devnull;
            - filenames, which will be automatically opened for writing; or
            - `str`, as in the Python string type. If you set these to `str`,
               output and error will be written to pipes and returned as
               a string.  If both `output` and `error` are set to `str`,
               then one string is returned containing output concatenated
               with error.

          input

            Same as output, error, but `str` is not an allowed value.

        Deprecated arguments

          return_output[=False]

            Setting this to True is the same as setting output=str.
            This argument may be removed in future Spack versions.

        """
        fail_on_error = kwargs.pop("fail_on_error", True)
        ignore_errors = kwargs.pop("ignore_errors", ())

        # TODO: This is deprecated.  Remove in a future version.
        return_output = kwargs.pop("return_output", False)

        # Default values of None says to keep parent's file descriptors.
        if return_output:
            output = str
        else:
            output = kwargs.pop("output", None)

        error         = kwargs.pop("error", None)
        input         = kwargs.pop("input", None)
        if input is str:
            raise ValueError("Cannot use `str` as input stream.")

        def streamify(arg, mode):
            if isinstance(arg, basestring):
                return open(arg, mode), True
            elif arg is str:
                return subprocess.PIPE, False
            else:
                return arg, False
        ostream, close_ostream = streamify(output, 'w')
        estream, close_estream = streamify(error,  'w')
        istream, close_istream = streamify(input,  'r')

        # if they just want to ignore one error code, make it a tuple.
        if isinstance(ignore_errors, int):
            ignore_errors = (ignore_errors,)

        quoted_args = [arg for arg in args if re.search(r'^"|^\'|"$|\'$', arg)]
        if quoted_args:
            tty.warn("Quotes in command arguments can confuse scripts like configure.",
                     "The following arguments may cause problems when executed:",
                     str("\n".join(["    "+arg for arg in quoted_args])),
                     "Quotes aren't needed because spack doesn't use a shell.",
                     "Consider removing them")

        cmd = self.exe + list(args)

        cmd_line = "'%s'" % "' '".join(map(lambda arg: arg.replace("'", "'\"'\"'"), cmd))
        tty.debug(cmd_line)

        try:
            proc = subprocess.Popen(
                cmd, stdin=istream, stderr=estream, stdout=ostream)
            out, err = proc.communicate()

            rc = self.returncode = proc.returncode
            if fail_on_error and rc != 0 and (rc not in ignore_errors):
                raise ProcessError("Command exited with status %d:"
                                   % proc.returncode, cmd_line)

            if output is str or error is str:
                result = ''
                if output is str: result += out
                if error is str:  result += err
                return result

        except OSError, e:
            raise ProcessError(
                "%s: %s" % (self.exe[0], e.strerror),
                "Command: " + cmd_line)

        except subprocess.CalledProcessError, e:
            if fail_on_error:
                raise ProcessError(
                    str(e),
                    "\nExit status %d when invoking command: %s"
                    % (proc.returncode, cmd_line))

        finally:
            if close_ostream: output.close()
            if close_estream: error.close()
            if close_istream: input.close()


    def __eq__(self, other):
        return self.exe == other.exe


    def __neq__(self, other):
        return not (self == other)


    def __hash__(self):
        return hash((type(self),) + tuple(self.exe))


    def __repr__(self):
        return "<exe: %s>" % self.exe


    def __str__(self):
        return ' '.join(self.exe)



def which(name, **kwargs):
    """Finds an executable in the path like command-line which."""
    path     = kwargs.get('path', os.environ.get('PATH', '').split(os.pathsep))
    required = kwargs.get('required', False)

    if not path:
        path = []

    for dir in path:
        exe = os.path.join(dir, name)
        if os.path.isfile(exe) and os.access(exe, os.X_OK):
            return Executable(exe)

    if required:
        tty.die("spack requires %s.  Make sure it is in your path." % name)
    return None


class ProcessError(spack.error.SpackError):
    def __init__(self, msg, long_message=None):
        # These are used for detailed debugging information for
        # package builds.  They're built up gradually as the exception
        # propagates.
        self.package_context = _get_package_context()
        self.build_log = None

        super(ProcessError, self).__init__(msg, long_message)

    @property
    def long_message(self):
        msg = self._long_message
        if msg: msg += "\n\n"

        if self.build_log:
            msg += "See build log for details:\n"
            msg += "  %s" % self.build_log

        if self.package_context:
            if msg: msg += "\n\n"
            msg += '\n'.join(self.package_context)

        return msg


def _get_package_context():
    """Return some context for an error message when the build fails.

    This should be called within a ProcessError when the exception is
    thrown.

    Args:
    process_error -- A ProcessError raised during install()

    This function inspects the stack to find where we failed in the
    package file, and it adds detailed context to the long_message
    from there.

    """
    lines = []

    # Walk up the stack
    for f in inspect.stack():
        frame = f[0]

        # Find a frame with 'self' in the local variables.
        if not 'self' in frame.f_locals:
            continue

        # Look only at a frame in a subclass of spack.Package
        obj = frame.f_locals['self']
        if type(obj) != spack.Package and isinstance(obj, spack.Package):
            break
    else:
        # Didn't find anything
        return lines

    # Build a message showing where in install we failed.
    lines.append("%s:%d, in %s:" % (
        inspect.getfile(frame.f_code),
        frame.f_lineno,
        frame.f_code.co_name))

    sourcelines, start = inspect.getsourcelines(frame)
    for i, line in enumerate(sourcelines):
        mark = ">> " if start + i == frame.f_lineno else "   "
        lines.append("  %s%-5d%s" % (mark, start + i, line.rstrip()))

    return lines
