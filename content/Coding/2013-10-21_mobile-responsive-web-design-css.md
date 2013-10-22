Title: Mobile-ready, Responsive Web Design With CSS
Thumb: http://cdn.morguefile.com/imageData/public/files/k/kolobsek/03/l/1363266068ypiy4.jpg
Summary: Just when I was starting to get comfortable with web design, I started learning more about mobile/responsive designs (I'm a little behind the times). It was a little rough at first, but seeing the site dynamically change without JavaScript is like pure magic `^_^`

Background
==========

I know that [smart phones](tag:mobile) have been out for ages and that it really shouldn't have taken me so long to learn how to [develop websites](tag:web_development) for them. However, as I'm still rocking my [dumb phone](tag:old_school), I kinda forgot about an entire segment of visitors `>_<`. So I finally took the plunge and attempted to make my website mobile ready and [responsive](tag:responsive) (making your website "respond" to changes in browser dimensions).

Here are a couple of things I learned along the way :)

Dumb phone, smart PC
====================

To make [LinuxLefty](/) mobile-ready, I would obviously need a mobile phone for testing. There are websites that claim to provide a mobile preview, but most (all?) of those simply use a mini-iframe. They may have the dimensions, but they don't give you a true idea of how to mobile browser will render your site.

However, I wasn't about to run out and purchase a new phone and a data plan just so I could test my website. Fortunately, I came across [AndroVM](http://www.androvm.org) which provides android [VirtualBox](http://www.virtualbox.org) images. Using this, I was able to run [android](tag:android) in a [virtual machine](tag:virtualization).

The Magic Meta
==============

When I first started making changes to my site, I was confounded as to why it was always displayed zoomed out in mobile devices and would always scroll by default, even though it wouldn't scroll on a small, resized [browser](tag:web_browser) (an example of why it's important to have access to a mobile device when developing).

Finally, I found the magic sauce in the form of a [meta tag](tag:meta_data):

    #!html
    <meta name="viewport" content="width=device-width initial-scale=1.0, user-scalable=yes">

By default, websites are rendered with a width that device vendors have decided is optimal. The meta tag, however, forces the browser to render your site with a width optimized for the device, with no scrolling or zooming by default (although the user is free to zoom if they wish).

Max-Width Is Your Friend
========================

Wherever you are specifying a `width`, make sure you have a `max-width: 100%` set. This will set the default width of an element but then force it to shrink when it would otherwise break the layout.

Media Queries are Awesome
=========================

`CSS` provides `@media` queries which allow you to earmark certain segments of your `CSS` to only be effective for browsers of specific dimensions. The two main settings you need to remember are `max-width` and `min-width`.

min-width
:   The contained CSS will only be effective for screen resolutions **larger** than the specified width (you are providing the *smallest* allowed screen width which will still activate these styles)

max-width
:   Conversely, the contained CSS will only be effective for screen resolutions **smaller** than the specified width (you are providing the *largest* allowed screen width which will still active these styles)

### Example ###

Here is some sample CSS which provides a three-column layout for screens larger than 800px. Any smaller, they will be displayed as a vertical stack.

    #!css
    .column {
        width: 33%;
        float: left;
    }

    @media {max-width:800px} {
        .column {
            width: 100%;
            float: none;
        }
    }

Note that we could have put everything inside a `@media` query. However, it's best practice (I think) to lay down your base styles first and then layer responsive/mobile styles on top as `@media` queries.
