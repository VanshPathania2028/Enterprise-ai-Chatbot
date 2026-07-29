def score_result(text, question):
    score = 0

    question_words = question.lower().split()
    text_lower = text.lower()

    for word in question_words:
        if word in text_lower:
            score += 1

    return score

def rerank(question, results):
    scored = []

    for result in results:
        score = score_result(question, result)
        scored.append((score, result))

    scored.sort(reverse=True)

    return [result for score, result in scored if  score > 0]
    