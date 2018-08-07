#       UDR_3GPP.py
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
import tools

#TS 29.329 - 6.1.1

#~ < User-Data -Request> ::=	< Diameter Header: 306, REQ, PXY, 16777217 >
                            #~ < Session-Id >
                            #~ [ DRMP ]
                            #~ { Vendor-Specific-Application-Id }
                            #~ { Auth-Session-State }
                            #~ { Origin-Host }
                            #~ { Origin-Realm }
                            #~ [ Destination-Host ]
                            #~ { Destination-Realm }
                            #~ *[ Supported-Features ]
                            #~ { User-Identity }
                            #~ [ Wildcarded-Public-Identity ]
                            #~ [ Wildcarded-IMPU ]
                            #~ [ Server-Name ]
                            #~ *[ Service-Indication ]
                            #~ *{ Data-Reference }
                            #~ *[ Identity-Set ]
                            #~ [ Requested-Domain ]
                            #~ [ Current-Location ]
                            #~ *[ DSAI-Tag ] 
                            #~ [ Session-Priority ] 
                            #~ [ User-Name ]
                            #~ [ Requested-Nodes ]
                            #~ [ Serving-Node-Indication ]
                            #~ [ Pre-paging-Supported ] 
                            #~ [ Local-Time-Zone-Indication ] 
                            #~ [ UDR-Flags ]
                            #~ [ Call-Reference-Info ] 
                            #~ [ OC-Supported-Features ]
                            #~ *[ AVP ]
                            #~ *[ Proxy-Info ]
                            #~ *[ Route-Record ]
                                                    
def create_pkg(config):
    ims = "ims.mnc%s.mcc%s.3gppnetwork.org" % (config['mnc'], config['mcc'])
    username = "%s@%s" % (config['msisdn'], ims)
    pubid = "sip:+%s" % (username)
    
    return Message(16777217, "User-Data",
        [DIAMETER_HDR_PROXIABLE, DIAMETER_HDR_REQUEST], [
            ("Session-Id", config["session-id"]),
            ("Vendor-Specific-Application-Id", [
                ("Vendor-Id", 10415),
                ("Auth-Application-Id", 16777217)
            ] ),
            ("Origin-Host", config["SH"]["origin-host-mme"]),
            ("Origin-Realm", config["SH"]["origin-realm"]),
            ("Destination-Host", config["SH"]["destination-host-hss"]),
            ("Destination-Realm", config["SH"]["destination-realm"]),
            ("Auth-Session-State", 1),
            ("User-Identity", [
                ("Public-Identity", pubid),
            ] ),
            ("Data-Reference", "USER_STATE"),
            ("Data-Reference", "IMSI"),
            ("Data-Reference", "LOCATION_INFORMATION"),
            ("Data-Reference", "SERVICE_LEVEL_TRACE_INFO"),
        ])
