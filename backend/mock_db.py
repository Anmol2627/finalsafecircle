import asyncio
from datetime import datetime
import uuid
import json
import os

DB_FILE = "db.json"

class MockCursor:
    def __init__(self, data, sort_key=None, sort_order=1, limit_n=None):
        self.data = data
        self.sort_key = sort_key
        self.sort_order = sort_order
        self.limit_n = limit_n

    def sort(self, key, order=1):
        self.sort_key = key
        self.sort_order = order
        return self

    def limit(self, n):
        self.limit_n = n
        return self

    async def to_list(self, length):
        result = list(self.data)  # Make a copy
        if self.sort_key:
            result.sort(key=lambda x: x.get(self.sort_key, 0), reverse=(self.sort_order == -1))
        
        if self.limit_n:
            result = result[:self.limit_n]
            
        if length:
            result = result[:length]
            
        return result

class MockCollection:
    def __init__(self, name, db):
        self.name = name
        self.db = db
        self.data = []

    async def insert_one(self, document):
        if '_id' not in document:
            document['_id'] = str(uuid.uuid4())
        self.data.append(document)
        self.db.save()
        return True

    async def insert_many(self, documents):
        for doc in documents:
            if '_id' not in doc:
                doc['_id'] = str(uuid.uuid4())
            self.data.append(doc)
        self.db.save()
        return True

    async def find_one(self, query, projection=None):
        for doc in self.data:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                return doc
        return None

    def find(self, query, projection=None):
        results = []
        for doc in self.data:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                results.append(doc)
        return MockCursor(results)

    async def update_one(self, query, update):
        doc = await self.find_one(query)
        if doc:
            if "$set" in update:
                for k, v in update["$set"].items():
                    doc[k] = v
            self.db.save()
            class Result:
                modified_count = 1
            return Result()
        class Result:
            modified_count = 0
        return Result()

    async def count_documents(self, query):
        if not query:
            return len(self.data)
        count = 0
        for doc in self.data:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                count += 1
        return count

class MockDatabase:
    def __init__(self):
        self.users = MockCollection('users', self)
        self.incidents = MockCollection('incidents', self)
        self.status_checks = MockCollection('status_checks', self)
        self.collections = {
            'users': self.users,
            'incidents': self.incidents,
            'status_checks': self.status_checks
        }
        self.load()

    def load(self):
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, 'r') as f:
                    data = json.load(f)
                    self.users.data = data.get('users', [])
                    self.incidents.data = data.get('incidents', [])
                    self.status_checks.data = data.get('status_checks', [])
            except Exception as e:
                print(f"Error loading DB: {e}")

    def save(self):
        data = {
            'users': self.users.data,
            'incidents': self.incidents.data,
            'status_checks': self.status_checks.data
        }
        try:
            with open(DB_FILE, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving DB: {e}")

    def __getitem__(self, name):
        return self.collections.get(name)

    def __getattr__(self, name):
        return self.collections.get(name)

    def close(self):
        self.save()

class MockClient:
    def __init__(self, url=None):
        self.db = MockDatabase()
    
    def __getitem__(self, name):
        return self.db

    def close(self):
        self.db.close()
