Title: Pushing SSH Keys Programmatically
Summary: SSH is the de facto tool for remote terminals. SSH keys make logging in breeze, but how do you distribute the SSH keys? Setting up keys doesn't take that long, but things get complicated with a large cluster and many users. Being unable to find an easy way to do this, I wrote my own.
Thumb: http://cdn.morguefile.com/imageData/public/files/m/missyredboots/preview/fldr_2008_11_28/file000972175181.jpg

The missing link in SSH
-----------------------

[Secure Shell][ssh] is a secure replacement for [telnet][]. Not only is transmitted data [encrypted](tag:encryption), but it also supports [public and private keys][ppg]. This allows you authorize specific users to log in remotely (and [securely](tag:security)) with a key rather than a [password](tag:password) ([tutorial][ppg-tutorial]); a privilege that can be easily revoked.

This is all good and well, but how do you distribute the [SSH keys](tag:keys)? Setting up keys doesn't take that long, but when you have an entire cluster of servers things get more complicated. When you have a cluster full of users unfamiliar with [SSH](tag:SSH), who want to be able to set up their own keys, things get even more complicated.

I searched for an easy way to do this. Some people accomplished this via [Expect][], but I wanted a tool that was simple to use and deploy with minimal requirements. Unable to find a satisfactory solution, I wrote my own `:)`. The only dependency for this script is [sshpass][], a wrapper for SSH and [scp][]. Consult your package manger; packages are available for most [Linux](tag:linux) distributions.

[expect]: wp:Expect
[ppg-tutorial]: http://oreilly.com/pub/h/66
[ppg]: wp:Public-key_cryptography
[scp]: wp:Secure_copy
[sshpass]: http://sourceforge.net/projects/sshpass
[ssh]: wp:Secure_Shell
[telnet]: wp:telnet

Bash goodness
-------------

Without further adieu,

    #!/bin/bash
    
    # Configure a list of hostnames or IP address separated by whitespace
    HOSTS=( )
    
    # Check to see if sshpass is installed
    which sshpass > /dev/null 2&>1 || ( echo "FATAL: sshpass is not installed"; exit )
    
    # Get password from user
    read -s -p "password for $(whoami): " SSHPASS
    export SSHPASS

    # Generate SSH key if needed
    if ! [ -f ~/.ssh/id_dsa ] && ! [ -f ~/.ssh/id_dsa.pub ]; then
        mkdir -p ~/.ssh
        ssh-keygen -b 1024 -f ~/.ssh/id_dsa -t dsa -P '' -C ''
    fi

    for host in ${HOSTS[@]}; do
        echo "Installing key on $host ..."
        # Copy ssh key over to remote server
        sshpass -e scp -o StrictHostKeyChecking=no ~/.ssh/id_dsa.pub $host:

        # Now put it into authorized_keys and set permissions
        sshpass -e ssh $host 'mkdir -p ~/.ssh; touch ~/.ssh/authorized_keys; cat id_dsa.pub ~/.ssh/authorized_keys | sort | uniq > $$; mv $$ ~/.ssh/authorized_keys; chmod 700 ~/.ssh; chmod 600 ~/.ssh/*; rm id_dsa.pub'

        ssh $host "echo '    key sucessfully installed on $host'"

    done

The only configuration you will need to set is the `HOSTS` variable. Note that the hosts/IPs (as a [Bash](tag:bash) array) should be separated by **whitespace**, not a comma. For example:

    #!bash
    HOSTS=(
        LinuxLefty-1
        LinuxLefty-2
        LinuxLefty-3
        LinuxLefty-4
        LinuxLefty-5
        LinuxLefty-6
        LinuxLefty-7
    )

Explaining the code
--------------------

A quick explanation of what is going on:

<div class="code" markdown=1>

Line 10, 11
:     prompts the user for their [password](tag:password) ( which will be used to log in and establish the keys ). The `-s` option disables echoing of what the user is typing ( standard for UNIX password prompts ). The `SSHPASS` variable is exported so that sshpass can read it later ( a little more [secure](tag:security) than putting it on the command line ).

Line 14 - 17
:     checks to see if a [DSA](wp:Digital_Signature_Algorithm) key already exists. If not, one is created

Line 22
:     scp (wrapped by sshpass) distributes the [public key](tag:keys) to the remote servers. The `-o StrictHostKeyChecking=no` prevents ssh/scp from prompting to accept the host if it is unknown.

Line 25
:     ssh (wrapped by sshpass) logs in to install the key. There is a lot of stuff going on (to minimize the number of ssh connections required). There is a breakdown below.

Line 27
:     finally, we log in without the sshpass wrapper. We should just see the echoed message. If a password prompt appears, something is wrong. Either there is a problem with how the keys were installed or how the SSH server is configured.

</div>

As promised, here is breakdown of line 25:

    #!bash
    mkdir -p ~/.ssh
    touch ~/.ssh/authorized_keys
    cat id_dsa.pub ~/.ssh/authorized_keys | sort | uniq > $$
    mv $$ ~/.ssh/authorized_keys
    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/*
    rm id_dsa.pub

<div class="code" markdown=1>

Line 1, 2
:     creates the `.ssh/` directory and `authorized_keys` file

Line 3, 4
:     adds our public key to the [authorized keys](tag:keys) and remove and duplicates, just in case it was previously added. Two lines are needed since you can't write to a file while you're reading from it (or bad things will happen to the file). `$$` is the PID of the script. I'm using it as a name of a temporary file that has a very low probability clobbering an existing file.

Line 5, 6
:     sets the correct permissions. Some [SSH servers](tag:SSH) will ignore `authorized_keys` otherwise.

Line 7
:     clean up the temporary file we scp'd over

</div>

Note
----

You can safely ignore any warnings such as:

    #!text
    Warning: Permanently added 'LinuxLefty-1,192.16.74.10' (RSA) to the list of known hosts

[SSH](tag:SSH) is just letting you know that it adding a known host instead of prompting you (which is what we want). This is a result of the `-o StrictHostKeyChecking=no` we are passing to SSH on line 25.

That's it :) Hopefully someone finds this useful!
