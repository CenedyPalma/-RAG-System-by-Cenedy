import pytest
from flask import Flask
from src.preprocess import app

@pytest.mark.parametrize(
    "question,expected",
    [
        ("অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?", "শুম্ভুনাথ"),
        ("কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?", "মামাকে"),
        ("বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?", "১৫ বছর"),
    ]
)
def test_rag_expected_answers(question, expected):
    client = app.test_client()
    response = client.post("/", data={"question": question})
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert expected in html