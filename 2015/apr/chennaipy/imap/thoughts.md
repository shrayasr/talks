# Python, Imap and Gmail

## Email

There are 2 main protocols to fetch email:

- POP3
- IMAP

### POP3

Post Office Protocol

Majorly used for retrieve and delete kind of access to mailboxes

- Simple
- Encryption over SSL/TLS
- Mailbox is one store, no folder business
- POP _moves_ messages locally (some servers have option to leave messages there)
- Receives all parts of a message

### Imap

Used for asynchronous mode of connections (offline and online modes) and leaves
the messages there unless the user explicitly deletes them. Multiple people
can access the account as well 

- Is very asynchronous. Can be connected or disconnected and download messages
  on demand
- Multiple clients can be connected to the inbox
- Download only parts of message (eg. only text and not attachments)
- Supports multiple mailboxes
- Server side searches
- Extensions

Internet Mail Access Protocol

## Gmail

Gmail much like any other email service allows us to retrieve our mail by both
pop3 and by imap methods. 

imap however needs to be enabled from within the settings > Forwarding and POP/IMAP 
menu. Additionally we have to allow access from "less secure" apps so that 
application that google deems "less secure" can access the account via means
other than OAuth (insert long discussion here)

## Python

So how do imap and gmail come together with Python?

**`import imaplib`** 

imaplib, a library in the standard lib, encapsulates a connection to an imap
server

Ideally you'd want to encrypt your connections using SSL/TLS and `IMAP4_SSL` is 
the class that can be used for it

Lets work on some cases together

### I want to check the count of emails in my inbox 

    import imaplib
    client = IMAP4_SSL("imap.gmail.com", "993")
    client.login("shrayasr@gmail.com","DontTryToReadMyPasswordMan")
    result, response = client.select("INBOX")
    print "count is %s" % response[0]

Before we go any further though, let us understand some Gmail imap specifics

In Gmail, there are no folders. Everything is but a label. All Gmail specific
labels are prefixed with "[Gmail]/". Here are some examples:

- Spam is "[Gmail]/Spam"
- Drafts is "[Gmail]/Drafts"
- Sent is "[Gmail]/Sent Mail"

and so on.

As i've already mentioned, the nice thing about imap is that it allows for
extensions. I.e. Gmail can _extend_ the imap protocol and allow for some
Gmail specific functions. 

I'm sure we all have at some point, used and marvelled at how awesome the
Gmail search is and how much of power it gives with its simple to understand
syntax. For Eg. to search all mails from Vijay, i'd just have to type 
"from: vijaykumar@bravegnu.org" in the search box and gmail will take care
of the rest for me. 

Gmail extends the imap "SEARCH" command and adds this interface _via_ imap 
itself. How cool is that? How does it do it? 

Gmail adds a 'X-GM-RAW' search attribute to which you can pass the string 
"from:vijaykumar@bravegnu.org" and when you execute a `.search` with these
parameters, you'll get back a set of matching message ids.

### I want to get the mails from my sent box, that I sent to Foo

    # ...
    client.select("[Gmail]/Sent Mail")
    client.search(None, '(X-GM-RAW "to:foo@bar.com")')
    # ...

OR since imap natively also has some decent search features, you can directly 
use the `TO` keyword instead of using the Gmail extension

    # ...
    client.select("[Gmail]/Sent Mail")
    client.search(None, '(TO "foo@bar.com")')
    # ...

### I want to search all the mails sent to me by foo and add a "foo" label

Labels are a notion of Gmail and not **ALL** mailboxes so this would also come 
under the list of Gmail extensions.

Which one? 

Well X-GM-LABELS of course :)

You can use the `.store` imap command with this Gmail extension to add a label
to the required mail of choice.


    # ...
    client.select("INBOX")
    emails = client.search(None, '(FROM "foo@bar.com")')
    for email in emails[1][0].split():
      client.store(email, '+X-GM-LABELS', "foo")
    # ...

Moving mails from one "folder" to another is as simple as applying a new label
and removing an old one. 

## OfflineIMAP [BONUS]

Ok so you have a way to access your mail, to read it, and you tell me that
it can be asynchronous. How do I get it all to my computer man?

**OfflineIMAP** sir!

OfflineIMAP is a piece of software that allows you to sync your inbox as a 
local MailDir. This allows us to read our messages when offline. Any change
that is made in both places is synced to the other place

OfflineIMAP is written in python and can be a pretty big pinch to set up. 
However it has gotten way easier over the past few releases and can be 
set up with just a few lines in your ~/.offlineimaprc file

Mails that are downloaded via the OfflineIMAP program are stored in the MailDir
format which is readily recognized by multiple email clients. Some of them
are Mutt (Vim based) and Gnus (Emacs based)

### I want to do something with these mails though

Sure boss!

`import mailbox` 

Mailbox is a module to manipulate on disk Mailboxes (which can be in multiple
formats)

To access mails on the mailbox is pretty simple: 

    import mailbox
    m = mailbox.MailDir("/path/to/Maildir")
    for mail in m:
      print mail["subject"]

The mailbox object itself can be iterated on to process them
