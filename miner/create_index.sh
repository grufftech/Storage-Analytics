curl -XPUT "http://elasticsearch:9200/file-index" -d'
{
  "settings": {
    "analysis": {
      "analyzer": {
        "file_analyzer": {
          "tokenizer": "my_tokenizer"
        }
      },
      "tokenizer": {
        "my_tokenizer": {
          "type": "path_hierarchy"
        }
      }
    }
  },
  "mappings": {
    "file": {
      "properties": {
        "path": {
          "type":  "text",
          "analyzer": "file_analyzer"
        },
        "size":{
          "type": "integer"
        },
        "timestamp": {
          "type":"date"
        }
      }
    }
  }
}'
