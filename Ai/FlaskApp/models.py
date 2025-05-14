from flask import Flask, request, jsonify
import os
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# --- Flask Setup ---
app = Flask(__name__)

def init_pipelines(device):
    pipelines = {}
    # General QG for short answer and essay
    pipelines['general_qg'] = pipeline(
        'text2text-generation',
        model='iarfmoose/t5-base-question-generator',
        tokenizer='iarfmoose/t5-base-question-generator',
        device=device
    )
    # Multiple Choice QG (exam-style MCQ)
    pipelines['mcq_gen'] = pipeline(
        'text2text-generation',
        model='voidful/bart-eqg-question-generator',
        tokenizer='voidful/bart-eqg-question-generator',
        device=device
    )
    # True/False QG
    pipelines['tf_gen'] = pipeline(
        'text2text-generation',
        model='fares7elsadek/boolq-t5-base-question-generation',
        tokenizer='fares7elsadek/boolq-t5-base-question-generation',
        device=device
    )
    # MixQG for advanced mixed types
    pipelines['mixqg'] = pipeline(
        'text2text-generation',
        model='Salesforce/mixqg-base',
        tokenizer='Salesforce/mixqg-base',
        device=device
    )
    return pipelines

# Detect device for pipelines
DEVICE = 0 if torch.cuda.is_available() else -1
PIPELINES = init_pipelines(DEVICE)

def extract_key_concepts(text, ner_pipeline, top_k=5):
    entities = ner_pipeline(text)
    # filter and unique
    labels = {'ORG','PER','LOC','MISC'}
    words = [ent['word'] for ent in entities if ent['entity'] in labels]
    # take most frequent / first k
    seen = []
    for w in words:
        if w not in seen:
            seen.append(w)
        if len(seen) >= top_k:
            break
    return seen or ['the topic']

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    text = data.get('text', '')
    num = int(data.get('num_questions', 30))
    types = data.get('types', None)
    # default all types
    all_types = ['short_answer', 'essay', 'multiple_choice', 'radio', 'true_false']
    types = types if types else all_types

    # distribute counts evenly
    base = num // len(types)
    remainder = num % len(types)
    counts = {t: base for t in types}
    # distribute remainder
    for i, t in enumerate(types):
        if i < remainder:
            counts[t] += 1

    # extract concepts for guidance
    ner = pipeline('ner', model='dslim/bert-base-NER', device=DEVICE)
    concepts = extract_key_concepts(text, ner)
    prompt_concepts = ', '.join(concepts)

    questions = []
    # generate per type
    for qtype, cnt in counts.items():
        if qtype in ['short_answer', 'essay']:
            # generic QG
            guidance = f"Generate {cnt} {qtype.replace('_',' ')} questions on: {prompt_concepts}."
            inputs = f"generate questions: {text} | {guidance}"
            out = PIPELINES['general_qg'](
                inputs,
                max_length=64,
                num_return_sequences=cnt,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.9,
                early_stopping=True
            )
            for o in out:
                questions.append({'type': qtype, 'question': o['generated_text']})
        elif qtype == 'multiple_choice':
            # MCQ with options
            guidance = f"Generate {cnt} multiple choice questions (4 options each) on: {prompt_concepts}."
            inputs = text + ' ' + guidance
            out = PIPELINES['mcq_gen'](
                inputs,
                max_length=128,
                num_return_sequences=cnt,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.9,
                early_stopping=True
            )
            for o in out:
                questions.append({'type': qtype, 'question': o['generated_text']})
        elif qtype == 'radio':
            # single correct choice
            guidance = f"Generate {cnt} single-best-answer (radio) questions (4 options each) on: {prompt_concepts}."
            inputs = text + ' ' + guidance
            out = PIPELINES['mcq_gen'](
                inputs,
                max_length=128,
                num_return_sequences=cnt,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.9,
                early_stopping=True
            )
            for o in out:
                questions.append({'type': qtype, 'question': o['generated_text']})
        elif qtype == 'true_false':
            # boolean
            guidance = f"Generate {cnt} true/false questions on: {prompt_concepts}."
            inputs = text + ' ' + guidance
            out = PIPELINES['tf_gen'](
                inputs,
                max_length=64,
                num_return_sequences=cnt,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.9,
                early_stopping=True
            )
            for o in out:
                questions.append({'type': qtype, 'question': o['generated_text']})

    return jsonify({'questions': questions})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
