Title: SSH Tunneling
Tags: proxy, network, ssh, socks, tunneling
Summary: A vehicular tunnel provides a way for cars to pass through otherwise impenetrable or unsafe terrain (such as rock or water). Likewise, a network tunnel provides access to a resource blocked by a firewall and supplies a secure way to pass through an untrusted/unsafe network.
Thumb: http://cdn.morguefile.com/imageData/public/files/j/jdurham/preview/fldr_2009_02_05/file9301233877792.jpg

A Quick Socket Intro
--------------------

A _socket_ is a "pipe" between two computers that is used to exchange [data](tag:data). Let's say, for example, that you open your [web browser](tag:web) and navigate to `http://www.example.com/index.html`.
Your browser connects to `example.com` (this action is called "opening a [socket](tag:socket) connection") and establishes a two way "pipe" between that server and your computer. Then you
are able to send a request for the page `index.html` and then the server sends back the contents of the page.

<graphviz filter="dot">
    digraph {
        rankdir=LR;

        computer -> example_com [label="socket"]

        computer [label="Your Computer"]
        example_com [label="http://www.example.com"]
    }
</graphviz>

Using Mainly Spoons ...
-----------------------

What if you have a [firewall](tag:firewall) that blocks `HTTP` access to `www.example.com`, but allows you to `SSH` to `www.linuxlefty.com`?

What if accessing `www.example.com` requires you to use an insecure network, but `www.linuxlefty.com` can access that site [securely](tag:encryption)?

Wouldn't it be nice if you could have `linuxlefty.com` transport the data and broker the connection between you and `example.com`?
Fortunately, you can, and this is called a "[tunnel](tag:tunnel)".

<graphviz filter="dot">
    digraph {
        rankdir=LR

        computer [label="Your Computer"]

        subgraph cluster_0 {
            linuxlefty [label="    ssh://linuxlefty.com    ", shape="component"]
            label = "SSH Tunnel"
        }

        example_com [label="http://www.example.com"]

        computer -> linuxlefty [label="socket"]
        linuxlefty -> example_com [label="socket"]
        computer -> example_com [style="dashed"]
    }
</graphviz>

Port Forwarding
---------------

The simplest way to create a tunnel is via [port forwarding](tag:port_forwarding). You'll need to know the following information:

  * The local port that you want to bind to (this is the "side" of the tunnel that resides on your computer)
  * The remote destination and port you want to connect to (this is other side of the tunnel)
  * The server and login for the server that will be brokering the tunnel

For our previous example, this could be:

  * Local port: `12345` (This could be any port as long as it is unused)
  * Remote destination: `www.example.com:80` (Port `80` is the default port for `HTTP`)
  * Tunnel broker: `linuxlefty.com`, username: `peter`, password: `abc123`

### Forwarding a single port ###

To set up the port forwarder using [OpenSSH](tag:ssh), you can use the following command:

    #!bash
    ssh -N -f -L $LOCAL_PORT:$REMOTE_DESTINATION $TUNNEL_BROKER

For our toy example above, our command would be:

    #!bash
    ssh -N -f -L 12345:www.example.com:80 peter@linuxlefty.com

Here's a breakdown of the command:

-N
:     Don't open a remote shell (you don't need to run any commands), just set up the port forwarder

-f
:     Run the port forwarder in the background

-L
:     The flag used to create the port forwarder

12345
:     The local port that you will connect to

www.example.com:80
:     Remote target destination (80 is the standard port for web servers)

peter@linuxlefty.com
:     The SSH username and hostname for the tunnel broker (ssh will prompt you for your password if you don't have keys set up)


### Connecting to our port forwarder ###

Now you can fire up your web browser, but instead of connecting to `www.example.com`, you connect to `localhost:12345`.
Remember, you connect to your local machine since that's where the port forwarder resides, it forwards your traffic to the target host

SOCKS Proxy
-----------

The above method works well for a single (maybe a handful) of ports and hosts. However, soon it becomes quite burdensome
and inconvenient. Wouldn't it be nice if you could create a single tunnel that could be reused for any port on any host?

Enter the [SOCKS](wp:SOCKS) (**Sock**et **S**ecure) proxy.

<graphviz filter="dot">
    digraph {
        rankdir=LR

        computer [label="Your Computer"]

        subgraph cluster_0 {
            linuxlefty [label="    ssh://linuxlefty.com    ", shape="component"]
            label = "SOCKS Proxy"
        }

        example_com [label="http://www.example.com"]
        facebook_com [label="http://www.facebook.com"]
        twitter_com [label="http://www.twitter.com"]
        pinterest_com [label="http://www.pinterest.com"]

        computer -> linuxlefty
        linuxlefty -> example_com
        linuxlefty -> facebook_com
        linuxlefty -> twitter_com
        linuxlefty -> pinterest_com
    }
</graphviz>

To create a socks [proxy](tag:proxy) using OpenSSH, you can use the following command:

    #!bash
    ssh -N -C -f -D 0.0.0.0:$LOCAL_PORT $TUNNEL_BROKER

### Just for you ###

Re-using our previous example of the following settings:

  * Local port: `12345` (This could be any port as long as it is unused)
  * Remote destination: `www.example.com:80` (Port `80` is the default port for `HTTP`)
  * Tunnel broker: `linuxlefty.com`, username: `peter`, password: `abc123`

We get the following command:

    #!bash
    ssh -N -f -D localhost:12345 peter@linuxlefty.com

Here's a breakdown of the command:

-N
:     Don't open a remote shell (you don't need to run any commands), just set up the port forwarder

-f
:     Run the port forwarder in the background

-D
:     Create a SOCKS proxy (`-D` is for **D**ynamic)

localhost:12345
:     The local port that you will be connecting to. Note that entering `localhost` means only you will be able to connect to this proxy (others connecting to your computer can't).

### Connecting to the SOCKS proxy ###

Now, configure your browser to use your [SOCKS proxy](tag:proxy) (host=`localhost`, port=`12345`) and you can browse to any site you wish too, sending all traffic through your tunnel broker.

### Other useful commands ###

Here are a few variations of our SOCKS proxy command that you might find useful `:)`

    #!bash

    # Share your SOCKS proxy with the world
    ssh -N -f -D 0.0.0.0:12345 peter@linuxlefty.com

    # Like the above but compress all network traffic (-C)
    ssh -N -f -C -D 0.0.0.0:12345 peter@linuxlefty.com

    # Be a SOCKS proxy and tunnel broker yourself
    ssh -N -f -D 0.0.0.0:12345 localhost

