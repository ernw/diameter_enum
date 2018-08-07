#!/usr/bin/env python2

#       diameter_enum.py
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
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import print_function

from libDiameter import *

from argparse import ArgumentParser
import binascii
from backports.configparser import RawConfigParser
import datetime
import socket
import select
import time
import unicodedata
import pprint
import csv
import os

from message import Message

APPIDS = './appids.csv'
MSG_PATH = './msgs/'

DIAMETER_PORT = 3868
MSG_SIZE = 4096

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

result_codes = {
#https://www.iana.org/assignments/aaa-parameters/aaa-parameters.xhtml
    
    #Informational
    1000	:   "Reserved",
    1001	:   "DIAMETER_MULTI_ROUND_AUTH",
    
    #Success
    2000	:   "Reserved",
    2001	:   "DIAMETER_SUCCESS",
    2002	:   "DIAMETER_LIMITED_SUCCESS",
    2003	:   "DIAMETER_FIRST_REGISTRATION",
    2004	:   "DIAMETER_SUBSEQUENT_REGISTRATION",
    2005	:   "DIAMETER_UNREGISTERED_SERVICE",
    2006	:   "DIAMETER_SUCCESS_SERVER_NAME_NOT_STORED",
    2007	:   "DIAMETER_SERVER_SELECTION",
    2008	:   "DIAMETER_SUCCESS_AUTH_SENT_SERVER_NOT_STORED",
    2009	:   "DIAMETER_SUCCESS_RELOCATE_HA",

    #Protocol Errors
    3000    :   "Reserved",
    3001	:   "DIAMETER_COMMAND_UNSUPPORTED",
    3002	:   "DIAMETER_UNABLE_TO_DELIVER",
    3003	:   "DIAMETER_REALM_NOT_SERVED",
    3004	:   "DIAMETER_TOO_BUSY",
    3005	:   "DIAMETER_LOOP_DETECTED",
    3006	:   "DIAMETER_REDIRECT_INDICATION",
    3007	:   "DIAMETER_APPLICATION_UNSUPPORTED",
    3008	:   "DIAMETER_INVALID_HDR_BITS",
    3009	:   "DIAMETER_INVALID_AVP_BITS",
    3010	:   "DIAMETER_UNKNOWN_PEER",
    3011	:   "DIAMETER_REALM_REDIRECT_INDICATION",

    #Transient Failures
    4000	:   "Reserved",
    4001	:   "DIAMETER_AUTHENTICATION_REJECTED",
    4002	:   "DIAMETER_OUT_OF_SPACE",
    4003	:   "ELECTION_LOST",
    4005	:   "DIAMETER_ERROR_MIP_REPLY_FAILURE",
    4006	:   "DIAMETER_ERROR_HA_NOT_AVAILABLE",
    4007	:   "DIAMETER_ERROR_BAD_KEY",
    4008	:   "DIAMETER_ERROR_MIP_FILTER_NOT_SUPPORTED",
    4010	:   "DIAMETER_END_USER_SERVICE_DENIED",
    4011	:   "DIAMETER_CREDIT_CONTROL_NOT_APPLICABLE",
    4012	:   "DIAMETER_CREDIT_LIMIT_REACHED",
    4013	:   "DIAMETER_USER_NAME_REQUIRED",
    4014	:   "RESOURCE_FAILURE",
    
    #Permanent Failure
    5000	:   "Reserved",
    5001	:   "DIAMETER_AVP_UNSUPPORTED",
    5002	:   "DIAMETER_UNKNOWN_SESSION_ID",
    5003	:   "DIAMETER_AUTHORIZATION_REJECTED",
    5004	:   "DIAMETER_INVALID_AVP_VALUE",
    5005	:   "DIAMETER_MISSING_AVP",
    5006	:   "DIAMETER_RESOURCES_EXCEEDED",
    5007	:   "DIAMETER_CONTRADICTING_AVPS",
    5008	:   "DIAMETER_AVP_NOT_ALLOWED",
    5009	:   "DIAMETER_AVP_OCCURS_TOO_MANY_TIMES",
    5010	:   "DIAMETER_NO_COMMON_APPLICATION",
    5011	:   "DIAMETER_UNSUPPORTED_VERSION",
    5012	:   "DIAMETER_UNABLE_TO_COMPLY",
    5013	:   "DIAMETER_INVALID_BIT_IN_HEADER",
    5014	:   "DIAMETER_INVALID_AVP_LENGTH",
    5015	:   "DIAMETER_INVALID_MESSAGE_LENGTH",
    5016	:   "DIAMETER_INVALID_AVP_BIT_COMBO",
    5017	:   "DIAMETER_NO_COMMON_SECURITY",
    5018	:   "DIAMETER_RADIUS_AVP_UNTRANSLATABLE",
    5024	:   "DIAMETER_ERROR_NO_FOREIGN_HA_SERVICE",
    5025	:   "DIAMETER_ERROR_END_TO_END_MIP_KEY_ENCRYPTION",
    5030	:   "DIAMETER_USER_UNKNOWN",
    5031	:   "DIAMETER_RATING_FAILED",
    5032	:   "DIAMETER_ERROR_USER_UNKNOWN",
    5033	:   "DIAMETER_ERROR_IDENTITIES_DONT_MATCH",
    5034	:   "DIAMETER_ERROR_IDENTITY_NOT_REGISTERED",
    5035	:   "DIAMETER_ERROR_ROAMING_NOT_ALLOWED",
    5036	:   "DIAMETER_ERROR_IDENTITY_ALREADY_REGISTERED",
    5037	:   "DIAMETER_ERROR_AUTH_SCHEME_NOT_SUPPORTED",
    5038	:   "DIAMETER_ERROR_IN_ASSIGNMENT_TYPE",
    5039	:   "DIAMETER_ERROR_TOO_MUCH_DATA",
    5040	:   "DIAMETER_ERROR_NOT SUPPORTED_USER_DATA",
    5041	:   "DIAMETER_ERROR_MIP6_AUTH_MODE",
    5042	:   "UNKNOWN_BINDING_TEMPLATE_NAME",
    5043	:   "BINDING_FAILURE",
    5044	:   "MAX_BINDINGS_SET_FAILURE",
    5045	:   "MAXIMUM_BINDINGS_REACHED_FOR_ENDPOINT",
    5046	:   "SESSION_EXISTS",
    5047	:   "INSUFFICIENT_CLASSIFIERS",
    5048	:   "DIAMETER_ERROR_EAP_CODE_UNKNOWN",
    
    None    :   "TIMEOUT",
}

