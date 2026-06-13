import PyPDF2

def extract_skills(path):
    skills = ["Python","Java","AI","ML","SQL"]
    text = ""

    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for p in reader.pages:
            text += p.extract_text()

    return [s for s in skills if s.lower() in text.lower()]




