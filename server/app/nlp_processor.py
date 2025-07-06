from transformers import pipeline

# You can also use Named Entity Recognition or summarization
def analyze_text(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=60, min_length=25, do_sample=False)
    return summary[0]["summary_text"]
