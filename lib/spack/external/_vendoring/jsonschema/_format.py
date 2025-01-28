import datetime
import re
import socket
import struct

from jsonschema.compat import str_types
from jsonschema.exceptions import FormatError


class FormatChecker(object):
    """
    A ``format`` property checker.

    JSON Schema does not mandate that the ``format`` property actually do any
    validation. If validation is desired however, instances of this class can
    be hooked into validators to enable format validation.

    `FormatChecker` objects always return ``True`` when asked about
    formats that they do not know how to validate.

    To check a custom format using a function that takes an instance and
    returns a ``bool``, use the `FormatChecker.checks` or
    `FormatChecker.cls_checks` decorators.

    Arguments:

        formats (~collections.Iterable):

            The known formats to validate. This argument can be used to
            limit which formats will be used during validation.
    """

    checkers = {}

    def __init__(self, formats=None):
        if formats is None:
            self.checkers = self.checkers.copy()
        else:
            self.checkers = dict((k, self.checkers[k]) for k in formats)

    def __repr__(self):
        return "<FormatChecker checkers={}>".format(sorted(self.checkers))

    def checks(self, format, raises=()):
        """
        Register a decorated function as validating a new format.

        Arguments:

            format (str):

                The format that the decorated function will check.

            raises (Exception):

                The exception(s) raised by the decorated function when an
                invalid instance is found.

                The exception object will be accessible as the
                `jsonschema.exceptions.ValidationError.cause` attribute of the
                resulting validation error.
        """

        def _checks(func):
            self.checkers[format] = (func, raises)
            return func
        return _checks

    cls_checks = classmethod(checks)

    def check(self, instance, format):
        """
        Check whether the instance conforms to the given format.

        Arguments:

            instance (*any primitive type*, i.e. str, number, bool):

                The instance to check

            format (str):

                The format that instance should conform to


        Raises:

            FormatError: if the instance does not conform to ``format``
        """

        if format not in self.checkers:
            return

        func, raises = self.checkers[format]
        result, cause = None, None
        try:
            result = func(instance)
        except raises as e:
            cause = e
        if not result:
            raise FormatError(
                "%r is not a %r" % (instance, format), cause=cause,
            )

    def conforms(self, instance, format):
        """
        Check whether the instance conforms to the given format.

        Arguments:

            instance (*any primitive type*, i.e. str, number, bool):

                The instance to check

            format (str):

                The format that instance should conform to

        Returns:

            bool: whether it conformed
        """

        try:
            self.check(instance, format)
        except FormatError:
            return False
        else:
            return True


draft3_format_checker = FormatChecker()
draft4_format_checker = FormatChecker()
draft6_format_checker = FormatChecker()
draft7_format_checker = FormatChecker()


_draft_checkers = dict(
    draft3=draft3_format_checker,
    draft4=draft4_format_checker,
    draft6=draft6_format_checker,
    draft7=draft7_format_checker,
)


def _checks_drafts(
    name=None,
    draft3=None,
    draft4=None,
    draft6=None,
    draft7=None,
    raises=(),
):
    draft3 = draft3 or name
    draft4 = draft4 or name
    draft6 = draft6 or name
    draft7 = draft7 or name

    def wrap(func):
        if draft3:
            func = _draft_checkers["draft3"].checks(draft3, raises)(func)
        if draft4:
            func = _draft_checkers["draft4"].checks(draft4, raises)(func)
        if draft6:
            func = _draft_checkers["draft6"].checks(draft6, raises)(func)
        if draft7:
            func = _draft_checkers["draft7"].checks(draft7, raises)(func)

        # Oy. This is bad global state, but relied upon for now, until
        # deprecation. See https://github.com/Julian/jsonschema/issues/519
        # and test_format_checkers_come_with_defaults
        FormatChecker.cls_checks(draft7 or draft6 or draft4 or draft3, raises)(
            func,
        )
        return func
    return wrap


@_checks_drafts(name="idn-email")
@_checks_drafts(name="email")
def is_email(instance):
    if not isinstance(instance, str_types):
        return True
    return "@" in instance


_ipv4_re = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


@_checks_drafts(
    draft3="ip-address", draft4="ipv4", draft6="ipv4", draft7="ipv4",
)
def is_ipv4(instance):
    if not isinstance(instance, str_types):
        return True
    if not _ipv4_re.match(instance):
        return False
    return all(0 <= int(component) <= 255 for component in instance.split("."))


if hasattr(socket, "inet_pton"):
    # FIXME: Really this only should raise struct.error, but see the sadness
    #        that is https://twistedmatrix.com/trac/ticket/9409
    @_checks_drafts(
        name="ipv6", raises=(socket.error, struct.error, ValueError),
    )
    def is_ipv6(instance):
        if not isinstance(instance, str_types):
            return True
        return socket.inet_pton(socket.AF_INET6, instance)


_host_name_re = re.compile(r"^[A-Za-z0-9][A-Za-z0-9\.\-]{1,255}$")


@_checks_drafts(
    draft3="host-name",
    draft4="hostname",
    draft6="hostname",
    draft7="hostname",
)
def is_host_name(instance):
    if not isinstance(instance, str_types):
        return True
    if not _host_name_re.match(instance):
        return False
    components = instance.split(".")
    for component in components:
        if len(component) > 63:
            return False
    return True


@_checks_drafts(name="regex", raises=re.error)
def is_regex(instance):
    if not isinstance(instance, str_types):
        return True
    return re.compile(instance)


@_checks_drafts(draft3="date", draft7="date", raises=ValueError)
def is_date(instance):
    if not isinstance(instance, str_types):
        return True
    return datetime.datetime.strptime(instance, "%Y-%m-%d")


@_checks_drafts(draft3="time", raises=ValueError)
def is_draft3_time(instance):
    if not isinstance(instance, str_types):
        return True
    return datetime.datetime.strptime(instance, "%H:%M:%S")
