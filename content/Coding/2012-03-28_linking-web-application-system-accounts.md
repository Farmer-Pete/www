Title: Linking Web Application and System User Accounts
Summary: You might want to authenticate users logging into a web application against system user accounts. There is no straight forward way of doing this, but a small C utility helps to bridge this gap.
Thumb: http://cdn.morguefile.com/imageData/public/files/d/danielito/preview/fldr_2008_11_11/file0001792779106.jpg

The problem
------------

I built a [web development](tag:web_development) on a system in which users all had a [Linux](tag:Linux) system account. Instead of forcing users to maintain two usernames and [passwords](tag:password), I wanted the application to [authenticate](tag:security) against the system accounts. Unfortunately, there is no straightforward way to accomplish this. However, never fear! [C](tag:C) to the rescue! `:D`

The Solution
------------

After some digging, I [stumbled across this gem][spasswd.c]. I cleaned up and commented the code for better readability:

[spasswd.c]: http://www.php.net/manual/en/function.posix-getpwnam.php#16154

This script reads a username and password from standard input and then returns `0` if the username/password was valid and `1` if it was invalid.

    #!c
    /*************************
    * Source of spasswd.c
    *************************/
    #include <unistd.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <crypt.h>
    #include <shadow.h> 
    
    // Set up structures
    static char salt[12], user[128], pass[128]; 
    
    void initMem(void) {
        // Wipes used memory for security
        // by overwriting with nulls
        memset(salt, '\0', 12);
        memset(user, '\0', 128);
        memset(pass, '\0', 128);
    } 
    
    int main(int argc, char *argv[]) {
        struct spwd *passwd; 
         
        atexit(initMem); // Register cleanup function
        initMem(); // Initialize memory
     
        // Read in two values ( username &amp; password )
        if(fscanf(stdin, "%127s %127s", user, pass) != 2)  {
            return 1; // Problem with input
        }
     
        // Retrieve actual (encrypted) password from shadow
        if(!(passwd = getspnam(user))) {
            return 1; // Invalid user or could not open shadow (permissions problem)
        }
        
        // Encrypt password from stdin
        strncpy(salt, passwd->sp_pwdp, 11);
        strncpy(pass, crypt(pass, salt), 127); 
        
        // Compare encrypted password with one in shadow
        if(!strncmp(pass, passwd->sp_pwdp, 127)) {
            return 0; // Hurray! Password is the same
        }
         
        return 1; // Invalid password
    }

How to use this code
--------------------

To use:

1. Compile: `gcc -O2 -s -o spasswd -lcrypt spasswd.c`
2. Set permissions: `sudo chown root spasswd && sudo chmod u+s spasswd`

The `chmod` command will set the "[sticky bit][wp:sticky_bit]" allowing non-root users to use this tool.

<div class="warning">This is a potential security risk. This **will not** reveal passwords, but could potentially allow someone to launch a brute force attack in an attempt to crack an account password</div>

Here are some examples on how to use this utility in [Bash](tag:Bash), [Python](tag:Python), and [PHP](tag:PHP):

Bash
----

    #!/bin/bash
    
    username="buggs"
    password="bunny"
    spasswd="/usr/local/bin/spasswd"
    
    echo "$username $password" | $spasswd
    
    if [ $? -gt 0 ]; then
        echo "Password incorrect"
    else
        echo "Password correct"
    fi

Python
------

    #!python
    import subprocess
    
    username = 'buggs'
    password = 'bunny'
    spasswd = '/usr/local/bin/spasswd'
    
    handle = subprocess.Popen( [spasswd], stdin=subprocess.PIPE, shell=False )
    handle.communicate( str(username + ' ' + password).encode() )

    if not handle.wait():
        print( "Password correct" )
    else:
        print( "Password incorrect" )

PHP
---

    #!php
    <?php
    $username = 'buggs';
    $password = 'bunny';
    $spasswd = '/usr/local/bin/spasswd';

    $handle = popen( $spasswd, 'w' );
    fwrite( $handle, $username . ' ' . $password . "\n");

    if ( !pclose($handle) ) {
        echo "Password correct\n";
    } else {
        echo "Password incorrect\n";
    }

    ?>
