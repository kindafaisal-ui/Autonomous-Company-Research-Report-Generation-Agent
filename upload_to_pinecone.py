import os
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY")
INDEX_NAME       = os.getenv("PINECONE_INDEX_NAME")

documents = [
    {
        "id": "doc_report_template",
        "text": """Company Intelligence Report Template.
        Required sections in order:
        1. EXECUTIVE SUMMARY: 3-5 bullets what to know, 1-2 bullets why it matters, 1-2 watch items.
        2. COMPANY OVERVIEW: founded, headquarters, sector, business model, core products, key leadership.
        3. FINANCIAL SNAPSHOT: revenue scale, market cap, profitability signals, note data limitations honestly.
        4. RECENT NEWS AND DEVELOPMENTS: 3-5 items tagged as Strategic, Financial, Operational, or Reputational.
        5. MARKET POSITION AND COMPETITORS: primary market, direct competitors named, differentiation, moat assessment.
        6. STRATEGIC ASSESSMENT: key strengths, key risks, strategic direction signals, analyst watch items.
        Validation rule: report is only complete when all 6 sections are present."""
    },
    {
        "id": "doc_competitor_mapping",
        "text": """Competitor Mapping Framework.
        Categories: Direct Competitors (same product same market),
        Indirect Competitors (different product same problem),
        Substitute Threats (captures same budget),
        Adjacent Entrants (moving in from nearby markets),
        Investor Comparables (analyst benchmarks).
        For each competitor: name, category, one sentence why they matter, recent moves if found.
        If only 1-2 competitors found say so honestly. Do not fabricate competitors."""
    },
    {
        "id": "doc_moat_framework",
        "text": """Moat and Competitive Advantage Framework.
        Moat types: Brand (recognition and pricing power),
        Switching Costs (locked in by integrations or contracts),
        Network Effects (value grows with more users),
        Scale Advantages (lower unit costs due to size),
        Intellectual Property (patents, algorithms, licenses),
        Distribution (hard to replicate customer access),
        Data Advantage (proprietary dataset enables AI edge),
        Regulatory Moat (licenses block new entrants),
        Operational Excellence (execution competitors cannot match).
        Identify 1-3 moats with strength rating: Strong, Moderate, Emerging, or Unclear.
        If no clear moat found state: moat unclear from available data."""
    },
    {
        "id": "doc_signals_playbook",
        "text": """Strategic Signals Playbook.
        Signal types and meanings:
        M&A Activity: acquiring signals capability gaps being filled; being acquired signals exit or consolidation.
        Partnerships: signals distribution expansion or technology access.
        Capital Expenditure or Fundraising: large capex signals infrastructure bet; new funding signals growth stage.
        Hiring Patterns: AI hiring signals product transformation; layoffs signal restructuring.
        Product Launches: new product signals R&D output and new revenue stream.
        Geographic Expansion: new markets signal growth ambition.
        Channel Shifts: moving direct signals margin improvement; moving to enterprise signals maturation.
        Regulatory News: signals risk exposure and compliance costs.
        For each news item identify signal type, write one sentence on strategic meaning,
        flag as positive, neutral, or negative for the company."""
    }
]

print("Connecting...")
openai_client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)
print(f"Connected to index: {INDEX_NAME}")

for doc in documents:
    print(f"\nEmbedding: {doc['id']}...")
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=doc["text"]
    )
    embedding = response.data[0].embedding
    print(f"  Dimensions: {len(embedding)}")
    index.upsert(vectors=[{
        "id": doc["id"],
        "values": embedding,
        "metadata": {"text": doc["text"], "doc_id": doc["id"]}
    }])
    print(f"  Uploaded: {doc['id']}")

print("\n✅ All 4 documents uploaded!")
stats = index.describe_index_stats()
print(f"Total vectors in index: {stats['total_vector_count']}")
