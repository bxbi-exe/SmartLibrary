from flask import Flask, request, jsonify, send_file

import os
import uuid
import shutil
import csv

import spacy
import torch

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline, T5Tokenizer

# --- Flask Setup ---
app = Flask(__name__)

# NLP model for extracting key concepts/definitions
concept_extractor = pipeline("ner", model="dslim/bert-base-NER")

model_name = "iarfmoose/t5-base-question-generator"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def extract_key_concepts(text):
    entities = concept_extractor(text)
    return list(set(ent['word'] for ent in entities if ent['entity_group'] in ['ORG', 'PERSON', 'LOCATION', 'MISC']))

def generate_questions(text, num=5, q_type="mcq", lang="en", instructions=""):
    key_concepts = extract_key_concepts(text)

    if not key_concepts:
        key_concepts = ["the topic"]

    concepts_prompt = ", ".join(key_concepts[:5])
    guidance = f"Generate {num} {q_type} questions in {lang} based on: {concepts_prompt}. {instructions}"

    inputs = f"generate questions: {text} | {guidance}"
    encoded_input = tokenizer.encode_plus(
        inputs,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512
    ).to(device)

    with torch.no_grad():
        output = model.generate(
            input_ids=encoded_input["input_ids"],
            attention_mask=encoded_input["attention_mask"],
            max_length=64,
            num_return_sequences=num,
            num_beams=5,
            early_stopping=True
        )

    questions = [tokenizer.decode(q, skip_special_tokens=True) for q in output]

    return [{
        "question": q,
        "answer": "To be reviewed", #QA extraction model here maybe
        "type": q_type,
        "lang": lang,
        "instructions": instructions
    } for q in questions]


# --- Test ---
if __name__ == '__main__':
    sample_text = (
        "Artificial Intelligence is transforming industries by enabling automation, "
        "smart assistants like Alexa and Siri, and intelligent decision-making in healthcare, "
        "finance, and transportation."
    )

    questions = generate_questions(
        text=sample_text,
        num=3,
        q_type="short",
        lang="en",
        instructions="Focus on use cases of AI in industries."
    )

    for i, q in enumerate(questions, start=1):
        print(f"\nQuestion {i}: {q['question']}\nType: {q['type']}\nLang: {q['lang']}\n")


