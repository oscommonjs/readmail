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

import blessed
from progress.bar import Bar
from ..helpers.Logger                       import Logger
from ..helpers.Switch                       import Switch
from ..bindings                             import *
from ..configuration                        import MailboxConfiguration
from ..data.mail                            import *
from ..data.message                         import *

InMessageView = False
SelectedMessageIndex = 0

def reset_globals() -> None:
    global InMessageView
    InMessageView = False

    global SelectedMessageIndex
    SelectedMessageIndex = 0

def draw_clear(terminal: blessed.Terminal) -> None:
    terminal.clear()

def draw_exit(terminal: blessed.Terminal) -> None:
    terminal.exit_fullscreen()

class UI(object):

    def __init__(self, initialization) -> None:
        self.__startup = initialization
        self.__terminal = blessed.Terminal()
        self.__is_running = True
        self.__folders = set()
        self.refresh()

    def process_input(self) -> None:
        with self.__terminal.cbreak():
            value = self.__terminal.inkey()
            if value.is_sequence is True:
                value = value.name
            action = Bindings.get(value)
            for case in Switch(action):
                Logger.write().debug('Action: "%s"' % action)
                if case(Action.quit):
                    self.__is_running = False
                    break
                if case(Action.refresh):
                    self.refresh()
                    break
                if case(Action.up):
                    self.navigate_up()
                    break
                if case(Action.down):
                    self.navigate_down()
                    break
                if case(Action.select):
                    self.navigate_in()
                    break
                if case(Action.back):
                    self.navigate_back()
                    break
                if case():
                    break

    def start(self) -> None:
        if self.__terminal.is_a_tty is True:
            with self.__terminal.hidden_cursor():
                self.folders()
                while self.__is_running is True:
                    self.process_input()
        else:
            Logger.write().error('Not a tty, unable to start up!')
        Logger.write().info('Quitting...')
        draw_exit(self.__terminal)

    def refresh(self) -> None:
        folder_set = set()
        # start up the mailbox configuration first to verify that we have a valid config to work from
        self.__config = MailboxConfiguration(self.__startup.config)
        if self.__config.is_valid() is not True:
            Logger.write().error('Could not load; invalid configuration')
        reset_globals()
        draw_clear(self.__terminal)
        mailbox_data = LoadMailboxFromConfiguration(self.__config.get_type(), self.__config.get_location())
        self.__data = MailData(mailbox_data)
        messages = self.__data.messages()
        for message_key in Bar('Loading eMail').iter(messages):
            message = self.__data.get_message(message_key)

    def view_mail(self) -> None:
        with self.__terminal.fullscreen():

    def navigate_up(self) -> None:
        if InMessageView is False:
            global SelectedMessageIndex                    
            if SelectedMessageIndex - 1 >= 0:
                SelectedMessageIndex -= 1
            self.view_mail()

    def navigate_down(self) -> None:
        if InFolderView is False:
            global SelectedMessageIndex
            if SelectedMessageIndex + 1 < len(self.__messages):
                SelectedMessageIndex += 1
            self.view_mail()

    def navigate_in(self) -> None:
        global InMessageView
        if InMessageView is False:
            InMessageView = True

    def navigate_back(self) -> None:
        global InMessageView
        if InMessageView is True:
            InMessageView = False
            self.view_mail()
