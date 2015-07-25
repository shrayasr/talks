----------------------
-- Json/Jsonb Storage
----------------------

select '{"foo": "bar"}'::json;

select '{
  "foo": "bar",
  "bar": true,
  "baz": 1
  }'::json;

select '{"foo": "bar"}'::jsonb;

select '{
  "foo": "bar",
  "bar": true,
  "baz": 1
  }'::jsonb;

select pg_column_size('{
      "notificationType":"Bounce",
      "bounce":{
         "bounceType":"Permanent",
         "bounceSubType": "General",
         "bouncedRecipients":[
            {
               "emailAddress":"recipient1@example.com"
            },
            {
               "emailAddress":"recipient2@example.com"
            }
         ],
         "timestamp":"2012-05-25T14:59:38.237-07:00",
         "feedbackId":"00000137860315fd-869464a4-8680-4114-98d3-716fe35851f9-000000"
      },
      "mail":{
         "timestamp":"2012-05-25T14:59:38.237-07:00",
         "messageId":"00000137860315fd-34208509-5b74-41f3-95c5-22c1edc3c924-000000",
         "source":"email_1337983178237@amazon.com",
         "sourceArn": "arn:aws:ses:us-west-2:888888888888:identity/example.com",
         "sendingAccountId":"123456789012",
         "destination":[
            "recipient1@example.com",
            "recipient2@example.com",
            "recipient3@example.com",
            "recipient4@example.com"
         ]
      }
   }'::jsonb);

-----------------
-- Path Traversal
-----------------

select count(*) from raw_notifications_cleaned 
where 
  data ->> 'notificationType' = 'Delivery';

select (data -> 'bounce' ->> 'timestamp')::timestamp from raw_notifications_cleaned 
where 
  data ->> 'notificationType' = 'Bounce';

select data #> '{mail, timestamp}' from raw_notifications_cleaned;

select data -> 'mail' -> 'timestamp' from raw_notifications_cleaned;

select data -> 'bounce' ->> 'bounceType', data -> 'bounce' ->> 'bounceSubType' 
from raw_notifications_cleaned  
where
  (data -> 'mail' ->> 'timestamp')::timestamp > '2015-07-12T13:34:00' and
  (data -> 'mail' ->> 'timestamp')::timestamp < '2015-07-12T13:38:00' and
  data ->> 'notificationType' = 'Bounce';

select * 
from raw_notifications_cleaned
where to_json(
  array(
    select jsonb_array_elements(data 
      -> 'bounce' 
      -> 'bouncedRecipients') 
        ->> 'emailAddress'))::jsonb ?| array['sengupta.anaya@rediffmail.com']

------------
-- Indexing
------------

drop index rwc_idx_data_notifType;
create index rwc_idx_data_notifType 
  on raw_notifications_cleaned ((data ->> 'notificationType'));

explain analyze select count(*) from raw_notifications_cleaned 
where
  data ->> 'notificationType' = 'Bounce'

drop index rwc_idx_data_bounce;
create index rwc_idx_data_bounce on raw_notifications_cleaned 
using gin ((data -> 'bounce') jsonb_path_ops);

explain analyze select * from raw_notifications_cleaned 
where
  data -> 'bounce' @> '{"bouncedRecipients":[{"emailAddress": "sengupta.anaya@rediffmail.com"}]}';

