
import pandas as pd
import re

df = pd.read_csv("data/hadith.csv")
df = df[['English_Hadith']].dropna()
df.columns = ['Hadith']

def clean_text(text):
    if isinstance(text, str):
        text = re.sub(r'[^A-Za-z\s]', '', text)
        text = text.lower()
    return text

df['Hadith'] = df['Hadith'].apply(clean_text)


from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

embeddings = model.encode(df['Hadith'].tolist())

print("Done 1")



d = embeddings.shape[1]

index = faiss.IndexFlatL2(d)

index.add(np.array(embeddings))

print("Done 2")


faiss.write_index(index, "hadith.index")

print("All Done ✅")