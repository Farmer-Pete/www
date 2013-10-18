Title: "Lease Does Not Exist" Error during HBase Export
Summary: While trying to do an HBase Export, here are some ways to fix the annoying "lease does not exist" errors.
Thumb: http://cdn.morguefile.com/imageData/public/files/k/kevinrosseel/preview/fldr_2008_11_28/file000597719214.jpg

Introduction
------------

While trying to do an [HBase](tag:HBase) Export vis [MapReduce](tag:MapReduce), I kept getting "lease does not exist" [errors](tag:error):

    2012-03-23 19:07:00,114 ERROR org.apache.hadoop.security.UserGroupInformation: PriviledgedActionException as:root (auth:SIMPLE) cause:org.apache.hadoop.hbase.regionserver.LeaseException: org.apache.hadoop.hbase.regionserver.LeaseException: lease '5896698310771141325' does not exist
    at org.apache.hadoop.hbase.regionserver.Leases.removeLease(Leases.java:230)
    at org.apache.hadoop.hbase.regionserver.HRegionServer.next(HRegionServer.java:1879)
    at sun.reflect.GeneratedMethodAccessor8.invoke(Unknown Source)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:25)
    at java.lang.reflect.Method.invoke(Method.java:597)
    at org.apache.hadoop.hbase.ipc.HBaseRPC$Server.call(HBaseRPC.java:570)
    at org.apache.hadoop.hbase.ipc.HBaseServer$Handler.run(HBaseServer.java:1039)

A temporary/quick [fix](tag:solution) was to increase the `hbase.regionserver.lease.period` and `hbase.rpc.timeout` settings in `hbase-site.xml` ( both values should be set to the same value )

`hbase.regionserver.lease.period`
:   HRegion server lease period in milliseconds. Clients must report in within this period else they are considered dead. ( Default is 1 minute )

`hbase.rpc.timeout`
:   The timeout for client RPC calls to [HBase](tag:HBase)

Notes
-----

* This is a **global** setting and that it requires a regionserver restart
* This is a temporary solution, we are currently modifying `org.apache.hadoop.hbase.mapreduce.Export` as a more permanent / reliable solution
