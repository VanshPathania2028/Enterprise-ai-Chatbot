from reranker.rerank import rerank
question = "What is Machine Learning?"

results = [
    "Machine Learning is a subset of Artificial Intelligence.",
    "Python is a programming language.",
    "Deep Learning is a part of Machine Learning.",
    "India has many IT companies."
]
best = rerank(question, results)

for item in best:
    print(item)