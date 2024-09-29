import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
        self.client = chromadb.PersistentClient("vectorstore")
        self.collection = self.client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for index, row in self.df.iterrows():
                self.collection.insert_one(
                    documents=row["Techstack"],
                    metadatas={'links':row['Links']},
                    ids=[str(uuid.uuid4())]
                )
                
    def query_links(self, skills, n_results=2):
        return self.collection.query(query_texts=skills, n_results=n_results).get('metadatas',[])
