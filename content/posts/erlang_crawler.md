---
title: Erlang Crawler
tags: dev, erlang, crawler
date: 2014-11-18 13:25
---

The first entry in this series will explore Erlang.

## Installation

Should be simple on Linux. For a Debian-based system an apt-get is enough:
    
~~~sh
$ sudo apt-get install erlang
~~~

## Input

Execution from the command-line uses the ~~~escript~~~ command. The following
script is adapted straight from the ~~~escript~~~ manpage and simply prints out
a string entered from the command-line.

~~~erlang
#!/usr/bin/env escript

main([String]) ->
    try
        io:format("~s~n", [String])
    catch
        _:_ ->
            usage()
    end;
main(_) ->
    usage().

usage() ->
    io:format("usage: echo <input>~n"),
    halt(1).
~~~
