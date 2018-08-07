# diameter_enum

A diameter Application and service scanner.

The tool tries to implements most of the diameter messages defined either in one of the RFCs or by 3GPP and uses them to check the answering behaviour of an Diameter service.
This can be used to verify the configuration of a Diameter service or a Diameter proxy/firewall and ensure the security of the Diameter setup.
The tool can also be used to gather topology information of a foreign diameter realm.

## Running

The tool is build around libDiameter from [pyprotosim](https://github.com/thomasbhatia/pyprotosim) and therefore uses python2, you will also need the backport for [py3-configparser](https://pypi.org/project/configparser/).

To run the tool you will need at least a valid configuration file and a destination host running a Diameter service. In default SCTP will be used to transport Diameter, this can be changed to TCP via the *-t* commandline switch.
In default the IANA Diameter port 3868 will be used, any other port can be selected via the *-p* switch. If only a single message should be probed, the message can be selected via the *-m* switch, where the parameter is the name of the file in ./msgs/.

```
$ ./diameter_enum.py -h
usage: diameter_enum.py [-h] [-p PORT] [-t {tcp,sctp}] [-c CFILE] [-v] [-s]
                        [-m MESSAGE] [-a]
                        HOST

positional arguments:
  HOST

optional arguments:
  -h, --help     show this help message and exit
  -p PORT        Target port
  -t {tcp,sctp}  Choose the transport protocol
  -c CFILE       Config file
  -v             Be verbose
  -s             Skip initial CER
  -m MESSAGE     Only send designated message
  -a             Scan for supported applications
```

## Configuration

The configuration file defiles the values written to the Diameter header like the origin and destination host and realm, as well as values for specific AVPs like the MCC, MNC or IMSI for 3GPP messages.

```
[DEFAULT]
origin-host: vanir
origin-realm: vanir
destination-host: baldr.midgard
destination-realm: midgard
host-ip-address: 127.0.0.1
vendor-id: 0
product-name: denum
inband-security-id: 0
disconnect-cause: 2
auth-application-id:
re-auth-request-type: 0
accounting-record-type: 1
accounting-record-number: 0

auth-request-type: 1
mnc: 001
mcc: 001
imsi: 0010012345678
plmnid: 12f345
msisdn: 12345678
imei: 9876543210
```

Further different values can be used for the 3GPP interfaces S6A, SH and SLH. An example configuration file with all possible values is supplied with the tool.

## Application Scan

To see which applications are supported by the remote diameter service, a message with the command code 0 (always invalid) will be sent to all known (by means of IANA, see appids.csv) application IDs. If the targeted application is supported by the target service, the answer *COMMAND_UNSUPPORTED* will be replied.
The scan will be performed two times, first with the AVP Destination-Host set and afterward with in implicit Destination-Host, meaning no Destination-Host AVP will be supplied. The first scan will target only on single Diameter instance, while the second one targets the whole realm and might reveal more services. 

```
$ ./diameter_enum.py -a 127.0.0.1
  === Initialy testing CER === 
Response: Result-Code = 2001
Response: Origin-Host = baldr.midgard
Response: Origin-Realm = midgard
Response: Origin-State-Id = 1533029326
Response: Host-IP-Address = 127.0.0.1
Response: Vendor-Id = 0
Response: Product-Name = freeDiameter
Response: Firmware-Revision = 10201
Response: Acct-Application-Id = Diameter base accounting [RFC6733]
Response: Auth-Application-Id = Diameter Session Initiation Protocol (SIP) Application [RFC4740]
Response: Auth-Application-Id = Relay [RFC6733]
  === SUCCESS ===
 
  === Scanning Application IDs with explicit Destination-Host === 
  === Application 0 (Diameter common message [RFC6733]) reachable (3001: DIAMETER_COMMAND_UNSUPPORTED) === 
  === Application 3 (Diameter base accounting [RFC6733]) reachable (3001: DIAMETER_COMMAND_UNSUPPORTED) === 
  === Application 6 (Diameter Session Initiation Protocol (SIP) Application [RFC4740]) reachable (3001: DIAMETER_COMMAND_UNSUPPORTED) === 

  === Scanning Application IDs with implicit Destination-Host === 
  === Application 0 (Diameter common message [RFC6733]) reachable (3001: DIAMETER_COMMAND_UNSUPPORTED) === 
  === Application 3 (Diameter base accounting [RFC6733]) reachable (3001: DIAMETER_COMMAND_UNSUPPORTED) === 
  === Application 6 (Diameter Session Initiation Protocol (SIP) Application [RFC4740]) reachable (3001: DIAMETER_COMMAND_UNSUPPORTED) === 


```

## Command Probing

To see which commands are available on the exposed Diameter applications, the tool generates a probe message for all implemented commands. The message will be enriched with the data from the configuration file and sent to the target host/realm. The answer is displayed and in the case of an error the error message is decoded.

```
$ ./diameter_enum.py 127.0.0.1
  === Initialy testing CER === 
Response: Result-Code = 2001
Response: Origin-Host = baldr.midgard
Response: Origin-Realm = midgard
Response: Origin-State-Id = 1533029326
Response: Host-IP-Address = 127.0.0.1
Response: Vendor-Id = 0
Response: Product-Name = freeDiameter
Response: Firmware-Revision = 10201
Response: Acct-Application-Id = Diameter base accounting [RFC6733]
Response: Auth-Application-Id = Diameter Session Initiation Protocol (SIP) Application [RFC4740]
Response: Auth-Application-Id = Relay [RFC6733]
  === SUCCESS ===
 
  === testing AAR === 
  *** ERROR (3001: DIAMETER_COMMAND_UNSUPPORTED) ***
 
  === testing ACR === 
  === SUCCESS ===
 
  === testing AIR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing AMR === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing ASR === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing BIR_3GPP === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing CCR === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing CLR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing DER === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing DPR === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing DSR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing DWR === 
  === SUCCESS ===
 
  === testing ECR_3GPP === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing HAR === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing IDR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing LIR === 
  === SUCCESS ===
 
  === testing LIR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing LRR_3GPP === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing MAR === 
  === SUCCESS ===
 
  === testing MAR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing MPR_3GPP === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing NOR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing PLR_3GPP === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing PNR_3GPP === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing PPR === 
  === SUCCESS ===
 
  === testing PPR_3GPP === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing PUR_2_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing PUR_3GPP === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing RAR === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing RIR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing RSR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing RTR === 
  === SUCCESS ===
 
  === testing RTR_3GPP === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing SAR === 
  === SUCCESS ===
 
  === testing SAR_3GPP === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing SIR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing SNR_3GPP === 
  *** ERROR (3007: DIAMETER_APPLICATION_UNSUPPORTED) ***
 
  === testing SRR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing UAR === 
  === SUCCESS ===
 
  === testing UAR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing UDR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
  === testing ULR_3GPP === 
  *** ERROR (3002: DIAMETER_UNABLE_TO_DELIVER) ***
 
```

This mode in combination with the *-t* commandline switch can be used to send single Diameter commands to a given realm/host. For special cases certain AVPs might be added, removed or changed in the generated probe packets by editing the probe definition in the msgs folder.
