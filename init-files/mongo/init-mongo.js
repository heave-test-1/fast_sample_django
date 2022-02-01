db = new Mongo().getDB("fast");

db.createCollection('users', { capped: false });
db.createCollection('test', { capped: false });

text = cat("/docker-entrypoint-initdb.d/data.json");
data = JSON.parse(text)
db.users.insert(data);