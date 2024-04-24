import ollama
import chromadb

class LlamaRAG:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(name=f"{agent_name}_docs")

    def store_documents(self, documents):
        for i, d in enumerate(documents):
            response = ollama.embeddings(
                model="mxbai-embed-large",
                prompt=d["content"]
            )
            embedding = response["embedding"]
            self.collection.add(
                ids=[f"{d['role']}_{i}"],
                embeddings=[embedding],
                documents=[d["content"]],
                metadatas=[{"role": d["role"]}]
            )

    def query_documents(self, prompt, n_results=3):
        response = ollama.embeddings(
            model="mxbai-embed-large",
            prompt=prompt
        )
        results = self.collection.query(
            query_embeddings=[response["embedding"]],
            n_results=n_results,
            include=["documents", "metadatas"]
        )

        relevant_docs = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            relevant_docs.append({
                "role": metadata["role"],
                "content": doc
            })

        return relevant_docs

    def generate_response(self, prompt, relevant_docs):
        context = "\n".join([f"{doc['role']}: {doc['content']}" for doc in relevant_docs])
        full_prompt = f"Relevant context:\n{context}\n\nPrompt: {prompt}\n\nResponse:"

        output = ollama.generate(
            model="stablelm2",
            prompt=full_prompt,

            
        )

        return output['response'].strip()

    def research(self, topic):
        search_query = f"Research topic: {topic}"
        relevant_docs = self.query_documents(search_query, n_results=5)
        research_summary = "\n".join([f"{doc['content']}" for doc in relevant_docs])
        return research_summary

    def test_code(self, code):
        # Implement code testing logic using the Ollama library if needed
        pass

    def chat(self, user_input, system_message, memory, model, temperature):
        self.store_documents(memory)

        if "Research topic:" in user_input:
            topic = user_input.split("Research topic:")[1].strip()
            research_summary = self.research(topic)
            memory.append({"role": "system", "content": f"Research summary for topic '{topic}':\n{research_summary}"})
            return f"Research completed for topic: {topic}. Summary added to memory."

        relevant_docs = self.query_documents(user_input)

        messages = [
            {"role": "system", "content": system_message},
            *[{"role": doc["role"], "content": doc["content"]} for doc in relevant_docs],
            {"role": "user", "content": user_input}
        ]

        response_content = self.generate_response(user_input, relevant_docs)

        if "```python" in response_content:
            code_block = response_content.split("```python")[1].split("```")[0]
            test_result = self.test_code(code_block)
            response_content += f"\n\nCode testing result: {test_result}"

        truncated_response = response_content[:1000]
        memory.append({"role": "assistant", "content": truncated_response})

        return response_content