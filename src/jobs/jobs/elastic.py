mapping = {
    "settings": {
        "analysis": {
            "char_filter": {
                "remove_special_chars": {
                    "type": "pattern_replace",
                    "pattern": "[,.]",
                    "replacement": "",
                }
            },
            "analyzer": {
                "custom_analyzer_with_char_filter": {
                    "tokenizer": "standard",
                    "char_filter": ["remove_special_chars"],
                    "filter": ["lowercase"],
                }
            },
        }
    },
    "mappings": {
        "properties": {
            "scrape_session": {"type": "keyword", "index": True},
            "job_id": {"type": "keyword", "index": True},
            "job_title": {"type": "text"},
            "organization": {"type": "keyword"},
            "posted_at": {"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss"},
            "location": {
                "type": "nested",
                "properties": {
                    "name": {
                        "type": "text",
                        "analyzer": "custom_analyzer_with_char_filter",
                    },
                    "state": {
                        "type": "text",
                        "analyzer": "custom_analyzer_with_char_filter",
                    },
                },
            },
        },
    },
}
