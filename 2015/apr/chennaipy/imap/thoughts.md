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

## Gmail?
