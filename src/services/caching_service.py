class CollectionCache:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CollectionCache, cls).__new__(cls)
            cls._instance.collection_cache = []
        return cls._instance

    def add_collection(self, collection_name: str, collection):
        self.collection_cache.append({"collection_name": collection_name, "collection": collection})

    def get_collection(self, collection_name: str):
        for collection in self.collection_cache:
            if collection["collection_name"] == collection_name:
                return collection["collection"]
        return None

    def delete_collection(self, collection_name: str):
        self.collection_cache = [c for c in self.collection_cache if c["collection_name"] != collection_name]

    def clear_cache(self):
        self.collection_cache.clear()
        
    def show_cache(self):
        for collection in self.collection_cache:
            print(collection["collection_name"])