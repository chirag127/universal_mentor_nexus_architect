import os
import time
import logging
import openai
from concurrent.futures import ThreadPoolExecutor, as_completed
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

        if not config.CEREBRAS_API_KEY:
            logger.critical("❌ CEREBRAS_API_KEY is missing! Check .env file.")
            raise ValueError("API Key missing.")

        try:
            # Initialize OpenAI Client pointing to Cerebras
            self.client = openai.OpenAI(
                base_url=config.BASE_URL,
                api_key=config.CEREBRAS_API_KEY
            )
            logger.info(f"✅ Cerebras (OpenAI) Client Initialized. Key: {config.CEREBRAS_API_KEY[:4]}...****")
        except Exception as e:
            logger.critical(f"❌ Failed to initialize Client: {e}")
            raise

        self.master_prompt = ""
        self.load_master_prompt()

        # Connection Test
        self.test_api_connection()

    def load_master_prompt(self):
        # --- THE AUDIOBOOK PROMPT ---
        self.master_prompt = (
            "You are an **Expert Technical Audiobook Writer** and **Universal Polymath Tutor**. "
            "Your goal is to write a chapter for **'The Book of Everything'** specifically designed "
            "to be **listened to** via Text-to-Speech (Moon Reader Pro). The listener is a "
            "High-Agency Software Engineer/Entrepreneur aiming for Nobel-level mastery.\n\n"
            "### CORE INSTRUCTIONS (AUDIO OPTIMIZATION):\n"
            "1. **NARRATIVE FLOW (CRITICAL):** Write as a continuous, engaging narrative. **DO NOT use bullet points, "
            "numbered lists, or markdown tables**, as these sound terrible in TTS. Use full, rhythmic sentences.\n"
            "2. **DESCRIBE, DON'T DISPLAY:** Never output raw code blocks, SQL queries, or mathematical notation verbatim. "
            "Instead, describe the logic in natural English (e.g., instead of 'print(x)', write 'The system outputs the variable x...').\n"
            "3. **VISUALIZATION:** If explaining a diagram or formula, describe it vividly so the listener can visualize it mentally.\n"
            "4. **NO FILLER:** Do not use phrases like 'Here is the chapter' or 'In this section'. Jump straight into the knowledge.\n\n"
            "### CONTENT REQUIREMENTS (POLYMATH DEPTH):\n"
            "1. **FIRST PRINCIPLES:** Start by defining the topic at its atomic, fundamental level. What is the absolute truth here?\n"
            "2. **THE DEEP DIVE:** Explain the mechanics rigorously. If it's Math/AI, explain the logic flow. If Business, explain the unit economics. "
            "Make it dense but speakable.\n"
            "3. **SYSTEMS VIEW:** Connect this topic to other fields (e.g., connect Biology to Engineering, or History to Economics).\n\n"
            "**TOPIC TO TEACH:**\n"
        )

    def test_api_connection(self):
        """Runs a single cheap request to verify auth/quota."""
        logger.info("🧪 Testing Cerebras Connection...")
        try:
            self.client.chat.completions.create(
                model=self.config.MODELS[-1], # Use smallest model for test
                messages=[{"role": "user", "content": "Echo: System Operational."}],
            )
            logger.info("✅ Connection Verified! Starting Engine...")
        except Exception as e:
            logger.critical(f"❌ CONNECTION TEST FAILED: {e}")
            raise ConnectionError("API Test Failed")

    def _call_cerebras_with_fallback(self, query: str) -> str:
        """Waterfall Model Cascade for Cerebras."""
        for model_name in self.config.MODELS:
            try:
                # OpenAI-Style Call
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": query}
                    ],
                    max_tokens=self.config.MAX_TOKENS
                )

                content = response.choices[0].message.content.strip()

                if not content:
                    logger.warning(f"⚠️  Empty response from {model_name}")
                    continue

                return content

            except Exception as e:
                err_msg = str(e)
                # Handle Rate Limits
                if "429" in err_msg:
                    logger.warning(f"⏳ Rate Limit (429) on {model_name}. Cooling down...")
                    time.sleep(1)
                # Handle Auth/Server Errors
                elif "401" in err_msg or "403" in err_msg:
                    logger.critical(f"⛔ Auth Error on {model_name}: Check Key!")
                    return None
                else:
                    logger.error(f"💥 Error on {model_name}: {err_msg}")

        return None

    def generate_and_cache_topic(self, full_topic_path: str) -> dict:
        try:
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
        content = self._call_cerebras_with_fallback(full_query)

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

                if res['status'] == "GENERATED":
                    logger.info(f"🔹 Generated: {res['topic'][:40]}")
                elif res['status'] == "FAILED":
                    logger.error(f"🔻 Failed: {res['topic'][:40]}")

        success = sum(1 for r in results if r['status'] in ['GENERATED', 'SKIPPED'])
        logger.info(f"✅ COMPLETE. Success: {success}/{len(results)}")

if __name__ == "__main__":
    if not os.path.exists(CONFIG.CACHE_DIR):
        os.makedirs(CONFIG.CACHE_DIR, exist_ok=True)
    if not os.path.exists(CONFIG.LOG_DIR):
        os.makedirs(CONFIG.LOG_DIR, exist_ok=True)

    generator = CurriculumGenerator(CONFIG)
    generator.run_parallel_generation()