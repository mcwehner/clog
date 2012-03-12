Clog
====

Clog is a stupid, barely functional campfire command-line client that probably
won't work.


Dependencies
------------

Use `pip` to install the dependencies listed in `Requirements`:

    $ pip install -r Requirements


It's recommended that this be done inside of a dedicated virtual environment.


Setup
-----

Copy the contents of `credentials.example.yaml` to a file called
`credentials.yaml`, and supply your own campfire auth token and relevant
subdomain.

Your auth token can be found by logging into your campfire account.


Usage
-----

### Streaming ###

Streaming chat from a room is simple:

    $ ./clog.py stream MyRoom


On OS X, text-to-speech is also available:

    $ ./clog.py stream MyRoom --text_to_speech


Clog uses `pyfire` to communicate with the campfire API, and streaming is done
by default in "transcript" mode. This means that joining the room isn't
necessary, but it also means that when streaming is started, all of the
"recent" messages will be output. Text-to-speech is disabled for any messages
that were sent prior to starting streaming (you want this, trust me).

To stop the streaming server, simply hit the enter key.


### Room listing ###

Rooms can be listed:

    $ ./clog.py rooms


### Room info ###

Detailed info about a can be shown:

    $ ./clog.py info MyRoom


Voices
------

When text-to-speech is enabled for streaming, different users can be given
different voices by adding them to `voices.yaml`. Keys are usernames, and
values are voice names. Partial usernames are acceptable: simply using "John"
will match a user named "John Doe".

Available voices can be listed for your system by using the `say` command:

    $ say -v ?


Bugs
----

There's probably lots of them, and I don't really care.
