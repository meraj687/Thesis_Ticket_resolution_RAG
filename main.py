from app.llm.prompt_builder import PromptBuilder
from app.llm.ollama_client import OllamaClient
from app.retriever.retriever import SemanticRetriever


def main():

    retriever = SemanticRetriever()

    query = "Material master replication stopped after DRF execution."

    results = retriever.search(query, top_k=3)

    records = [r["record"] for r in results]

    prompt = PromptBuilder.build(query, records)

    client = OllamaClient()

    print("\nGenerating AI Recommendation...\n")

    answer = client.generate(prompt)

    print("=" * 80)
    print(answer)
    print("=" * 80)


if __name__ == "__main__":
    main()