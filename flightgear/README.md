# FlightGear extras

## FlightGear communication
My objective is to make Attitude work with the awesome, free, opensource simulator, [Flightgear](https://www.flightgear.org).

To make Attitude communicate with the simulator, we need to create a communication protocol. In the case of Attitude, I will be using a network connection (TCP at the moment, but will try UDP and see if it can work error free). Through the connection, the data will be sent from the simulator in JSON format, converted into a Python dictionary which will then be easily interpreted by Attitude's PFD.set_value().

Flightgear has a versatile way of outputting realtime information; We can create a [generic protocol](https://wiki.flightgear.org/Howto:Create_a_generic_protocol) that converts this output into a JSON string, sent over the network to Attitude.

## Assumptions

* This configuration was written based on the Cessna 172p model, the default Flightgear aircraft.
* Attitude in the example below, is running on the same computer as the simulator, so communication is established on 127.0.0.1 (localhost). It will make sense to be running Attitude on a separate computer (in my case it will be a Raspberry Pi on the dashboard of my simulator cockpit) in which case the correct address will have to be specified.

## Attitude's client instructions
Included in this directory is Attitude.xml, a FlightGear generic protocol file to achieve just that.

To use it, we need to copy Attitude.xml into FlightGear's data tree. In my debian system:

```
$ sudo cp Attitude.xml /usr/games/flightgear/Protocol
```

FlightGear also keeps a per-user configuration under ~/.fgfs but I've been unsuccessful in using this protocol file from there.

Once copied, we can invoke Attitude's client (net.py) which will be listening on port 12345. The screen starts with all instruments disabled.

Next, invoke FlightGear, as follows:

```
$ fgfs --generic=socket,out,10,127.0.0.1,12345,tcp,Attitude
```

Once the simulator loads, it will connect to Attitude and live data will drive the PFD.

Happy flying!