import os
import google.generativeai as genai
from typing import List

# Try to get API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class RAGAgent:
    def __init__(self, vector_store_module):
        self.vector_store = vector_store_module
        self.model = None
        if GOOGLE_API_KEY:
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            print("Warning: GOOGLE_API_KEY not found. Agent will be in dummy mode.")

    def ask(self, query: str, history: List[dict] = []) -> str:
        # 0. Contextualize Query (if history exists)
        search_query = query
        if history and self.model:
            # Create a standalone query based on history
            history_context = "\n".join([f"{msg.get('role')}: {msg.get('content')}" for msg in history[-3:]])
            rewrite_prompt = f"""Given the following conversation history and a follow-up question, rephrase the follow-up question to be a standalone question.
            
            History:
            {history_context}
            
            Follow-up Question: {query}
            
            Standalone Question:"""
            
            try:
                # Ensure we don't block forever, simple generation
                response = self.model.generate_content(rewrite_prompt)
                search_query = response.text.strip()
                print(f"DEBUG: Rewrote '{query}' to '{search_query}'")
            except Exception as e:
                print(f"Error rewriting query: {e}")

        # 1. Search Knowledge Base (with standalone query)
        print(f"Agent thinking: Searching Knowledge Base for '{search_query}'...")
        vector_results = self.vector_store.vector_search(search_query, limit=3)
        
        context_parts = []
        source_used = "Knowledge Base"

        # Check quality of vector results
        if vector_results:
            context_parts.append("--- Knowledge Base Results ---")
            for res in vector_results:
                context_parts.append(f"- {res.get('content')} (Score: {res.get('score', 0):.4f})")
        
        # 2. Decision: Should we search the Web?
        top_score = vector_results[0].get('score', 0) if vector_results else 0
        print(f"Top Vector Score: {top_score}")

        if top_score < 0.75:
            print("Score is low. Searching the Web...")
            source_used += " + Web Search"
            try:
                # Try relative import first (standard for packages)
                from .tools import search_web
            except ImportError:
                try:
                    # Try absolute import from backend package
                    from backend.tools import search_web
                except ImportError:
                    # Try direct import if path is set
                    from tools import search_web
            
            try:
                web_results = search_web(search_query, limit=3)
                if web_results:
                     context_parts.append("\n--- Web Search Results ---")
                     for res in web_results:
                         context_parts.append(f"- [{res.get('title')}] {res.get('body')} (Source: {res.get('href')})")
            except Exception as e:
                print(f"Web search failed: {e}")

        final_context = "\n".join(context_parts)
        
        # Format History
        history_text = ""
        if history:
            history_text = "--- Conversation History ---\n"
            for msg in history[-5:]: # Last 5 messages
                role = "User" if msg.get("role") == "user" else "Assistant"
                history_text += f"{role}: {msg.get('content')}\n"

        # 3. Generate Answer
        if self.model:
            prompt = f"""You are a helpful assistant. Use the provided context and conversation history to answer the user's question.
            If the answer is found in the Knowledge Base, prioritize that.
            If the answer is found in the Web Search results, use that.
            If the answer is not found, say you don't know.
            
            {history_text}
            
            Context:
            {final_context}
            
            Current Question: {query}
            
            Answer:"""
            
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"Error generating response: {e}"
        else:
            return f"[Dummy Agent] Sources: {source_used}\nContext:\n{final_context}\n(Configure GOOGLE_API_KEY)"
