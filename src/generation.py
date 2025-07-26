import openai

openai.api_key = "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" 
def generate_answer(query: str, contexts: list[str]):
    prompt = (
        "You are a helpful assistant. Use the following contexts to answer.\n\n"
        + "\n\n".join(f"Context {i+1}:\n{c}" for i,c in enumerate(contexts))
        + f"\n\nQ: {query}\nA:"
    )
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content": prompt}],
        max_tokens=200,
    )
    return resp.choices[0].message.content.strip()
