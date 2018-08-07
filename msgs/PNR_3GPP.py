#       PNR_3GPP.py
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

#TS 29.329 - 6.1.7

#~ < Push-Notification-Request > ::=			< Diameter Header:  309, REQ, PXY, 16777217 >
                                    #~ < Session-Id >
                                    #~ [ DRMP ]
                                    #~ { Vendor-Specific-Application-Id }
                                    #~ { Auth-Session-State }
                                    #~ { Origin-Host }
                                    #~ { Origin-Realm }
                                    #~ { Destination-Host }
                                    #~ { Destination-Realm }
                                    #~ *[ Supported-Features ]
                                    #~ { User-Identity }
                                    #~ [ Wildcarded-Public-Identity ]
                                    #~ [ Wildcarded-IMPU ]
                                    #~ [ User-Name ]
                                    #~ { User-Data }
                                    #~ *[ AVP ]
                                    #~ *[ Proxy-Info ]
                                    #~ *[ Route-Record ]
                                                    
def create_pkg(config):
    return Message(16777217, "Push-Notification",
        [DIAMETER_HDR_PROXIABLE, DIAMETER_HDR_REQUEST], [
            ("Session-Id", config["session-id"]),
            ("Vendor-Specific-Application-Id", [
                ("Vendor-Id", 10415),
                ("Auth-Application-Id", 16777217)
            ] ),
            ("Origin-Host", config["origin-host"]),
            ("Origin-Realm", config["origin-realm"]),
            ("Destination-Host", config["destination-host"]),
            ("Destination-Realm", config["destination-realm"]),
            ("Auth-Session-State", 1),
    #{ User-Identity }
    #{ User-Data }
        ])
