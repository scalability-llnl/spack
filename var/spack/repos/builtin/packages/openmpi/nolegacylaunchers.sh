#!/bin/sh
cat <<_EOF >&2
The users are strongly discouraged from using
'$0'.

Please, refer to your site's user guide for the recommended way to launch MPI
applications.

_EOF
exit 2
