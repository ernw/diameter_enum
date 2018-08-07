#       CER.py
#       
#       Copyright 2017 Daniel Mende <mail@c0decafe.de>
#

#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       AS IS AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#RFC 6733

#~ <CER> ::= < Diameter Header: 257, REQ >
                   #~ { Origin-Host }
                   #~ { Origin-Realm }
                #~ 1* { Host-IP-Address }
                   #~ { Vendor-Id }
                   #~ { Product-Name }
                   #~ [ Origin-State-Id ]
                 #~ * [ Supported-Vendor-Id ]
                 #~ * [ Auth-Application-Id ]
                 #~ * [ Inband-Security-Id ]
                 #~ * [ Acct-Application-Id ]
                 #~ * [ Vendor-Specific-Application-Id ]
                   #~ [ Firmware-Revision ]
                 #~ * [ AVP ]

from libDiameter import *
from message import Message

def create_pkg(config):
    return Message(0, "Capabilities-Exchange", 
        [DIAMETER_HDR_REQUEST], [
            ("Origin-Host", config["origin-host"]),
            ("Origin-Realm", config["origin-realm"]),
            ("Host-IP-Address", config["host-ip-address"]),
            ("Vendor-Id", config["vendor-id"]),
            ("Product-Name", config["product-name"]),
            ("Inband-Security-Id", config["inband-security-id"]),
        ])
