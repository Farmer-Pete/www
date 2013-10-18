Title: inotify: An Alternative to Busy Waiting / Polling
Summary: Monitoring a directory or file system for changes can be implemented by polling the directory over and and over again, waiting for changes ( also called a busy wait ) and is akin to a child asking "are we there yet?" over and over again. inotify provides a better alternative to this.
Thumb: http://cdn.morguefile.com/imageData/public/files/d/deanjenkins/preview/fldr_2004_12_02/file0001894206932.jpg

Are We There Yet?
-----------------

Anyone who travels with a small child has often heard the dreaded question repeated Ad nauseam: "Are We There Yet?". After about the fiftieth repetition a response along the lines of "No we're not. Don't ask me anymore. I'll tell you when we're there!" is retorted. Although we can easily see the foolishness of continually asking the same question again and again, sadly we fail to apply this concept to our [code](cat:coding).

For example, say we were writing a program that audited a directory and recorded all access and modifications to the files contained. One way would to use the following logic:

    current_state = get_directory_state()
    while FOREVER:
        new_state = get_directory_state()
        if new_state is not current_state:
            do_something( new_state )
            current_state = new_state

Which is basically the same thing as:

    while FOREVER:
        if are_we_there_yet?():
            do_something()

The process of asking "are we there yet?" over and over again is what we call [busy waiting][] or [polling][]. If you'd like to delve in further, reading about [Asynchronous I/O][] is a good place to start. Although this way works, it has [performance](tag:performance) (in the case of small poll times) and/or [latency](tag:latency) issues (in the case of large poll times).

[busy waiting]: wp:Busy_waiting
[polling]: wp:Polling_(computer_science)
[Asynchronous I/O]: wp:Asynchronous_I/O

The Better Alternative
----------------------

Instead of constantly asking "are we there yet?", it would be great if we could do something like the following:

    while FOREVER:
        directory_delta = sleep_until_directory_changes()
        do_something( directory_delta )

Fortunately ( for those on Linux ) we have something like this: [inotify][]. `inotify` watch the [file system](tag:file_system) and will block (i.e. stop the process) until there is something new for the program to process. I've coded several examples in [C/C++](tag:c), [python](tag:python) and [bash](tag:bash) as a launching point for your code `:)`. I've tried to add comments in an attempt to make things self-explanatory, but let me know if you have questions / comments.

[inotify]: http://linux.die.net/man/7/inotify

C++
---

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <string.h>
    #include <sys/inotify.h>
    
    #define EVENT_LEN ( sizeof( struct inotify_event ) )
    #define BUF_LEN ( 1024 * ( EVENT_LEN + 16 ) )
    
    
    char DIR_NAMES[100][100];
    
    void handler( struct inotify_event *event ) {
        char fType[100];
        char action[100];
    
        // Is it a file or a directory?
        if ( event->mask & IN_ISDIR ) {
            strcpy( fType, "directory" );
        } else {
            strcpy( fType, "file" );
        }
    
        // What event triggered?
        if (event->mask & IN_ACCESS)
            strcpy(action, "accessed");
        else if (event->mask & IN_ATTRIB)
            strcpy(action, "modified ( attributes )");
        else if (event->mask & IN_CLOSE_NOWRITE)
            strcpy(action, "closed after being open in read-only");
        else if (event->mask & IN_CLOSE_WRITE)
            strcpy(action, "closed after being open in read-write");
        else if (event->mask & IN_CREATE)
            strcpy(action, "created");
        else if (event->mask & IN_DELETE)
            strcpy(action, "deleted");
        else if (event->mask & IN_DELETE_SELF)
            strcpy(action, "deleted and is the watched directory/file");
        else if (event->mask & IN_MODIFY)
            strcpy(action, "modified");
        else if (event->mask & IN_MOVED_FROM)
            strcpy(action, "moved from watched directory");
        else if (event->mask & IN_MOVED_TO)
            strcpy(action, "moved into watched directory");
        else if (event->mask & IN_MOVE_SELF)
            strcpy(action, "moved and is the watched directory/file");
        else if (event->mask & IN_OPEN)
            strcpy(action, "opened");
        else if (event->mask & IN_UNMOUNT)
            strcpy(action, "on a filesystem which has just be unmounted");
        else {
            printf("Unknown event %#x", event->mask);
            return;
        }
    
        // Print out the info
        printf("The %s %s/%s was %s.\n", fType, DIR_NAMES[event->wd], event->name, action);
    }
    
    int main( int argc, char *argv[] ) {
    
        int inotify, i, wd;
        char buf[BUF_LEN];
        ssize_t numRead;
        char *p;
        struct inotify_event *event;
    
        if ( argc < 2 ) {
            // Usage information
            printf( "USAGE: %s pathname1 ... [pathnameN]\n", argv[0] );
            exit(1);
        }
    
        // Create inotify instance
        inotify = inotify_init();
    
        // For each pathname, set up an inotify watcher
        for ( i = 1; i < argc; i++ ) {
            wd = inotify_add_watch( inotify, argv[i], IN_ALL_EVENTS );
            strcpy(&DIR_NAMES[wd][0], argv[i]);
        }
    
        for (;;) {
            numRead = read(inotify, buf, BUF_LEN);
    
            // Process all of the events in buffer returned by read()
            for (p = buf; p < buf + numRead; ) {
                event = (struct inotify_event *) p; // retrieve the p'th event
                handler(event); // handle it
                p += EVENT_LEN + event->len; // point to next event
            }
        }
    }

