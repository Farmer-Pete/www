Title: SSH Tunneling
Tags: proxy, network, ssh, socks, tunneling
Summary: A vehicular tunnel provides a way for cars to pass through otherwise impenetrable or unsafe terrain (such as rock or water). Likewise, a network tunnel provides access to a resource blocked by a firewall and supplies a secure way to pass through an untrusted/unsafe network.
Thumb: 
Status: draft

A Quick Socket Intro
====================

A _socket_ is a "pipe" between two computers that is used to exchange data. Let's say, for example, that you open your web browser and navigate to `http://www.example.com/index.html`.
Your browser connects to `example.com` (this action is called "opening a socket connection") and establishes a two way "pipe" between that server and your computer. Then you
are able to send a request for the page `index.html` and then the server sends back the contents of the page.

                     Socket
    [Your Computer]<-------->[http://www.example.com]

Using Mainly Spoons ...
=======================

What if you have a firewall that blocks `HTTP` access to `www.example.com` but allows you to `SSH` to `www.linuxlefty.com`? Wouldn't it be nice if you could have `linuxlefty.com` transport
the data and broker the connection between you and `example.com`? Fortunately, you can, and this is called a "tunnel".

                     Socket                         Socket
    [Your Computer]<------->[ssh://linuxlefty.com]<------->[http://www.example.com]
                  |                                        |
                  |----------------------------------------|
                                   Tunnel

Port Forwarding
===============

The simplest way to create a tunnel is via port forwarding. You'll need to know the following information:

  * The local port that you want to bind to (this is the "side" of the tunnel that resides on your computer)
  * The remote destination and port you want to connect to (this is other side of the tunnel)
  * The server and login for the server that will be brokering the tunnel

For our previous example, this could be:

  * Local port: `12345` (This could be any port as long as it is unused)
  * Remote destination: `www.example.com:80` (Port `80` is the default port for `HTTP`)
  * Tunnel broker: `linuxlefty.com`, username: `peter`, password: `abc123`

To set up the port forwarder using OpenSSH, you can use the following command:

            "-L" is the flag used to create a port forwarder
           /   The local port          Run the port forwarder in the background
          /   /                       /     username  host that will be brokering the tunnel
         /   /                       /     /         /
    ssh -L 12345:www.example.com:80 -f -N peter@linuxlefty.com
                 |----------------|     \
                 Remote destination      Don't open a remote shell, just set up for port forwarder

