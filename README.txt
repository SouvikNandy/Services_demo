It's a DEMO of the CASE below:
## CASE :
A Service Provider can register a new Service, choose among standard Features and provide prices for each feature.
A Service Receiver aka. Client can subscribe to one/multiple service, choosing only the features needed.
Also, the Client need to know the total amount to be paid for subscription
(total features tariff + convenience charges).

## The APIs are enlisted on this google doc below :
https://docs.google.com/spreadsheets/d/1Hlj3SBC0ekxrmuBUn-96ts5pktZ8Y0pgdq-5BXupnsI/edit?usp=sharing

## BOTTLE NECKS:
1) As its a dummy project there is no authentication system.
We are using different tables to store Service Provider and Clients , it can be done using a Single `User` table.
2) For now we are assuming only one Service Provider and Only one Client (to keep the request body same,
as the frontend don't need to send user_id's on request body. It should be retrieved from Authentication only ).
3) convenience charges are hard-coded as 500 while calculating payable

## n.b:
We are also placed our SECRET_KEY and a sqlite3 database inside the codebase as it's a ready to run demo.

