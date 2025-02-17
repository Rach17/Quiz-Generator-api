import time
import threading
from config import settings

class CollectionCache:
    _instance = None  # Singleton instance
    _cleanup_interval = 60 * 60  # Cleanup interval in seconds

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CollectionCache, cls).__new__(cls)
            cls._instance.cache = {}
            cls._instance._stop_cleanup = False
            cls._instance._start_cleanup_thread()
        return cls._instance

    def _start_cleanup_thread(self):
        def cleanup_loop():
            while not self._stop_cleanup:
                self.cleanup()
                time.sleep(self._cleanup_interval)
        thread = threading.Thread(target=cleanup_loop, daemon=True)
        thread.start()

    def add_collection(self, collection_name: str, collection, size, language, lifetime: float = settings.COLLECTION_LIFETIME):
        expire_time = time.time() + lifetime if lifetime is not None else None
        self.cache[collection_name] = {"collection": collection, "size": size, "language" : language, "expire_time": expire_time}

    def get_collection(self, collection_name: str):
        item = self.cache.get(collection_name)
        if item is None:
            return None
        return item

    def delete_collection(self, collection_name: str):
        self.cache.pop(collection_name, None)

    def clear_cache(self):
        self.cache.clear()

    def cleanup(self):
        now = time.time()
        expired_keys = [
            key for key, item in self.cache.items()
            if item["expire_time"] is not None and now > item["expire_time"]
        ]
        for key in expired_keys:
            self.cache.pop(key, None)

    def show_cache(self):
        for key, item in self.cache.items():
            expire_str = time.ctime(item["expire_time"]) if item["expire_time"] is not None else "Never"
            print(f"{key}: expires at {expire_str}")

    def stop_cleanup_thread(self):
        self._stop_cleanup = True