#!/usr/bin/env python3
# Copyright (c) 2016, Samantha Marshall (http://pewpewthespells.com)
# All rights reserved.
#
# https://github.com/samdmarshall/readmail
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# 3. Neither the name of Samantha Marshall nor the names of its contributors may
# be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import argparse
from .version                               import __version__ as READMAIL_VERSION
from .helpers.Logger                        import Logger
from .helpers.Switch                        import Switch
from .configuration.mailboxconfiguration    import MailboxConfiguration
from .data.mail                             import MailData
from .                                      import term
from .                                      import data

def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='a simple email reader, for use with getmail')
    parser.add_argument(
        '--version',
        help='displays the version information',
        action='version',
        version=READMAIL_VERSION
    )
    parser.add_argument(
        '--quiet',
        help='Silences all logging output',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--verbose',
        help='Adds verbosity to logging output',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--no-ansi',
        help='Disables the ANSI color codes as part of the logger',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--debug',
        help=argparse.SUPPRESS,
        default=False,
        action='store_true'
    )
    
    # -------------------------------------------------------------------------
    # flags for readmail
    # -------------------------------------------------------------------------
    parser.add_argument(
        '--config',
        help='Specify a custom configuration path, the default is ~/.config/readmail/',
        default='~/.config/readmail/',
        action='store',
    )

    # -------------------------------------------------------------------------
    # application startup
    # -------------------------------------------------------------------------

    # collect all arguments from the command line and environment variable
    all_arguments = args
    default_arguments_from_env = os.environ.get('READMAIL_DEFAULT_FLAGS')
    if default_arguments_from_env is not None:
        all_arguments += default_arguments_from_env

    # now parse the arguments
    init = parser.parse_args(all_arguments)
    
    # perform the logging modifications before we do any other operations
    Logger.disableANSI(init.no_ansi)
    Logger.enableDebugLogger(init.debug)
    Logger.isVerbose(init.verbose)
    Logger.isSilent(init.quiet)
    
    # verify that this is being run in a UTF-8 supported environment
    if term.uses_suitable_locale() is False:
        Logger.write().error('Environment could not be configured to support UTF-8, exiting!')
        sys.exit(1)
    else:
        # start up the mailbox configuration first to verify that we have a valid config to work from
        config = MailboxConfiguration(init.config)
        if config.is_valid() is not True:
            Logger.write().error('Could not load; invalid configuration')
            sys.exit(1)
        mailbox = data.mail.LoadMailboxFromConfiguration(config.get_type(), config.get_location())
        if mailbox is not None:
            mail_data = MailData(mailbox)

if __name__ == '__main__':
    main()
