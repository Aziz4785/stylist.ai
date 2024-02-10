OPENAI_API_KEY = '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'
TOGETHER_API_KEY = "1716ac006ca7879c4eba09ec99ba0d9de41d0a6a214f3425a1d4bf108025e8c8"
REPLICATE_API_KEY = "r8_aBlUqMCdaKVujQCMu6NkPFltPQXJAw50wVBwT"
#$env:REPLICATE_API_TOKEN="r8_aBlUqMCdaKVujQCMu6NkPFltPQXJAw50wVBwT"
#to run database server :
# 1)You must open the command interpreter as an Administrator.
# 2)cd C:\
# md "\data\db"
# 3)"C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath="c:\data\db"

db_uri = "mongodb://localhost:27017/"
db_name = "mydatabase"
#docker-compose up --build
collection_name_start_with = "data_zalando"
reference_name="reference8"