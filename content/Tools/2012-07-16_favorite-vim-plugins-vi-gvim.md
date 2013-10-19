Title: A Dozen Favorite Vim Plugins
Summary: I love Vim. I've used it for years and I still feel like I'm just scratching the surface of this tool. One thing that makes Vim so great is its plugins. In this post I'll talk about a few of my favorites.
Thumb: http://www.elfnet.org/wp-content/uploads/2011/10/Vim_logo.png

Introduction
------------

I love [Vim][]. I've used it for years and I still feel like I'm just scratching the surface of this tool. I'll part with my browser, I'll switch [shells][zsh], and if work requires it, I'll even begrudgingly relinquish my [operating system](tag:Linux) (heresy!) ... but you'll have to pry my editor from my cold, dead hands.

Sorry, got carried away there. `:)` Anyhow, one thing that makes [Vim](tag:Vim) so great is its [plugins][]. Recently I came across some really fantastic [plugins](tag:plugins) which have really enhanced my Vim experience. Although there are so many to choose from, I'm only listing ones that I use on a regular basis.

1: Pathogen
------------

### Overview ###

One of the frustrations I've had in the past with [Vim's](tag:Vim) plugins is that things get really messy, really fast. Files get scattered all throughout the `~/.vim` directory and trying to keep track of what plugins you have installed is a chore. [Pathogen][] comes to the rescue by organizing everything into _bundles_. Everything goes neatly into their own directory inside of `~/.vim/bundles`. In addition, since everything is in its own directory, you can easily pull things down via [git](tag:git). Then updating all your plugins can be done with the tiny [bash](tag:Bash) script listed below. _Beautiful_.

    #!bash
    for dir in ~/.vim/bundle/*; do
        pushd $dir
        git pull
        popd
    done

### Installation ###

    #!bash
    mkdir -p ~/.vim/autoload ~/.vim/bundle
    curl -so ~/.vim/autoload/pathogen.vim \
        https://raw.github.com/tpope/vim-pathogen/master/autoload/pathogen.vim

And to enable it, put `call pathogen#infect()` in your `~/.vimrc` file. That's it `:)`

**Project Page:** [https://github.com/tpope/vim-pathogen](https://github.com/tpope/vim-pathogen)

__Note: All other installation instructions will assume that you have pathogen installed.__

2: Ctrl-P
----------

### Overview ###

A lot of people really love [Command-T][]. It (supposedly) provides you with fast file navigation. I tried using it for a while but I always found it cumbersome since all files were relative to your current directory so you'd end up typing paths like `../../../my/file.txt`. Sure you could see listings of files as you were typing but it wasn't all that much faster than using the plain 'ol `:e` in Vim. In addition, it requires Ruby and a C++ extension to be compiled.

Enter [Ctrl-P][]:

  * Written in pure Vimscript
  * Automatically finds the root directory for your project and uses that for your search
  * Supports regexp
  * You can easily open a file in a vertical split or new tab
  * And more `:)`

### Installation ###

    #!bash
    git clone https://github.com/kien/ctrlp.vim ~/.vim/bundles/ctrlp.vim

### Demo ###

<center>
    <iframe border='0' height='502' scrolling='no' src='http://shelr.tv/records/500a04d89660806d7e000003/embed' style='border: 0' width='710'></iframe>
</center>

**Project Page:** [https://wincent.com/products/command-t](https://wincent.com/products/command-t)


3: Rainbow Parentheses
-----------------------

### Overview ###

We've all been there ... somewhere in the mist of your spaghetti [code](cat:coding) you have a missing parentheses. Of course you can count parentheses or use the 'ol finger pointing method, but [rainbow parentheses][] gives a nice visual display that goes a long way towards hunting down those pesky missing buggers. Plus, life can always use more rainbows `=D`!

### Installation ###

    #!bash
    git clone https://github.com/kien/rainbow_parentheses.vim ~/.vim/bundles/rainbow_parentheses.vim

### Demo ###

<center>
    <iframe border='0' height='502' scrolling='no' src='http://shelr.tv/records/500a06b19660806d7e000004/embed' style='border: 0' width='710'></iframe>
</center>


**Project Page:** [https://github.com/kien/rainbow_parentheses.vim](https://github.com/kien/rainbow_parentheses.vim)

4: Conque
----------

### Overview ###

One of my friends loves [Emacs][] (see!? We _can_ co-exist peacefully `;)` ) and I was really amazed at Emacs' [terminal emulator][]. I started poking around and found [conque][], a plugin which allows you to run interactive [Linux](tag:Linux) commands (like a [Bash](tag:Bash) shell, [Python](tag:Python) session, or [MySQL](tag:MySQL) client) inside of a [Vim](tag:Vim) buffer. Although I don't use this plugin every day, it comes in handy and is super convenient. It's the type of thing that you don't realize how how useful it is until you try it.

### Installation ###

    #!bash
    git clone https://github.com/chilicuil/conque ~/.vim/bundles/conque

### Demo ###

<center>
    <iframe border='0' height='502' scrolling='no' src='http://shelr.tv/records/500a07129660806d7e000005/embed' style='border: 0' width='710'></iframe>
</center>

**Project Page:** [http://code.google.com/p/conque/](http://code.google.com/p/conque/)

5: EasyMotion
---------------

### Overview ###

This plugin is not needed by [Vim](tag:Vim) gurus, but for the rest of us mere mortals, [EasyMotion][] is a fantastic [plugin](tag:plugin). As I'm sure you're well aware, Vim has a ton of motion commands such as `h` for "left", `k` for "down", `f` "for find", `w` for "word forwards", `b` for "word backwards", etc, etc, etc. Each of these commands takes a preceding number so `4h` means "go 4 characters to the left" and `10w` means (go 10 words to the right). However, I rarely use these preceding numbers. Why? Honestly, by the time I count the number of words I want to go forward, I could have just pressed `w` a bunch of times until I got where I wanted.

What EasyMotion does is provide you with the command `\\w` which displays a visual marker for each possible word (since we're in the "word forward" mode) you can go to. Then jumping to that position is as simple as pressing the letter corresponding to the position you want to be at. _Easy-peasy._

### Installation ###

    #!bash
    git clone https://github.com/Lokaltog/vim-easymotion ~/.vim/bundles/vim-easymotion

### Demo ###

<center>
    <iframe border='0' height='502' scrolling='no' src='http://shelr.tv/records/500a07729660806d7c000003/embed' style='border: 0' width='710'></iframe>
</center>

**Project Page:** [https://github.com/Lokaltog/vim-easymotion](https://github.com/Lokaltog/vim-easymotion)

6: Fugitive
------------

### Overview ###

My version control system of choice is [Git](tag:Git). Since I spend most/all of my coding time in Vim, [fugitive][] is a great plugin that integrates with Git.

A few of my favorite features:

  * Adding `%{fugitive#statusline()}` to `statusline` in your `~/.vimrc` shows the current branch in your status line
  * `Gstatus` shows the changed files and allows you to easily stage / commit
  * `Gblame` creates an interactive split
  * `Glog` shows the git log
  * `Gdiff` diffs the current version against what is checked into git

### Installation ###

    #!bash
    git clone https://github.com/tpope/vim-fugitive ~/.vim/bundles/vim-fugitive

### Demo ###

<center>
    <iframe border='0' height='502' scrolling='no' src='http://shelr.tv/records/500a07ad9660806d7e000006/embed' style='border: 0' width='710'></iframe>
</center>

**Project Page:** [https://github.com/tpope/vim-fugitive](https://github.com/tpope/vim-fugitive)

7: GUndo
----------

### Overview ###

Every editor supports undo, but Vim just doesn't do undo (that would be _waaay_ too easy). It keeps track of [undo branches](http://vim.wikia.com/wiki/Using_undo_branches). What does this mean? Let's say you edit line 5, undo that change, and then edit line 20. In normal editors, that change you just made on line 5 is gone forever. But in Vim you can get it back: the `:undolist` command lists all your changes. Using `:undolist` is a really confusing but [GUndo][] wraps that all up and puts a beautiful little bow on top. It allows you to easily visualize the your undo tree, view diffs, and revert changes.

### Installation ###

    #!bash
    git clone http://github.com/sjl/gundo.vim.git ~/.vim/bundle/gundo

### Demo ###

<center>
    <iframe border='0' height='502' scrolling='no' src='http://shelr.tv/records/500a07e89660806d7c000004/embed' style='border: 0' width='710'></iframe>
</center>

**Project Page:** [http://sjl.bitbucket.org/gundo.vim/](http://sjl.bitbucket.org/gundo.vim/)

8: Indent Guides
-----------------

### Overview ###

 [Python](tag:Python) is my tool of choice. I love that it is indention based, but having braces does have it's occasional benefits (especially keeping nested levels straight in long functions). [Vim indent guides][] highlights every indention level with a vertical bar making coding much easier. Earlier I had this functionality hacked into Python's syntax file, however this plugin is much faster and doesn't slow down on deep indents.

### Installation ###

    #!bash
    git clone https://github.com/nathanaelkane/vim-indent-guides ~/.vim/bundles/vim-indent-guides

### Demo ###

_I didn't make a demo for this one, it's fairly self explanatory, yes?_

**Project Page:** [https://github.com/nathanaelkane/vim-indent-guides](https://github.com/nathanaelkane/vim-indent-guides)

9: MatchIt
-----------

### Overview ###

 [MatchIt][] is a super simple, yet super useful plugin. Vim supports matching braces with `%` which is great for jumping around. MatchIt extends this to match just about anything (for example matching [XML](tag:XML) tags, `if`/`fi` in [Bash](tag:Bash), etc).

### Installation ###

    #!bash
    git clone https://github.com/edsono/vim-matchit ~/.vim/bundles/vim-matchit

### Demo ###

<center>
    <iframe border='0' height='502' scrolling='no' src='http://shelr.tv/records/500a08159660806d7e000007/embed' style='border: 0' width='710'></iframe>
</center>

**Project Page:** [http://www.vim.org/scripts/script.php?script_id=39](http://www.vim.org/scripts/script.php?script_id=39)

10: Speed Dating
----------------

### Overview ###

I regularly need to generate data files for work. In the bad 'ol days, creating these was very slow and labor intensive. Once I found out how to [increment and decrement](http://vim.wikia.com/wiki/Increasing_or_decreasing_numbers) numbers with `Ctrl-A` / `Ctrl-X`, this work went a _lot_ faster. However, this incrementing coolness doesn't work correctly with dates. With [speed dating][], dates increment correctly. _Shweet!_

### Installation ###

    #!bash
    git clone https://github.com/tpope/vim-speeddating ~/.vim/bundles/vim-speeddating

### Demo ###

<center>
    <iframe border='0' height='502' scrolling='no' src='http://shelr.tv/records/500a08519660806d7c000005/embed' style='border: 0' width='710'></iframe>
</center>

**Project Page:** [http://www.vim.org/scripts/script.php?script_id=2120](http://www.vim.org/scripts/script.php?script_id=2120)

11: Yank Stack
--------------

### Overview ###

One of the many things I love about Vim is its support for multiple yank buffers. However, using the default yank buffer is a lot more convenient. The only problem with this is often I'll need to paste something which has now been overwritten by another yank. People raved about [yankring](https://github.com/chrismetcalf/vim-yankring) but I found it counter-intuitive and difficult to use (not to mention it messed with the default way that yanks worked). I came across [yankstack][] which is a simpler and easier to use alternative.

When pasting from the default buffer with `p`, this plugin allows you to do `meta-p` and `meta-shift-p` to cycle backwards and forwards (respectively) through your yank history. In addition, the `:Yanks` command will display your yank history.

**Note:** Recent updates to yankstack have made this plugin a little more unstable. IMO, it is still a valuable plugin.

### Installation ###

    #!bash
    git clone https://github.com/maxbrunsfeld/vim-yankstack ~/.vim/bundles/vim-yankstack

### Demo ###

<center>
    <iframe border='0' height='502' scrolling='no' src='http://shelr.tv/records/500a087d9660806d7c000006/embed' style='border: 0' width='710'></iframe>
</center>

**Project Page:** [https://github.com/maxbrunsfeld/vim-yankstack](https://github.com/maxbrunsfeld/vim-yankstack)

12: Surround
-------------

### Overview ###

Vim provides the `i` selector to allow you to operate on text between two tokens. For example, given the text `{ 1, 2, 3 }`, `di{` (delete inside `{`), will result in the text `{}`. However, what if you want to change the surrounding `{` and `}`? The [surround][] plugin provides you with the `s` selector that allows you to operate on the surrounding tokens of text.

So taking our earlier example, `{ 1, 2, 3 }`, `cs{[` will result in `[ 1, 2, 3 ]`. Oh, "ho hum" you say? Surround can do much more. When working with any [XML](tag:XML) based language, Surround allows you to add, delete, and modify tags like a boss.

### Installation ###

    #!bash
    git clone https://github.com/tpope/vim-surround ~/.vim/bundles/vim-surround

### Demo ###

<center>
    <iframe border='0' height='502' scrolling='no' src='http://shelr.tv/records/500a08b09660806d7e000008/embed' style='border: 0' width='710'></iframe>
</center>

**Project Page:** [https://githumb.com/tpope/vim-surround](https://githumb.com/tpope/vim-surround)

[Vim]: wp:Vim
[opera]: wp:Opera_(web_browser)
[zsh]: wp:Z_shell
[Arch]: wp:Arch_Linux
[plugins]: http://vim.sourceforge.net/scripts/script_search_results.php?order_by=rating
[git]: wp:Git (software)
[Emacs]: http://www.gnu.org/software/emacs/
[terminal emulator]:http://www.gnu.org/software/emacs/manual/html_node/emacs/Terminal-emulator.html
[Python]: http://www.python.org

[Pathogen]:https://github.com/tpope/vim-pathogen#readme
[Command-T]:https://wincent.com/products/command-t
[Ctrl-P]: https://kien.github.com/ctrlp.vim#readme
[rainbow parentheses]: https://github.com/kien/rainbow_parentheses.vim#readme
[conque]: http://code.google.com/p/conque/
[fugitive]: https://github.com/tpope/vim-fugitive#readme
[vim indent guides]: https://github.com/nathanaelkane/vim-indent-guides#readme
[yankstack]: https://github.com/maxbrunsfeld/vim-yankstack#readme
[surround]: https://github.com/tpope/vim-surround#readme
[EasyMotion]: https://github.com/Lokaltog/vim-easymotion#readme
[GUndo]: http://sjl.bitbucket.org/gundo.vim/
[speed dating]: http://www.vim.org/scripts/script.php?script_id=2120
[MatchIt]: http://www.vim.org/scripts/script.php?script_id=39
