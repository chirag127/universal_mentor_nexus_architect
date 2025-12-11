import os
import time
from typing import Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from google.genai.errors import APIError
from config import CONFIG

class CurriculumGenerator:
    def __init__(self, config):
        self.config = config
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.master_prompt = ""
        self.load_master_prompt()

    def load_master_prompt(self):
        self.master_prompt = (
            "You are the **Universal Mentor AI**, architecting the life blueprint "
            "for Chirag Singhal. PRIMARY GOAL: Generate content that teaches the "
            "topic below, prioritizing knowledge for **Fastest Wealth, Universal "
            "Mastery, and a Nobel Prize in AI/Computational Economics.**\n\n"
            "CONTEXT:\n"
            "1. **USER STATUS:** 23, SWE at TCS. Starting at **LEVEL 0** technical skill.\n"
            "2. **FINANCIAL MANDATE:** Maximize ROI from: 3Cr Cattle Feed business & "
            "100-gaj Real Estate plots in Ghaziabad.\n"
            "3. **OUTPUT FORMAT:** Optimized for text-to-speech (Moon Reader). Clear headings.\n\n"
            "INSTRUCTIONS FOR OUTPUT:\n"
            "1. **TITLE:** Use the topic name exactly.\n"
            "2. **SUMMARY:** Dense, scientific summary (No fluff).\n"
            "3. **IMPORTANCE (Chirag Context):** Link to Wealth/Nobel goals.\n"
            "4. **ACTIONABLE STEPS:** 3-5 immediate exercises/tasks.\n"
            "5. **FORMAT:** Markdown.\n\n"
            "GENERATE CONTENT FOR THIS TOPIC:\n"
        )

    def _call_gemini_with_fallback(self, query: str) -> Tuple[str, str]:
        """Waterfall Model Cascade."""
        for model_name in self.config.GEMINI_MODELS:
            # Retry once per model
            for attempt in range(1):
                try:
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=query,
                        config={"max_output_tokens": self.config.MAX_TOKENS}
                    )
                    content = response.text.strip()
                    if not content: raise APIError("Empty response.")
                    return content, model_name
                except Exception:
                    time.sleep(0.5)
        return "FATAL API ERROR", "FAILED_ALL"

    def generate_and_cache_topic(self, full_topic_path: str) -> dict:
        try:
            # Parse: BROAD/SUB: Topic
            path_part, topic_part = full_topic_path.split(":", 1)
            broad_cat, sub_cat = path_part.split("/", 1)
            topic = topic_part.strip()
        except Exception:
            return {"topic": full_topic_path, "status": "ERROR_FORMAT", "model": "N/A"}

        folder_path = os.path.join(self.config.CACHE_DIR, broad_cat, sub_cat)
        file_name = f"{topic.replace(' ', '_').replace('/', '_')[:60]}.md"
        file_path = os.path.join(folder_path, file_name)

        if os.path.exists(file_path):
            return {"topic": topic, "status": "CACHE_HIT", "model": "N/A"}

        full_query = self.master_prompt + topic
        content, model_used = self._call_gemini_with_fallback(full_query)

        if model_used != "FAILED_ALL":
            os.makedirs(folder_path, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"topic": topic, "status": "GENERATED", "model": model_used}
        else:
            return {"topic": topic, "status": "FATAL_FAILURE", "model": "FAILED_ALL"}

    def run_parallel_generation(self):
        topic_list = self.config.get_full_topic_list()
        print(f"🚀 Launching Apex Architecture: {len(topic_list)} Topics | {self.config.MAX_WORKERS} Workers")

        results = []
        with ThreadPoolExecutor(max_workers=self.config.MAX_WORKERS) as executor:
            future_to_topic = {
                executor.submit(self.generate_and_cache_topic, t): t
                for t in topic_list
            }

            for future in as_completed(future_to_topic):
                res = future.result()
                results.append(res)

                # Color Coded Output
                color = "\033[92m" if res['status'] == "CACHE_HIT" else "\033[94m" if res['status'] == "GENERATED" else "\033[91m"
                print(f"{color}[{res['status']:<10}] {res['topic'][:50]:<50} ({res['model']})\033[0m")

        print(f"\n✅ EXECUTION COMPLETE.")

if __name__ == "__main__":
    os.makedirs(CONFIG.CACHE_DIR, exist_ok=True)
    generator = CurriculumGenerator(CONFIG)
    generator.run_parallel_generation()