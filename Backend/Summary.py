from transformers import pipeline
import re

TF_ENABLE_ONEDNN_OPTS=0

def split_text(text, max_chunk_length=1000):
    # Split text into chunks while preserving sentence boundaries
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_length:
            current_chunk += sentence
        else:
            chunks.append(current_chunk)
            current_chunk = sentence
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def generate_lecture_notes(file_url,s):

    print("Summarising...")

    with open(file_url, 'r') as file:
        text = file.read().replace('\n', '')
    
    chunks = split_text(text)
    
    summarization_pipeline = pipeline("summarization")
    for chunk in chunks:
        max_length = min(len(chunk) // 3, 50)  # You can adjust the ratio and the maximum length as needed
        summary = summarization_pipeline(chunk, max_length=max_length, min_length=30, do_sample=False)[0]['summary_text']
        #print("Summary:")
        #print(summary)
        #print("-" * 50)
        s = s + ' ' + summary
        print(len(text)-len(s))

    with open(file_url, 'w') as f:
        f.write(s)

    print("Summary completed")
    return s