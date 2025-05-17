from flask import Flask, request
import mimetypes
from docx import Document
import PyPDF2

import torch

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline, T5Tokenizer

app = Flask(__name__)

# Document/file management ====================================================
def read_file(file) -> str:
    filename = file.filename.lower()
    mimetype, _ = mimetypes.guess_type(filename)

    # TXT / JAVA / PY files
    if filename.endswith(('.txt', '.java', '.py')):
        try:
            return file.read().decode('utf-8')
        except UnicodeDecodeError:
            file.seek(0)
            return file.read().decode('windows-1251')  # fallback for Cyrillic

    # DOCX files
    elif filename.endswith('.docx'):
        doc = Document(file)
        return '\n'.join([para.text for para in doc.paragraphs])

    # PDF files
    elif filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
        return text

    else:
        raise ValueError("Unsupported file type. Only .txt, .java, .docx, .pdf are supported.")


# request needs to have an uploaded file in the body with key "file"
# tested with Postman, functions works
@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return {"error": "No file part in the request"}, 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return {"error": "No selected file"}, 400

    try:
        file_content = read_file(uploaded_file)
        return {"content": file_content}, 200  # preview only
    except ValueError as e:
        return {"error": str(e)}, 400


# ======================================================================
# NLP model for extracting key concepts/definitions ====================
# todo research about facebook/bart-large-cnn, dslim/bert-base-NER, spaCy or keyBert models
concept_extractor = pipeline("ner", model="dslim/bert-base-NER")


def extract_key_concepts(text):
    entities = concept_extractor(text)
    return list(set(ent['word'] for ent in entities if ent['entity'] in ['ORG', 'PER', 'LOC', 'MISC']))


model_name = "iarfmoose/t5-base-question-generator"
tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


# Question generation ========================================================
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
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.9,
            early_stopping=True
        )

    questions = [tokenizer.decode(q, skip_special_tokens=True) for q in output]

    return [{
        "question": q,
        "answer": "To be reviewed",
        "type": q_type,
        "lang": lang,
        "instructions": instructions
    } for q in questions]


# --- Test ---
if __name__ == '__main__':
    sample_text = (
        "Psychology, derived from the Greek words psyche (meaning soul or mind) and logos (meaning study), is the scientific study of behavior and mental processes. Though psychology as a formal discipline is relatively young, its roots extend deep into ancient philosophy, notably in the works of Greek philosophers like Socrates, Plato, and Aristotle, who questioned human thought, motivation, and behavior as early as 400 BCE. However, psychology did not become a distinct scientific field until the late 19th century. The official birth of psychology as a science is often dated to 1879, when German physician and physiologist Wilhelm Wundt established the first experimental psychology laboratory at the University of Leipzig in Germany. Wundt used a method called introspection to analyze the inner workings of the human mind and is widely regarded as the “father of modern psychology.” His student, Edward Titchener, later brought Wundt’s ideas to the United States and developed the school of thought known as structuralism, which aimed to break down mental processes into their most basic components. Around the same time, William James, often referred to as the “father of American psychology,” founded a competing school called functionalism, influenced by Charles Darwin’s theory of evolution. Functionalism focused on the purpose of consciousness and behavior in helping individuals adapt to their environment. As psychology evolved, it moved beyond introspection and philosophical speculation to embrace scientific methodology. In the early 20th century, Sigmund Freud, an Austrian neurologist, introduced psychoanalysis, a theory and method emphasizing unconscious motives, childhood experiences, and internal conflicts, profoundly influencing both psychology and culture. While Freud’s theories were controversial, they opened the door to new discussions about personality and mental illness. Soon after, John B. Watson and B.F. Skinner pioneered behaviorism, a school of thought that focused on observable behaviors and the ways they are learned, rejecting introspective methods. Behaviorism dominated American psychology for much of the early to mid-20th century and led to practical applications in education, therapy, and training. Later, in the 1950s and 1960s, humanistic psychology, led by Carl Rogers and Abraham Maslow, emerged in response to the deterministic views of psychoanalysis and behaviorism. It emphasized human potential, free will, and the importance of self-actualization. During the same period, the cognitive revolution began, restoring interest in the study of mental processes such as thinking, memory, and language. Psychologists like Jean Piaget and Noam Chomsky played key roles in this shift. Today, psychology is a diverse field with many sub-disciplines, including clinical, cognitive, developmental, social, biological, and industrial-organizational psychology. It employs various research methods, from experiments and case studies to neuroimaging and behavioral observation. Modern psychology integrates biological, psychological, and socio-cultural perspectives to provide a more complete understanding of human behavior. From its philosophical origins to its status as a rigorous science, psychology continues to evolve, driven by new technologies, discoveries, and the timeless quest to understand the human mind. As we begin this course, remember: psychology is not just about diagnosing mental illness—it’s about understanding ourselves and others, improving lives, and exploring what it means to be human."
    )

    questions = generate_questions(
        text=sample_text,
        num=12,
        q_type="short",
        lang="en",
        instructions="Focus on facts about psychology"
    )

    for i, q in enumerate(questions, start=1):
        print(f"\nQuestion {i}: {q['question']}\n")
