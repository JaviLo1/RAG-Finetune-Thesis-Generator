# RAG-Finetune-Thesis-Generator

This repository contains the RAG-Finetune Thesis Generator, a system designed to generate personalized thesis project proposals for students based on their academic profile and interests.

The tool combines:

Retrieval-Augmented Generation (RAG): to align generated topics with the most relevant courses the student has studied.

Fine-tuned LLMs: trained on real thesis projects to ensure realistic structure, complexity, and academic rigor.

🚀 Features

Extracts relevant courses from the student’s curriculum using a vector database (Chroma, FAISS, Pinecone, or Weaviate).

Creates semantic embeddings of course guides (guías docentes).

Matches student inputs (career, interests, technologies) with top-aligned subjects.

Builds enriched prompts and feeds them into a fine-tuned OpenAI model.

Generates structured thesis proposals with:

📌 Title

📖 Description

🎯 Objectives

🧪 Methodology

🌍 Alignment with UN SDGs (ODS)


🏗️ Project Architecture
flowchart LR
    A[Student Input] --> B[Embeddings Model]
    B --> C[Vector Database]
    C --> D[Retrieve Similar Subjects]
    D --> E[Prompt Maker]
    E --> F[Fine-Tuned Model]
    F --> G[Thesis Proposal Output]


Input:

Career (predefined)

Interests / Technologies

Subjects (retrieved via RAG)

Output:

Thesis title

Description

Objectives

Methodology

ODS (Sustainable Development Goals)