def err2msg(err):
    try:
        return result_codes[err]
    except:
        return "undefined"

appids = {}
with open(APPIDS) as idfile:
    reader = csv.reader(idfile)
    for row in reader:
        appids[int(row[0])] = row[1] + " " + row[2]

msgs = {}
sys.path.append(MSG_PATH)
for i in os.listdir(MSG_PATH):
    if os.path.isfile(os.path.join(MSG_PATH, i)):
        (name, ext) = os.path.splitext(i)
        if ext == ".py":
            msgs[name] = __import__(name)

def dflt_host_realm(config, section):
    if not 'origin-host' in config[section]:
        config[section]['origin-host'] = config['origin-host']
    if not 'origin-realm' in config[section]:
        config[section]['origin-realm'] = config['origin-realm']
    if not 'destination-host' in config[section]:
        config[section]['destination-host'] = config['destination-host']
    if not 'destination-realm' in config[section]:
        config[section]['destination-realm'] = config['destination-realm']

def load_config(cfile):
    cparser = RawConfigParser()
    cparser.read(cfile)
    config = {  'S6A'       : {},
                'SH'        : {},
                'SLH'       : {},
                }
    for i in cparser['DEFAULT']:
        config[i] = unicodedata.normalize('NFKD', cparser['DEFAULT'][i]).encode('ascii','ignore')
    
    if 'S6A' in cparser:
        for i in cparser['S6A']:
            config['S6A'][i] = unicodedata.normalize('NFKD', cparser['S6A'][i]).encode('ascii','ignore')
    dflt_host_realm(config, 'S6A')
    
    if 'SH' in cparser:
        for i in cparser['SH']:
            config['SH'][i] = unicodedata.normalize('NFKD', cparser['SH'][i]).encode('ascii','ignore')
    dflt_host_realm(config, 'SH')
    
    if 'SLH' in cparser:
        for i in cparser['SLH']:
            config['SLH'][i] = unicodedata.normalize('NFKD', cparser['SLH'][i]).encode('ascii','ignore')
    dflt_host_realm(config, 'SLH')
    
    #enrich config
    config['provider-url'] = "mnc%s.mcc%s.3gppnetwork.org" % (config['mnc'], config['mcc'])
    config['epc-url'] = "epc.%s" % (config['provider-url'])
    config['ims-url'] = "ims.%s" % (config['provider-url'])
    config['username'] = "%s@%s" % (config['imsi'], config['ims-url'])
    config['public-identity'] = "sip:%s" % (config['username'])
    
    return config

def connect(stype, dst, src):
    sock = socket.socket(socket.AF_INET, stype)
    if src is not None:
        sock.bind(src)
    sock.connect(dst)
    return sock

