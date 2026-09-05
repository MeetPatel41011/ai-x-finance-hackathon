import os
import chromadb
from anthropic import Anthropic

class ContextSynthesizer:
    def __init__(self):
        # Use an ephemeral in-memory Chroma client for the hackathon
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name="fpa_memory")
        self.run_counter = 1
        
    def synthesize_narrative(self, raw_forensic_report: str) -> str:
        """
        Agent 3 (Claude 3.5 Sonnet): Turns raw findings into executive narratives, 
        learning from prior cycles via ChromaDB.
        """
        print("[Context Synthesizer] Querying memory for past insights...")
        
        # Query past reports (if any exist)
        past_insights = "None (First Run)"
        if self.collection.count() > 0:
            results = self.collection.query(
                query_texts=[raw_forensic_report],
                n_results=1
            )
            if results['documents'] and results['documents'][0]:
                past_insights = results['documents'][0][0]
                
        prompt = f"""
        You are the CFO. Your job is to summarize this raw forensic report into a concise executive brief.
        
        RAW FORENSIC REPORT:
        {raw_forensic_report}
        
        PAST INSIGHTS (DO NOT REPEAT THESE GENERICALLY):
        {past_insights}
        
        Write a concise, 3-sentence summary of what changed and why, avoiding generic observations.
        Focus heavily on exact dollar amounts and the specific business drivers.
        """
        
        print("[Context Synthesizer] Drafting final executive narrative via Claude 3.5 Sonnet...")
        try:
            client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model='claude-sonnet-5',
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            final_narrative = "".join(block.text for block in response.content if hasattr(block, 'text'))
            
            # Store the new narrative in memory for future runs
            self.collection.add(
                documents=[final_narrative],
                metadatas=[{"run_id": f"run_{self.run_counter}"}],
                ids=[f"id_{self.run_counter}"]
            )
            self.run_counter += 1
            
            return final_narrative
        except Exception as e:
            print(f"[Context Synthesizer] Error during synthesis: {e}")
            return "Failed to synthesize narrative."
