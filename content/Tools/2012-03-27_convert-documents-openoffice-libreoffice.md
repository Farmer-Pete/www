Title: Converting files with LibreOffice ( OpenOffice )
Summary: Converting document formats is a common and difficult task. LibreOffice's document conversion is getting better all the time and it is possible to harness this power for batch conversion
Thumb: https://upload.wikimedia.org/wikipedia/commons/a/ad/LibreOffice_Writer.png

The script
-----------

This [Bash](tag:Bash) script will convert to and from any format supported by [OpenOffice](tag:OpenOffice)/[LibreOffice](tag:LibreOffice) via the command line. It leverages the awesome [JODConverter](http://www.artofsolving.com/opensource/jodconverter) which you'll need to have installed.

And now for the script:

    #!/bin/bash
    
    ## Written by LinuxLefty ##
    
    ########################################
    ## Takes 2 comand line arguments:
    ##    [1]: The file to be converted
    ##    [2]: Where to save the conveted file to
    ########################################
    
    ## Start OpenOffice if it's not already running
    
    echo "Command: $0 $1 $2";

    echo "Welcome!";
    echo "Checking to see if soffice is running...";

    if pgrep -u `whoami` soffice.bin; then
    echo "Soffice found!";
    else
    echo "soffice is not running....";
    exit 1;
    fi
    
    echo "soffice is running, checking to see if port 8100 is open...";
    
    ## Check to see if port 8100 is open. That is how we'll know that soffice is up and ready to run
    counter=0
    while ! nmap -p 8100 localhost | grep "8100/tcp open" ; do
    echo "Checking...";
    sleep 1s;
    counter=$(($counter + 1));
    if (( $counter &gt; 5 )); then
        echo "Giving up...";
        exit 1;
    fi
    done
    
    echo "It is!";
    echo "Now attempting to start off java conversion";
    
    ## Now kick of the conversion
    /opt/java/jre/bin/java -jar /usr/local/bin/JODConverter/jodconverter-cli-2.2.2.jar $1 $2 2&gt;&amp;1
    
    echo "All done!";</pre>]]></content:encoded>


Note
----

[OpenOffice](tag:OpenOffice)/[LibreOffice](tag:LibreOffice) must first be started in listening mode <!-- this would be a great place for a sidenote! -->

    /usr/bin/soffice -accept="socket,port=8100;urp;"