To use this program:

compile
:    `gcc inotify.c`

example usage
:    `./a.out /tmp/directory1 /tmp/directory2`

Python
------

    #!/bin/python2
    import sys
    import pyinotify
    
    def handler(event):
    
    
        # Is it a file or directory?
        if event.dir:
            fType = "directory"
        else:
            fType = "file"
    
        # What event triggered?
        if event.maskname == "IN_ACCESS":
            action = "accessed"
        elif event.maskname == "IN_ATTRIB":
            action = "modified ( attributes )"
        elif event.maskname == "IN_CLOSE_NOWRITE":
            action = "closed after being open in read-only"
        elif event.maskname == "IN_CLOSE_WRITE":
            action = "closed after being open in read-write"
        elif event.maskname == "IN_CREATE":
            action = "created"
        elif event.maskname == "IN_DELETE":
            action = "deleted"
        elif event.maskname == "IN_DELETE_SELF":
            action = "deleted and is the watched directory/file"
        elif event.maskname == "IN_MODIFY":
            action = "modified"
        elif event.maskname == "IN_MOVED_FROM":
            action = "moved from watched directory"
        elif event.maskname == "IN_MOVED_TO":
            action = "moved into watched directory"
        elif event.maskname == "IN_MOVE_SELF":
            action = "moved and is the watched directory/file"
        elif event.maskname == "IN_OPEN":
            action = "opened"
        elif event.maskname == "UNMOUNT":
            action = "on a filesystem which has just be unmounted"
        else:
            print "Unknown event: %s" % event.maskname
            return
    
        # Print out the info
        print "The %s %s was %s." % (fType, event.path, action)
    
    if __name__ == "__main__":
    
        # Usage information
        if len(sys.argv) < 2:
            print "USAGE: %s pathname1 ... [pathnameN]" % sys.argv[0]
            exit(1)
    
        # Create inotify instance
        inotify = pyinotify.WatchManager()
    
        # For each pathname, set up an inotify watcher
        for path in sys.argv[1:]:
            inotify.add_watch(path, pyinotify.ALL_EVENTS)
    
        # Register event handler
        notifier = pyinotify.Notifier(inotify, handler)
     
        # Read events forever
        notifier.loop()

Requirements
:     [inotify](https://github.com/seb-m/pyinotify/wiki)

example usage
:    `python2 inotify.py /tmp/directory1 /tmp/directory2`

BASH
----

    #!/usr/bin/bash
    function handler {
    
        while IFS=' ' read rootPath event fileName; do
    
            IFS=',' eventMask=( $event )
    
            # Is it a file or directory?
            if [ ${#eventMask[@]} -gt 1 ] && [ ${#eventMask[1]} == 'ISDIR' ]; then
                fType="directory"
            else
                fType="file"
            fi
    
            watchEnd=False
    
            # What event triggered?
            case ${eventMask[0]} in
                "ACCESS")
                    action="accessed" ;;
                "ATTRIB")
                    action="modified ( attributes )" ;;
                "CLOSE_NOWRITE")
                    action="closed after being open in read-only" ;;
                "CLOSE_WRITE")
                    action="closed after being open in read-write" ;;
                "CREATE")
                    action="created" ;;
                "DELETE")
                    action="deleted" ;;
                "DELETE_SELF")
                    action="deleted and is the watched directory/file";;
                "MODIFY")
                    action="modified" ;;
                "MOVED_FROM")
                    action="moved from watched directory" ;;
                "MOVED_TO")
                    action="moved into watched directory" ;;
                "MOVE_SELF")
                    action="moved and is the watched directory/file";;
                "OPEN")
                    action="opened" ;;
                "UNMOUNT")
                    action="on a filesystem which has just be unmounted";;
                *)
                    echo "Unknown event: ${eventMask[0]}"; return ;;
            esac
    
            # Print out the info
            echo "The $fType $rootPath$fileName was $action."
    
        done
    }
    
    if [ $# -lt 1 ]; then
        # Usage information
        echo "USAGE: $0 pathname1 ... [pathnameN]"
        exit 1
    fi
    
    inotifywait -qm $@ | handler

requirements
:    [inotify-tools](https://github.com/rvoicilas/inotify-tools/wiki/)

example usage
:    `./inotify.sh /tmp/directory1 /tmp/directory2`
