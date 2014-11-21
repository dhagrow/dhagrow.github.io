---
title: F# Crawler
category: Crawler Prototypes
tags: dev, crawler, fsharp
date: 2014-11-19 13:25
---

Blah blah F#.

## Installation

Should be simple on Linux. For a Debian-based system an ==apt-get== is enough:
    
~~~sh
$ sudo apt-get install fsharp
~~~

This will pull in Mono for .NET support.

## Input

Blah blah.

~~~fsharp
open System

[<EntryPoint>]
let main(args) =    
    printfn "args: %A" args
    printfn "env.cmdline: %A" <| Environment.GetCommandLineArgs()    
    0
~~~
