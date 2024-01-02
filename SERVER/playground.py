from SERVER.ServerUtil import *
import pandas as pd
import pickle
from typing import List, Optional
from scipy import spatial
import openai
import numpy as np

EMBEDDING_MODEL = "text-embedding-ada-002"
embedding_cache = {}

def get_embedding(text: str, model="text-similarity-davinci-001", **kwargs) -> List[float]:

    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")

    response = openai.embeddings.create(input=[text], model=model, **kwargs)

    return response.data[0].embedding

def get_embeddings(
    list_of_text: List[str], model="text-similarity-babbage-001", **kwargs
) -> List[List[float]]:
    assert len(list_of_text) <= 2048, "The batch size should not be larger than 2048."

    # replace newlines, which can negatively affect performance.
    list_of_text = [text.replace("\n", " ") for text in list_of_text]

    data = openai.embeddings.create(input=list_of_text, model=model, **kwargs).data
    return [d.embedding for d in data]


def distances_from_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    distance_metric="cosine",
) -> List[List]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances

#run  py -m SERVER.playground at root
test_cases = [
            ("a tshirt/pull or something similar where the colors on it are separated by horizontal lines", "unknown"),
            ("an item for men (but not trousers/pants) with the norwegian flag on it","men"),
            ("a tshirt where the name of the brand is written in big", "unknown"),
            ("a stand collar coat", "unknown"),
            ("I want a checkered shirt containing the color green", "unknown"),
            ("an officier collar coat" , "unknown"),
            ("I want bi-colored shoes, with white as one of the colors","unknown"),
            ("a pair of women's shorts that I can wear over pantyhose","women"),
            ("sailor/marinière style for women ","women"),
            ("something related to FC barcelona", "unknown")]

def embedding_from_string(
    string: str,
    model: str = EMBEDDING_MODEL,
    embedding_cache=embedding_cache
) -> list:
    """Return embedding of given string, using a cache to avoid recomputing."""
    if (string, model) not in embedding_cache.keys():
        embedding_cache[(string, model)] = get_embedding(string, model)
    return embedding_cache[(string, model)]

def indices_of_nearest_neighbors_from_distances(distances) -> np.ndarray:
    """Return a list of indices of nearest neighbors from a list of distances."""
    return np.argsort(distances)

def recommendations_from_strings(
   strings: List[str],
   index_of_source_string: int,
   model="text-embedding-ada-002",
) -> List[int]:
   """Return nearest neighbors of a given string."""

   # get embeddings for all strings
   embeddings = [embedding_from_string(string, model=model) for string in strings]

   # get the embedding of the source string
   query_embedding = embeddings[index_of_source_string]

   # get distances between the source embedding and other embeddings (function from embeddings_utils.py)
   distances = distances_from_embeddings(query_embedding, embeddings, distance_metric="cosine")

   # get indices of nearest neighbors (function from embeddings_utils.py)
   indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)
   return indices_of_nearest_neighbors

def print_recommendations_from_strings(
    strings: list[str],
    index_of_source_string: int,
    k_nearest_neighbors: int = 1,
    model=EMBEDDING_MODEL,
) -> list[int]:
    """Print out the k nearest neighbors of a given string."""
    # get embeddings for all strings
    embeddings = [embedding_from_string(string, model=model) for string in strings]
    # get the embedding of the source string
    query_embedding = embeddings[index_of_source_string]
    # get distances between the source embedding and other embeddings (function from utils.embeddings_utils.py)
    distances = distances_from_embeddings(query_embedding, embeddings, distance_metric="cosine")
    # get indices of nearest neighbors (function from utils.utils.embeddings_utils.py)
    indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)

    # print out source string
    query_string = strings[index_of_source_string]
    print(f"Source string: {query_string}")
    # print out its k nearest neighbors
    k_counter = 0
    for i in indices_of_nearest_neighbors:
        # skip any strings that are identical matches to the starting string
        if query_string == strings[i]:
            continue
        # stop after printing out k articles
        if k_counter >= k_nearest_neighbors:
            break
        k_counter += 1

        # print out the similar strings and their distances
        print(
            f"""
        --- Recommendation #{k_counter} (nearest neighbor {k_counter} of {k_nearest_neighbors}) ---
        String: {strings[i]}
        Distance: {distances[i]:0.3f}"""
        )

    return indices_of_nearest_neighbors

if __name__ == '__main__':
    # for case in test_cases:
    #     print(case[0]+" : ")
    #     print(extract_feature_words_from_query(case[0]))
    #     print("-------------------")
    print("test")
    print_recommendations_from_strings(strings = ["black and white stripes, presenting","boat neckline that accentuates the","PACK - T-shirt à manches","It presents a boat neckline","T-shirt à manches longues presented","marinière"],
    index_of_source_string=5,  # let's look at articles similar to the first one about Tony Blair
    k_nearest_neighbors=5,  # let's look at the 5 most similar articles
)
    