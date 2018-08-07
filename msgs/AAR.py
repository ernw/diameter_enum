#       AAR.py
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

from libDiameter import *
from message import Message

#RFC7155 - 3.1

#~ <AA-Request> ::= < Diameter Header: 265, REQ, PXY >
                          #~ < Session-Id >
                          #~ { Auth-Application-Id }
                          #~ { Origin-Host }
                          #~ { Origin-Realm }
                          #~ { Destination-Realm }
                          #~ { Auth-Request-Type }
                          #~ [ Destination-Host ]
                          #~ [ NAS-Identifier ]
                          #~ [ NAS-IP-Address ]
                          #~ [ NAS-IPv6-Address ]
                          #~ [ NAS-Port ]
                          #~ [ NAS-Port-Id ]
                          #~ [ NAS-Port-Type ]
                          #~ [ Origin-AAA-Protocol ]
                          #~ [ Origin-State-Id ]
                          #~ [ Port-Limit ]
                          #~ [ User-Name ]
                          #~ [ User-Password ]
                          #~ [ Service-Type ]
                          #~ [ State ]
                          #~ [ Authorization-Lifetime ]
                          #~ [ Auth-Grace-Period ]
                          #~ [ Auth-Session-State ]
                          #~ [ Callback-Number ]
                          #~ [ Called-Station-Id ]
                          #~ [ Calling-Station-Id ]
                          #~ [ Originating-Line-Info ]
                          #~ [ Connect-Info ]
                          #~ [ CHAP-Auth ]
                          #~ [ CHAP-Challenge ]
                        #~ * [ Framed-Compression ]
                          #~ [ Framed-Interface-Id ]
                          #~ [ Framed-IP-Address ]
                        #~ * [ Framed-IPv6-Prefix ]
                          #~ [ Framed-IP-Netmask ]
                          #~ [ Framed-MTU ]
                          #~ [ Framed-Protocol ]
                          #~ [ ARAP-Password ]
                          #~ [ ARAP-Security ]
                        #~ * [ ARAP-Security-Data ]
                        #~ * [ Login-IP-Host ]
                        #~ * [ Login-IPv6-Host ]
                          #~ [ Login-LAT-Group ]
                          #~ [ Login-LAT-Node ]
                          #~ [ Login-LAT-Port ]
                          #~ [ Login-LAT-Service ]
                        #~ * [ Tunneling ]
                        #~ * [ Proxy-Info ]
                        #~ * [ Route-Record ]
                        #~ * [ AVP ]


def create_pkg(config):
    return Message(3, "AA",
        [DIAMETER_HDR_PROXIABLE, DIAMETER_HDR_REQUEST], [
            ("Session-Id", config["session-id"]),
            ("Origin-Host", config["origin-host"]),
            ("Origin-Realm", config["origin-realm"]),
            ("Destination-Realm", config["destination-realm"]),
            ("Auth-Application-Id", 1),
            ("Auth-Request-Type", int(config["auth-request-type"])),
        ])
