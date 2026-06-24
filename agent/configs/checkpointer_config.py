
write_config = {
    "configurable": {
        "thread_id": "1", 
        "checkpoint_ns": ""
    },
    "recursion_limit": 100
}
read_config = {
    "configurable": {
        "thread_id": "1"
    },
    "recursion_limit": 100
}


MONGODB_URI = "mongodb://omniful:omniful@localhost:27017/?authSource=admin"
DB_NAME = "checkpoint_example"