def dump_payload(avps):
    for avp in avps:
        (name, value) = decodeAVP(avp)
        if name == 'Auth-Application-Id' or \
             name == 'Acct-Application-Id' or \
             name == 'Vendor-Specific-Application-Id':
            if isinstance(value, list):
                #~ print(value)
                _, value = value[0]
            if int(value) not in appids:
                Id = 'Unassigned'
            else:
                Id = appids[int(value)]
            print('Response:',name,'=',Id)
        elif name=='Supported-Vendor-Id':
            print('Response:',name,'=',dictVENDORcode2id(value))
        else:
           print('Response:',name,'=',value)
    
def next_session_id(config):
    #The Session-Id MUST be globally and eternally unique
    #<DiameterIdentity>;<high 32 bits>;<low 32 bits>[;<optional value>]
    now = datetime.datetime.now()
    ret = config['origin-host'] + ";"
    ret = ret + str(now.year)[2:4] + "%02d" % now.month + "%02d" % now.day
    ret = ret + "%02d" % now.hour + "%02d" % now.minute + ";"
    ret = ret + "%02d" % now.second + str(now.microsecond) + ";"
    ret = ret + config['origin-host'][2:16]
    return ret

def snd_rev(sock, msg, cmd, dst, dwa):
    if cmd == 257:
        sock.sendto(msg, dst)
    while(1):
        r = select.select([sock], [], [], 10)
        if r[0]:
            data = sock.recv(MSG_SIZE)        
            rmsg = HDRItem()
            stripHdr(rmsg, binascii.hexlify(data))
            if rmsg.appId == 0 and rmsg.cmd == 280 and rmsg.flags & DIAMETER_HDR_REQUEST > 0: #Device Watchdog request
                sock.sendto(dwa, dst)
                if not cmd == 257:
                    sock.sendto(msg, dst)
                continue            
            if rmsg.flags & DIAMETER_HDR_REQUEST > 0:
                continue
            if rmsg.cmd != cmd:
                continue
            return rmsg
        else:
            #logging.error("No answer recieved!")
            return None

def test_msg(sock, mod, config, args, verbose=True):
    dwa = Message(0, 280, [], [
            ("Result-Code", 2001),
            ("Origin-Host", config["origin-host"]),
            ("Origin-Realm", config["origin-realm"])]).generate()
    dwa = binascii.unhexlify(dwa)
    config['session-id'] = next_session_id(config)
    try:
        if isinstance(mod, Message):
            pkg = mod
        else:
            pkg = mod.create_pkg(config)
        cmd = pkg.cmd
        msg = pkg.generate()
    except Exception as e:
        print(bcolors.WARNING, "Failed to create", mod, ":", e)
        return -1
    res = snd_rev(sock, binascii.unhexlify(msg), cmd, (args.host, args.port), dwa)
    ret = None
    if not res is None:
        avps = splitMsgAVPs(res.msg)
        if verbose:
            dump_payload(avps)
        for avp in avps:
            (name, value) = decodeAVP(avp)
            if name == 'Result-Code':
                ret = int(value)
            elif name == 'Origin-Host':
                config['destination-host'] = value
            elif name == 'Origin-Realm':
                config['destination-realm'] = value
            elif name == 'Origin-State-Id':
                config["origin-state-id"] = value
    return ret

#                              ,|     
#                             //|                              ,|
#                           //,/                             -~ |
#                         // / |                         _-~   /  ,
#                       /'/ / /                       _-~   _/_-~ |
#                      ( ( / /'                   _ -~     _-~ ,/'
#                       \~\/'/|             __--~~__--\ _-~  _/,
#               ,,)))))));, \/~-_     __--~~  --~~  __/~  _-~ /
#            __))))))))))))));,>/\   /        __--~~  \-~~ _-~
#           -\(((((''''(((((((( >~\/     --~~   __--~' _-~ ~|
#  --==//////((''  .     `)))))), /     ___---~~  ~~\~~__--~ 
#          ))| @    ;-.     (((((/           __--~~~'~~/
#          ( `|    /  )      )))/      ~~~~~__\__---~~__--~~--_
#             |   |   |       (/      ---~~~/__-----~~  ,;::'  \         ,
#            o_);   ;        /      ----~~/           \,-~~~\  |       /|
#                   ;        (      ---~~/         `:::|      |;|      < >
#                  |   _      `----~~~~'      /      `:|       \;\_____// 
#            ______/\/~    |                 /        /         ~------~
#          /~;;.____/;;'  /          ___----(   `;;;/               
#         / //  _;______;'------~~~~~    |;;/\    /          
#        //  | |                        /  |  \;;,\              
#       (<_  | ;                      /',/-----'  _>
#        \_| ||_                     //~;~~~~~~~~~ 
#            `\_|                   (,~~ 
#                                    \~\ 
#                                     ~~ 

