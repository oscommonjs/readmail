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

import string
import blessed

class MetaClassVars(type):
    def __new__(mcs, classname, bases, dictionary):
        for var_name in dictionary.get('_cls_vars', ()):
            dictionary[var_name] = var_name
        return type.__new__(mcs, classname, bases, dictionary)

class Action(metaclass=MetaClassVars):
    _cls_vars = [
        'refresh', 'quit',

        'up', 'down', 'left', 'right',

        'select', 'back',
    ]

Actions = set({
    Action.refresh,
    Action.quit,
    
    Action.up,
    Action.down,
    Action.left,
    Action.right,

    Action.select,
    Action.back,
})

class Keycode(metaclass=MetaClassVars):
    _cls_vars = list(string.ascii_letters+string.digits)


class Keysequence(metaclass=MetaClassVars):
    _cls_vars = [
        'KEY_UP', 'KEY_DOWN', 'KEY_LEFT', 'KEY_RIGHT',

        'KEY_ENTER',

        'KEY_DELETE',
    ]

Bindings = dict({
    Keycode.Q: Action.quit,
    Keycode.R: Action.refresh,

    Keysequence.KEY_UP: Action.up,
    Keysequence.KEY_DOWN: Action.down,
    Keysequence.KEY_LEFT: Action.left,
    Keysequence.KEY_RIGHT: Action.right,

    Keysequence.KEY_ENTER: Action.select,
    Keysequence.KEY_DELETE: Action.back,
})
