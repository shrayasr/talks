# The beauty that is PostgreSQL - Part 1

To set the record straight, we added the _part 1_ at the end just so that we 
give ourselves some head space for future talks. Think sequels and prequels. 

## PostgreSQL? 

PostgreSQL brands itself as the worlds most advanced open source database. If 
pg isn't in your stack, you owe it to yourself to give it a shot. You will not
regret it. 

## 2

Today, we're here to give you 2 instances as to why even you might start 
believing that PG _is_ the world's most advanced open source database 

- Insert statements
- Json

## Insert statements

I'm sure that you're probably thinking right now as to what is so "new and
advanced" about insert statements. You'll see soon enough how things behave
with scale. 

* inserting one record 
  * using insert statement
* inserting 1000 records
  * using insert multiple values statement
* inserting 1000000 records
  * using insert with `values(),()` statement ? 
    * But that's slow, 
    * "The COPY command is optimized for loading large numbers of rows" [2]
  * use copy with csv statement? OK but size of the csv in memory
    * number of characters * 2bytes per string, 
    * /r/whoadude
  * use copy with binary ? 
    * postgres standard file header
    * number of fields
      * field size
      * field value
    * size in memory ? datatype specific, 
  * did I mention this was in prod
    * not prod ? just use pgbulkload

## Json

### Outline

* Intro
* History 
  * json
  * jsonb
* Use cases 
* Demos
  * Path traversal
  * Array contains
  * Indexes

### Intro

Applications rely on two kinds of data - Structured and Unstructured. Depending
on the domain, one might supersede the other. RDBMS' are really good at
handling data which has a backing structure. Relations are very powerful and
can be used to model a vast variety of business scenarios. Unstructured data is
usually when we would opt for databases like MongoDB or the more recent -
RethinkDB.

There arises a case, more often than not that applications would reach a point
of scale where they _will_ have to incorporate structured / unstructured data
_along_ with the other. In this case, people usually opt to have two databases,
one for structured and the other for unstructured data. Lets talk about that.

### History

#### Json

In 9.2, PG introduced the Json type. As of 9.2, they were just stored as text
fields after checking for validity. There were a few functions on top of the 
json type to turn a given row in json and vice versa.

Had stuff like row_to_json and array_to_json

The main caveat however was that storage was still text (after json
validation), so while insertion would be cheap, querying would be a tough thing
to do since it had to convert it to a proper json format before performing any
operation on it.

#### Enter Jsonb

In 9.4, PG introduced the new Jsonb type - A much required improvement on the
json format. The major difference was that the storage now didn't require us
to reparse the original text in order to process it. This brought with it 
the power to apply concepts like indexing to a json column! 

Because of this, all the existing json_* functions were supported with jsonb
along with the addition of many more json generation/querying functions. 

### Some use cases 

* Store API Keys / Integration information
* Delayed processing of API responses from 3rd party sources 

---

Refs:
- http://michael.otacoo.com/postgresql-2/postgres-9-2-highlight-json-data-type/
- http://www.depesz.com/2014/03/25/waiting-for-9-4-introduce-jsonb-a-structured-format-for-storing-json/
- https://blog.codeship.com/unleash-the-power-of-storing-json-in-postgres/
- http://nandovieira.com/using-postgresql-and-jsonb-with-ruby-on-rails

