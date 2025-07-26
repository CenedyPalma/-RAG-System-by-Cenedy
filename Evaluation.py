def evaluate_answer(predicted: str, expected: str) -> float:
   
    pred_tokens = set(predicted.lower().split())
    exp_tokens = set(expected.lower().split())

    if not exp_tokens:
        return 0.0

    overlap = pred_tokens.intersection(exp_tokens)
    score = len(overlap) / len(exp_tokens)
    return round(score, 3)

predicted = "অনুপম আত্মীয়ের সহানুভূতির কথা কোথায় বলেছেন?"
expected = "অনুপমের আত্মীয়ের সহানুভূতির কথা মামার কাছে বলেছেন।"

score = evaluate_answer(predicted, expected)
print(f"Evaluation Score: {score}")
