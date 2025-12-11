import os
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from google.genai.errors import APIError
from config import CONFIG

# --- SETUP LOGGING ---
if not os.path.exists(CONFIG.LOG_DIR):
    os.makedirs(CONFIG.LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(CONFIG.LOG_DIR, "debug.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CurriculumGenerator:
    def __init__(self, config):
        self.config = config

        # 1. Validate API Key
        if not config.GEMINI_API_KEY:
            logger.critical("❌ GEMINI_API_KEY is missing! Check .env file.")
            raise ValueError("API Key missing.")

        # 2. Initialize Client
        try:
            self.client = genai.Client(api_key=config.GEMINI_API_KEY)
            logger.info(f"✅ Client Initialized. Key: {config.GEMINI_API_KEY[:4]}...****")
        except Exception as e:
            logger.critical(f"❌ Failed to initialize Client: {e}")
            raise

        self.master_prompt = ""
        self.load_master_prompt()

        # 3. Connection Test
        self.test_api_connection()

    def load_master_prompt(self):
        # The "Book of Everything" Prompt
        self.master_prompt = (
            "You are writing a chapter for **'The Book of Everything'**, written specifically "
            "for a **High-Agency Polymath** (Software Engineer/Entrepreneur). "
            "INSTRUCTIONS:\n"
            "1. **FIRST PRINCIPLES:** Define the topic at its atomic level.\n"
            "2. **DEEP DIVE:** Explain the mechanics, math, and logic rigorously.\n"
            "3. **SYSTEMS VIEW:** Connect this topic to other fields (Business/Biology/Code).\n"
            "4. **FORMAT:** Dense, narrative paragraphs optimized for Audio Learning. No fluff.\n\n"
            "TOPIC TO TEACH:\n"
        )

    def test_api_connection(self):
        """Runs a single cheap request to verify auth/quota."""
        logger.info("🧪 Testing API Connection with 1 request...")
        try:
            self.client.models.generate_content(
                model=self.config.GEMINI_MODELS[5],
                contents="Hello, echo 'Connection Successful'.",
            )
            logger.info("✅ Connection Verified! Starting Engine...")
        except Exception as e:
            logger.critical(f"❌ CONNECTION TEST FAILED: {e}")
            logger.critical("   -> Check your API Key.")
            logger.critical("   -> Check if you have Billing enabled in Google Cloud Console.")
            raise ConnectionError("API Test Failed")

    def _call_gemini_with_fallback(self, query: str) -> str:
        """Waterfall Model Cascade with detailed error logging."""
        for model_name in self.config.GEMINI_MODELS:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=query,
                    config={"max_output_tokens": self.config.MAX_TOKENS}
                )

                # Validation check
                if not response.text:
                    logger.warning(f"⚠️  Empty response from {model_name}")
                    continue

                return response.text.strip()

            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg:
                    logger.warning(f"⏳ Rate Limit (429) on {model_name}. Cooling down...")
                    time.sleep(2)
                elif "404" in err_msg:
                    logger.error(f"🚫 Model Not Found (404): {model_name}")
                elif "401" in err_msg or "403" in err_msg:
                    logger.critical(f"⛔ Auth Error (401/403) on {model_name}: Check Key/Permissions!")
                    return None # Fatal
                else:
                    logger.error(f"💥 Error on {model_name}: {err_msg}")

        return None # Failed all models

    def generate_and_cache_topic(self, full_topic_path: str) -> dict:
        try:
            # Parse path
            path_part, topic_part = full_topic_path.split(":", 1)
            broad_cat, sub_cat = path_part.split("/", 1)
            topic = topic_part.strip()
        except Exception as e:
            logger.error(f"Format Error: {full_topic_path} | {e}")
            return {"topic": full_topic_path, "status": "ERROR"}

        # Define Path
        folder_path = os.path.join(self.config.CACHE_DIR, broad_cat, sub_cat)
        file_name = f"{topic.replace(' ', '_').replace('/', '_')[:60]}.md"
        file_path = os.path.join(folder_path, file_name)

        # Check Cache
        if os.path.exists(file_path):
            return {"topic": topic, "status": "SKIPPED"}

        # Generate
        full_query = self.master_prompt + topic
        content = self._call_gemini_with_fallback(full_query)

        if content:
            os.makedirs(folder_path, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"topic": topic, "status": "GENERATED"}
        else:
            return {"topic": topic, "status": "FAILED"}

    def run_parallel_generation(self):
        topic_list = self.config.get_full_topic_list()
        logger.info(f"🚀 ENGINE START: {len(topic_list)} Topics | {self.config.MAX_WORKERS} Workers")

        results = []
        with ThreadPoolExecutor(max_workers=self.config.MAX_WORKERS) as executor:
            future_to_topic = {
                executor.submit(self.generate_and_cache_topic, t): t
                for t in topic_list
            }

            for future in as_completed(future_to_topic):
                res = future.result()
                results.append(res)

                # Log status
                if res['status'] == "GENERATED":
                    logger.info(f"🔹 Generated: {res['topic'][:40]}")
                elif res['status'] == "FAILED":
                    logger.error(f"🔻 Failed: {res['topic'][:40]}")

        success = sum(1 for r in results if r['status'] in ['GENERATED', 'SKIPPED'])
        logger.info(f"✅ COMPLETE. Success: {success}/{len(results)}")

if __name__ == "__main__":
    # Ensure dirs exist
    os.makedirs(CONFIG.CACHE_DIR, exist_ok=True)
    os.makedirs(CONFIG.LOG_DIR, exist_ok=True)

    generator = CurriculumGenerator(CONFIG)
    generator.run_parallel_generation()