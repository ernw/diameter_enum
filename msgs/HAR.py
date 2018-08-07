#       HAR.py
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

#RFC4004 - 5.3

#~ <Home-Agent-MIP-Request> ::= < Diameter Header: 262, REQ, PXY >
                                      #~ < Session-Id >
                                      #~ { Auth-Application-Id }
                                      #~ { Authorization-Lifetime }
                                      #~ { Auth-Session-State }
                                      #~ { MIP-Reg-Request }
                                      #~ { Origin-Host }
                                      #~ { Origin-Realm }
                                      #~ { User-Name }
                                      #~ { Destination-Realm }
                                      #~ { MIP-Feature-Vector }
                                      #~ [ Destination-Host ]
                                      #~ [ MIP-MN-to-HA-MSA ]
                                      #~ [ MIP-MN-to-FA-MSA ]
                                      #~ [ MIP-HA-to-MN-MSA ]
                                      #~ [ MIP-HA-to-FA-MSA ]
                                      #~ [ MIP-MSA-Lifetime ]
                                      #~ [ MIP-Originating-Foreign-AAA ]
                                      #~ [ MIP-Mobile-Node-Address ]
                                      #~ [ MIP-Home-Agent-Address ]
                                    #~ * [ MIP-Filter-Rule ]
                                      #~ [ Origin-State-Id ]
                                    #~ * [ Proxy-Info ]
                                    #~ * [ Route-Record ]
                                    #~ * [ AVP ]
                                                    
def create_pkg(config):
    return Message(2, "Home-Agent-MIP",
        [DIAMETER_HDR_PROXIABLE, DIAMETER_HDR_REQUEST], [
            ("Session-Id", config["session-id"]),
            ("Auth-Application-Id", 2),
            ("Origin-Host", config["origin-host"]),
            ("Origin-Realm", config["origin-realm"]),
            ("Destination-Host", config["destination-host"]),
            ("Destination-Realm", config["destination-realm"]),
            ("Auth-Session-State", 1),
        ])
