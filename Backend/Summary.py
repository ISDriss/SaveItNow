from transformers import pipeline
import re
import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

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

def generate_lecture_notes(fromfile, tofile):
    print("Summarising...")

    with open(fromfile, 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', '')

    #ATTENTION : le text doit faire plus de 30 mots sinon ça fait n'importe quoi
    summarization_pipeline = pipeline("summarization")
    
    # mettre le pourcentage voulu du text de début
    target_length = len(text) * 0.2
    
    summary = text
    while len(summary) > target_length:
        chunks = split_text(summary)
        summary_text = ""
        for chunk in chunks:
            max_length = min(len(chunk) // 3, 50)  # You can adjust the ratio and the maximum length as needed
            chunk_summary = summarization_pipeline(chunk, max_length=max_length, min_length=30, do_sample=False)[0]['summary_text']
            summary_text += ' ' + chunk_summary
        
        summary = summary_text.strip()

    with open(tofile, 'w', encoding='utf-8') as f:
        f.write(summary)

    print("Summary completed")
    return summary
