# ...
client.select("INBOX")
emails = client.search(None, '(FROM "foo@bar.com")')
for email in emails[1][0].split():
  client.store(email, '+X-GM-LABELS', "foo")
# ...

