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
