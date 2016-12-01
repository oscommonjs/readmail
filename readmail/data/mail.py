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
import mailbox
from ..helpers.Logger       import Logger
from ..helpers.Switch       import Switch

def LoadMailboxFromConfiguration(mailbox_type: str, location: str) -> mailbox.Mailbox:
    mail_box = None
    if os.path.exists(location) is True:
        for case in Switch(mailbox_type):
            if case('maildir'):
                mail_box = mailbox.Maildir(location)
                break
            if case('mbox'):
                mail_box = mailbox.mbox(location)
                break
            if case('mh'):
                mail_box = mailbox.MH(location)
                break
            if case('babyl'):
                mail_box = mailbox.Babyl(location)
                break
            if case('mmdf'):
                mail_box = mailbox.MMDF(location)
                break
            if case():
                Logger.write().error('Unknown mailbox type "%s" was specified' % mailbox_type)
                break
    else:
        Logger.write().error('The mailbox path given (%s) does not exist!' % location)
    return mail_box

class MailData(object):
    def __init__(self, mail_box: mailbox.Mailbox):
        self.__mailbox = mail_box