#   <=== BAD UNICORN HIPPOGRIFFIN, gonna eat all your mobile data!


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(dest='host', metavar='HOST')
    parser.add_argument("-p", help="Target port", type=int, dest="port", default=DIAMETER_PORT)
    parser.add_argument("-t", help="Choose the transport protocol", type=str, dest="transport", choices=["tcp", "sctp"], default="sctp")
    parser.add_argument("-c", help="Config file", type=str, dest="cfile", default="./diameter.cfg")
    parser.add_argument("-v", help="Be verbose", action="store_true", dest="verbose", default=False)
    parser.add_argument("-s", help="Skip initial CER", action="store_true", dest="skip_cer", default=False)
    parser.add_argument("-m", help="Only send designated message", type=str, dest="message", default=None)
    parser.add_argument("-a", help="Scan for supported applications", action="store_true", dest="appscan", default=False)
    
    args = parser.parse_args()
    
    #logging.basicConfig(level=logging.DEBUG)
    LoadDictionary("dictDiameter.xml")
    
    config = load_config(args.cfile)
    
    keys = msgs.keys()
    keys.sort()
    
    cer = msgs['CER']
    
    if args.transport == "tcp":
        stype = socket.SOCK_STREAM
    else:
        stype = socket.SOCK_SEQPACKET
    
    if not args.skip_cer:
        print(bcolors.BOLD, " === Initialy testing CER ===", bcolors.ENDC)
    
        sock = connect(stype, (args.host, args.port), None)
        ret = test_msg(sock, cer, config, args)
        sock.close()    
        if ret != 2001:
            print(bcolors.FAIL, ' *** ERROR ***', bcolors.ENDC)
            print('Check your config and see the diameter error message')
            print('Error was %d - %s' % (ret, err2msg(ret)))
            exit(2)
        else:
            print(bcolors.OKGREEN, ' === SUCCESS ===\n', bcolors.ENDC)
    
    if args.appscan:
        avps_exp = [("Origin-Host", config["origin-host"]),
                    ("Origin-Realm", config["origin-realm"]),
                    ("Destination-Host", config["destination-host"]),
                    ("Destination-Realm", config["destination-realm"])]
        avps_imp = [("Origin-Host", config["origin-host"]),
                    ("Origin-Realm", config["origin-realm"]),
                    ("Destination-Realm", config["destination-realm"])]

        #TODO: print origin-host der antwort
        for avps, txt in [(avps_exp, "explicit"), (avps_imp, "implicit")]:
            print(bcolors.BOLD, " === Scanning Application IDs with %s Destination-Host ===" % txt, bcolors.ENDC)
            for appid in appids:
                if appid == 0 or appid == 4294967295:   #Relay
                    flags = [DIAMETER_HDR_REQUEST]
                else:
                    flags = [DIAMETER_HDR_PROXIABLE, DIAMETER_HDR_REQUEST]
                msg = Message(appid, 0, flags, avps)
                sock = connect(stype, (args.host, args.port), None)
                ret = test_msg(sock, cer, config, args, False)
                if ret != 2001:
                    print(bcolors.FAIL, ' *** ERROR in CER ***', bcolors.ENDC)
                    print('Check your setup, as CERs worked initially.')
                    print('Error was %s: %s' % (ret, err2msg(ret)))
                    exit(2)
                ret = test_msg(sock, msg, config, args, args.verbose)
                sock.close()
                if ret == 3007 or ret == 3002:
                    if args.verbose:
                        print(bcolors.FAIL, ' *** Application %d (%s) unsupported (%d: %s) ***' % (appid, appids[appid], ret, err2msg(ret)), bcolors.ENDC)
                else:
                    print(bcolors.OKGREEN, ' === Application %d (%s) reachable (%d: %s) ===' % (appid, appids[appid], ret, err2msg(ret)), bcolors.ENDC)
            print("")
    else:
        for i in keys:
            if i == 'CER':
                continue
            if not args.message is None and args.message != i:
                continue
            
            print(bcolors.BOLD, ' === testing %s ===' % i, bcolors.ENDC)
            sock = connect(stype, (args.host, args.port), None)
            ret = test_msg(sock, cer, config, args, False)
            if ret != 2001:
                print(bcolors.FAIL, ' *** ERROR in CER ***', bcolors.ENDC)
                print('Check your setup, as CERs worked initially.')
                print('Error was %s: %s' % (ret, err2msg(ret)))
                exit(2)
            ret = test_msg(sock, msgs[i], config, args, args.verbose)
            
            sock.close()
            if ret == 2001 or (ret >= 5000 and ret < 6000):
                print(bcolors.OKGREEN, ' === SUCCESS ===\n', bcolors.ENDC)
            else:
                print(bcolors.FAIL, ' *** ERROR (%s: %s) ***\n' % (ret, err2msg(ret)), bcolors.ENDC)
    
    exit(0)
