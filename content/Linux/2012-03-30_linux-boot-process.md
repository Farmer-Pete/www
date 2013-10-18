Title: The Linux Boot Process
Summary: I've been using Linux for years now and have messed with ( and sometimes messed up ) my GRUB configs. However, I've never really stopped to think about exactly what these entries mean ... and had no clue what vmlinuz or initramfs were or what the difference between them were. I did some digging and learned some really fascinating things.
Thumb: http://cdn.morguefile.com/imageData/public/files/w/wax115/preview/fldr_2004_12_11/file0001839156154.jpg

Introduction
-------------

I've been using [Linux](tag:Linux) for years now and have messed with ( and sometimes messed up ) my [GRUB][] `/boot/grub/menu.list`

However, I've never really stopped to think about exactly what these entries mean:

      # (0) Arch Linux
      title  Arch Linux
      root   (hd0,0)
      kernel /vmlinuz-linux cryptdevice=/dev/sda3:root root=/dev/mapper/root ro
      initrd /initramfs-linux.img
      
      # (1) Arch Linux
      title  Arch Linux Fallback
      root   (hd0,0)
      kernel /vmlinuz-linux cryptdevice=/dev/sda3:root root=/dev/mapper/root ro
      initrd /initramfs-linux-fallback.img

When I did stop to think about it ... I had no clue what `vmlinuz` or `initramfs` were or what the difference between them was.

First, some back-story
----------------------

When the computer first turns on, the BIOS initializes the hardware and then looks at the [Master boot record][] or [Volume boot record][] for a clue of what to do next. The [bootloader](tag:boot) ( [GRUB](tag:GRUB) ) installs itself in one of these two locations. This is where all the magic begins.

The Linux Kernel
----------------

Not surprisingly, `/vmlinuz-linux` is the [Linux kernel][] ( the "`kernel`" keyword was a good hint `:D` ). [Vmlinux][] ( vmlinuz is the zlib-compressed version of vmlinux ), not only contains the [Linux](tag:Linux) [kernel](tag:kernel) but also additional boot headers and setup routines to make the kernel bootable.

Initrd
-------

[Initrd][] ( **Initial** <strong>r</strong>am <strong>d</strong>isk ) is the core [file system](tag:file_system) ( stored as an image -- `initramfs-linux.img` on my system ) that [kernel](tag:kernel) loads first. After that, all the other file systems ( listed in `/etc/fstab` ) are mounted.

When I peaked into the initramfs, I was really surprised at what I saw. I always assumed everything was installed on the harddisk as part of the Linux installation, but it turns out that a lot of things are stored in initramfs.

Opening Initrd
--------------

Obviously this may be different for various distros, but here is how I looked inside of my initramfs:

First, some prep work ... we're going to create a safe place to work with the img file ... initramfs **really** isn't something you want to mess with `;)`

      mkdir /tmp/initramfs
      cp /boot/initramfs-linux.img /tmp/initramfs/initramfs-linux.img.gz # Put the .gz extension so we can extract it
      cd /tmp/initramfs
      gunzip initramfs-linux.img.gz

There is a chance that your initramfs won't be gzip compressed and can skip the `gunzip` phases. To check, run `file` and look at the result

      [linuxlefty@localhost] file /boot/initramfs-linux.img
      /boot/initramfs-linux.img: gzip compressed data, from Unix, last modified: Mon Mar 19 09:35:23 2012

Now feel free to peek inside with your favorite editor ([Vim](tag:Vim), of course). The first part is a bunch of [shell](tag:Bash) functions followed by the disk image.

Now, it's time to extract this puppy! ( you might need to install [cpio][] if it isn't already installed )

      cd /tmp/initramfs/
      cpio -i --make-directories < initramfs-linux.img

Now you can poke around and see what lives tucked inside `:)`

Obviously, there is **much** more to the [boot](tag:boot) process ... I'll save that for another time

[GRUB]: wp:GRUB
[Master boot record]: wp:Master_boot_record
[Volume boot record]: wp:Volume_boot_record
[Linux kernel]: wp:Linux_kernel
[Vmlinux]: wp:Vmlinux
[Initrd]: wp:Initrd
[cpio]: wp:cpio
