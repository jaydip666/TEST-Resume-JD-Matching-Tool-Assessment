"""
Curated skills taxonomy for the Resume-JD Matching Tool.

The list is intentionally broad (tech + soft skills) and organized as
"canonical name -> list of surface forms / aliases" so that variations
like "Node.js" / "NodeJS" / "Node" all resolve to one skill.
"""

SKILLS_TAXONOMY = {
    # Programming languages
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "csharp"],
    "C": [r"\bc\b"],
    "Go": ["golang", r"\bgo\b"],
    "Ruby": ["ruby"],
    "PHP": ["php"],
    "R": [r"\br\b"],
    "Scala": ["scala"],
    "Kotlin": ["kotlin"],
    "Swift": ["swift"],
    "SQL": ["sql"],
    "Bash": ["bash", "shell scripting"],

    # Web / frameworks
    "React": ["react", "reactjs", "react.js"],
    "Angular": ["angular"],
    "Vue.js": ["vue", "vuejs", "vue.js"],
    "Node.js": ["node", "nodejs", "node.js"],
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "Streamlit": ["streamlit"],
    "Express.js": ["express", "expressjs", "express.js"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "REST API": ["rest api", "restful", "rest"],
    "GraphQL": ["graphql"],

    # Data / AI / ML
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "dl"],
    "Natural Language Processing": ["natural language processing", "nlp"],
    "Computer Vision": ["computer vision", "cv"],
    "LLM": ["llm", "large language model", "large language models"],
    "Generative AI": ["generative ai", "genai", "gen ai"],
    "Prompt Engineering": ["prompt engineering"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch", "torch"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "OpenCV": ["opencv"],
    "Hugging Face": ["hugging face", "huggingface", "transformers"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Data Visualization": ["data visualization", "data viz"],
    "Statistics": ["statistics", "statistical analysis"],
    "spaCy": ["spacy"],
    "NLTK": ["nltk"],
    "OpenAI API": ["openai api", "openai", "chatgpt api", "gpt"],
    "LangChain": ["langchain"],
    "Vector Databases": ["vector database", "vector db", "embeddings", "faiss", "pinecone", "chromadb"],

    # Databases
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MongoDB": ["mongodb", "mongo"],
    "Redis": ["redis"],
    "SQLite": ["sqlite"],
    "Firebase": ["firebase"],

    # Cloud / DevOps
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "Google Cloud Platform": ["gcp", "google cloud"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "CI/CD": ["ci/cd", "ci-cd", "continuous integration", "continuous deployment"],
    "Git": ["git", "github", "gitlab", "version control"],
    "Linux": ["linux", "unix"],

    # Tools / general
    "Jupyter Notebook": ["jupyter"],
    "Excel": ["excel", "ms excel"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "APIs": ["api integration", "third-party apis", "api development"],
    "Agile/Scrum": ["agile", "scrum"],
    "Testing/QA": ["unit testing", "testing", "qa", "quality assurance", "pytest"],

    # Soft skills
    "Communication": ["communication skills", "communication"],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Teamwork": ["teamwork", "collaboration"],
    "Time Management": ["time management"],
    "Critical Thinking": ["critical thinking"],
    "Adaptability": ["adaptability"],
    "Leadership": ["leadership"],
    "Attention to Detail": ["attention to detail"],
}

# Keywords that (when found near a sentence containing a skill) signal
# that a JD skill is a "must-have" vs a "nice-to-have".
MUST_HAVE_MARKERS = [
    "must have", "must-have", "required", "requirement", "mandatory",
    "essential", "need to have", "should have strong", "minimum qualification",
    "you have", "you must", "proficient in", "strong knowledge of",
    "hands-on experience", "solid understanding",
]

NICE_TO_HAVE_MARKERS = [
    "nice to have", "nice-to-have", "preferred", "plus", "bonus",
    "good to have", "advantageous", "a plus", "added advantage",
    "familiarity with", "exposure to", "would be a plus",
]
