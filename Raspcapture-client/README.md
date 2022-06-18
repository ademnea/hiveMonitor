Quick links
===========

-   [Home](https://github.com/giampaolo/pyftpdlib)

About
=====

Python FTP server library provides a high-level portable interface to
easily write very efficient, scalable and asynchronous FTP servers with
Python. It is the most complete
[RFC-959](http://www.faqs.org/rfcs/rfc959.html) FTP server
implementation available for [Python](http://www.python.org/)
programming language.

Features
========

-   Extremely **lightweight**, **fast** and **scalable** (see
    [why](https://github.com/giampaolo/pyftpdlib/issues/203) and
    [benchmarks](http://pyftpdlib.readthedocs.io/en/latest/benchmarks.html)).
-   Uses **sendfile(2)** (see
    [pysendfile](https://github.com/giampaolo/pysendfile)) system call
    for uploads.
-   Uses epoll() / kqueue() / select() to handle concurrency
    asynchronously.
-   \...But can optionally skip to a [multiple thread /
    process](http://pyftpdlib.readthedocs.io/en/latest/tutorial.html#changing-the-concurrency-model)
    model (as in: you\'ll be free to block or use slow filesystems).
-   Portable: entirely written in pure Python; works with Python from
    **2.6** to **3.5** by using a single code base.
-   Supports **FTPS** ([RFC-4217](http://tools.ietf.org/html/rfc4217)),
    **IPv6**
    ([RFC-2428](ftp://ftp.rfc-editor.org/in-notes/rfc2428.txt)),
    **Unicode** file names
    ([RFC-2640](http://tools.ietf.org/html/rfc2640)), **MLSD/MLST**
    commands
    ([RFC-3659](ftp://ftp.rfc-editor.org/in-notes/rfc3659.txt)).
-   Support for virtual users and virtual filesystem.
-   Extremely flexible system of \"authorizers\" able to manage both
    \"virtual\" and \"real\" users on on both
    [UNIX](http://pyftpdlib.readthedocs.io/en/latest/tutorial.html#unix-ftp-server)
    and
    [Windows](http://pyftpdlib.readthedocs.io/en/latest/tutorial.html#windows-ftp-server).
-   [Test
    coverage](https://github.com/giampaolo/pyftpdlib/blob/master/pyftpdlib/test/)
    close to 100%.

Performances
============

Despite being written in an interpreted language, pyftpdlib has transfer
rates comparable or superior to common UNIX FTP servers written in C. It
usually tends to scale better (see
[benchmarks](https://pyftpdlib.readthedocs.io/en/latest/benchmarks.html))
because whereas vsftpd and proftpd use multiple processes to achieve
concurrency, pyftpdlib only uses one (see [the C10K
problem](http://www.kegel.com/c10k.html)).

pyftpdlib vs. proftpd 1.3.4
---------------------------

+--------------------------------+------------+------------+----------+
| **benchmark type**             | **p        | *          | **s      |
|                                | yftpdlib** | *proftpd** | peedup** |
+--------------------------------+------------+------------+----------+
| STOR (client -\> server)       | > 585.90   | 600.49     | -0.02x   |
|                                | > MB/sec   | MB/sec     |          |
+--------------------------------+------------+------------+----------+
| RETR (server -\> client)       | 1652.72    | 1524.05    | *        |
|                                | MB/sec     | MB/sec     | *+0.08** |
+--------------------------------+------------+------------+----------+
| 300 concurrent clients         | > 0.19     | 9.98 secs  | **+51x** |
| (connect, login)               | > secs     |            |          |
+--------------------------------+------------+------------+----------+
| STOR (1 file with 300 idle     | > 585.59   | 518.55     | *        |
| clients)                       | > MB/sec   | MB/sec     | *+0.1x** |
+--------------------------------+------------+------------+----------+
| RETR (1 file with 300 idle     | 1497.58    | 1478.19    | 0x       |
| clients)                       | MB/sec     | MB/sec     |          |
+--------------------------------+------------+------------+----------+
| 300 concurrent clients (RETR   | > 3.41     | 3.60 secs  | **       |
| 10M file)                      | > secs     |            | +0.05x** |
+--------------------------------+------------+------------+----------+
| 300 concurrent clients (STOR   | > 8.60     | 11.56 secs | *        |
| 10M file)                      | > secs     |            | *+0.3x** |
+--------------------------------+------------+------------+----------+
| 300 concurrent clients (QUIT)  | > 0.03     | 0.39 secs  | **+12x** |
|                                | > secs     |            |          |
+--------------------------------+------------+------------+----------+

pyftpdlib vs. vsftpd 2.3.5
--------------------------

+--------------------------------+------------+------------+----------+
| **benchmark type**             | **p        | **vsftpd** | **s      |
|                                | yftpdlib** |            | peedup** |
+--------------------------------+------------+------------+----------+
| STOR (client -\> server)       | > 585.90   | 611.73     | -0.04x   |
|                                | > MB/sec   | MB/sec     |          |
+--------------------------------+------------+------------+----------+
| RETR (server -\> client)       | 1652.72    | 1512.92    | *        |
|                                | MB/sec     | MB/sec     | *+0.09** |
+--------------------------------+------------+------------+----------+
| 300 concurrent clients         | > 0.19     | 20.39 secs | *        |
| (connect, login)               | > secs     |            | *+106x** |
+--------------------------------+------------+------------+----------+
| STOR (1 file with 300 idle     | > 585.59   | 610.23     | -0.04x   |
| clients)                       | > MB/sec   | MB/sec     |          |
+--------------------------------+------------+------------+----------+
| RETR (1 file with 300 idle     | 1497.58    | 1493.01    | 0x       |
| clients)                       | MB/sec     | MB/sec     |          |
+--------------------------------+------------+------------+----------+
| 300 concurrent clients (RETR   | > 3.41     | 3.67 secs  | **       |
| 10M file)                      | > secs     |            | +0.07x** |
+--------------------------------+------------+------------+----------+
| 300 concurrent clients (STOR   | > 8.60     | 9.82 secs  | **       |
| 10M file)                      | > secs     |            | +0.07x** |
+--------------------------------+------------+------------+----------+
| 300 concurrent clients (QUIT)  | > 0.03     | 0.01 secs  | +0.14x   |
|                                | > secs     |            |          |
+--------------------------------+------------+------------+----------+

For more benchmarks see
[here](http://pyftpdlib.readthedocs.io/en/latest/benchmarks.html).

Quick start
===========

``` {.python}
>>> from pyftpdlib.authorizers import DummyAuthorizer
>>> from pyftpdlib.handlers import FTPHandler
>>> from pyftpdlib.servers import FTPServer
>>>
>>> authorizer = DummyAuthorizer()
>>> authorizer.add_user("user", "12345", "/home/giampaolo", perm="elradfmwMT")
>>> authorizer.add_anonymous("/home/nobody")
>>>
>>> handler = FTPHandler
>>> handler.authorizer = authorizer
>>>
>>> server = FTPServer(("127.0.0.1", 21), handler)
>>> server.serve_forever()
[I 13-02-19 10:55:42] >>> starting FTP server on 127.0.0.1:21 <<<
[I 13-02-19 10:55:42] poller: <class 'pyftpdlib.ioloop.Epoll'>
[I 13-02-19 10:55:42] masquerade (NAT) address: None
[I 13-02-19 10:55:42] passive ports: None
[I 13-02-19 10:55:42] use sendfile(2): True
[I 13-02-19 10:55:45] 127.0.0.1:34178-[] FTP session opened (connect)
[I 13-02-19 10:55:48] 127.0.0.1:34178-[user] USER 'user' logged in.
[I 13-02-19 10:56:27] 127.0.0.1:34179-[user] RETR /home/giampaolo/.vimrc completed=1 bytes=1700 seconds=0.001
[I 13-02-19 10:56:39] 127.0.0.1:34179-[user] FTP session closed (disconnect).
```

[other code
samples](http://pyftpdlib.readthedocs.io/en/latest/tutorial.html)

Donate
======

A lot of time and effort went into making pyftpdlib as it is right now.
If you feel pyftpdlib is useful to you or your business and want to
support its future development please consider
[donating](https://gmpy.dev/donate) me some money.