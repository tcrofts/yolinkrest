# yolinkrest
This is a simple REST endpoint to expose a local sqlite DB that is populated by an MQTT feed from yolink 

The schema from the DB is as follows

CREATE TABLE yolink(deviceId varchar(17), stateChangedAt int, time int,state varchar(10),alertType varchar(17),event varchar(17),temperature real,humidity real,battery varchar(1));
