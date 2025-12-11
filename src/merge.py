import os
import markdown
import logging
from config import CONFIG

# --- LOGGING SETUP ---
if not os.path.exists(CONFIG.LOG_DIR):
    os.makedirs(CONFIG.LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(CONFIG.LOG_DIR, "merge.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- CONDITIONAL IMPORT (Prevents Crash on Windows) ---
try:
    from weasyprint import HTML, CSS
    PDF_ENGINE_AVAILABLE = True
except OSError:
    PDF_ENGINE_AVAILABLE = False
    logger.warning("⚠️  GTK3 Runtime not found. PDF generation will be disabled.")
    logger.warning("👉 Fix: Install GTK3 for Windows to enable native PDF generation.")

class ContentArchivist:
    def __init__(self, config):
        self.config = config
        self.master_md_path = os.path.join("data", "THE_BOOK_OF_EVERYTHING.md")
        self.master_html_path = os.path.join("data", "THE_BOOK_OF_EVERYTHING.html")
        self.master_pdf_path = os.path.join("data", "THE_BOOK_OF_EVERYTHING.pdf")

    def merge_content(self):
        """Iterates through the Config Subject Structure to enforce logical order."""
        logger.info("📚 Starting Compilation of 'The Book of Everything'...")

        full_content = []

        # Add Title Page
        full_content.append("# THE BOOK OF EVERYTHING\n")
        full_content.append(f"**Architect:** Chirag Singhal | **Generated:** {os.getenv('USERNAME', 'Apex User')}\n")
        full_content.append(f"**Purpose:** Universal Polymathy (Level 0 -> Nobel)\n\n---\n")

        total_topics = 0
        missing_topics = 0

        # 1. Iterate Broad Subjects (e.g., "01_CORE_THINKING")
        for broad_cat, sub_cats in self.config.SUBJECT_STRUCTURE.items():
            # Add Section Header
            clean_broad = broad_cat.replace("_", " ").title()
            full_content.append(f"\n\n# {clean_broad}\n\n")

            # 2. Iterate Sub Subjects (e.g., "Meta_Learning")
            for sub_cat, topics in sub_cats.items():
                clean_sub = sub_cat.replace("_", " ").title()
                full_content.append(f"\n## {clean_sub}\n\n")

                # 3. Iterate Topics
                for topic in topics:
                    # Construct expected file path (Sanitization matches main.py)
                    file_name = f"{topic.replace(' ', '_').replace('/', '_')[:60]}.md"
                    file_path = os.path.join(self.config.CACHE_DIR, broad_cat, sub_cat, file_name)

                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            text = f.read()
                            # Append logic
                            full_content.append(f"### {topic}\n\n")
                            full_content.append(text)
                            full_content.append("\n\n---\n")
                        total_topics += 1
                    else:
                        logger.warning(f"⚠️ Missing Topic File: {file_path}")
                        missing_topics += 1

        # Write Master Markdown
        with open(self.master_md_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(full_content))

        logger.info(f"✅ Markdown Compilation Complete: {self.master_md_path}")
        logger.info(f"   Topics Merged: {total_topics}")
        logger.info(f"   Missing: {missing_topics}")

        return self.master_md_path

    def convert_to_pdf(self):
        """Converts the Master Markdown to HTML, then attempts PDF."""
        logger.info("⚙️ Converting to HTML...")

        # 1. Read Markdown
        with open(self.master_md_path, 'r', encoding='utf-8') as f:
            md_text = f.read()

        # 2. Convert to HTML with extensions
        html_body = markdown.markdown(md_text, extensions=['extra', 'toc', 'sane_lists'])

        # 3. Add CSS for "Textbook" Look
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Georgia', serif; line-height: 1.6; max-width: 900px; margin: auto; padding: 20px; }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; margin-top: 50px; page-break-before: always; }}
                h2 {{ color: #34495e; margin-top: 30px; border-bottom: 1px solid #ddd; }}
                h3 {{ color: #7f8c8d; margin-top: 20px; text-transform: uppercase; font-size: 1.1em; }}
                p {{ margin-bottom: 15px; text-align: justify; }}
                strong {{ color: #2980b9; }}
                li {{ margin-bottom: 5px; }}
                hr {{ border: 0; height: 1px; background: #ccc; margin: 40px 0; }}
            </style>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """

        # Save HTML (Always succeeds)
        with open(self.master_html_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        logger.info(f"✅ HTML Generated: {self.master_html_path}")

        # 4. Attempt PDF Generation
        if PDF_ENGINE_AVAILABLE:
            try:
                logger.info("⚙️ Rendering PDF (This may take a moment)...")
                HTML(string=full_html).write_pdf(self.master_pdf_path)
                logger.info(f"🎉 PDF SUCCESS: {self.master_pdf_path}")
            except Exception as e:
                logger.error(f"❌ PDF Engine Error: {e}")
        else:
            logger.info("ℹ️  SKIPPING PDF generation (GTK missing).")
            logger.info(f"👉 OPEN THIS FILE IN BROWSER: {os.path.abspath(self.master_html_path)}")

if __name__ == "__main__":
    archivist = ContentArchivist(CONFIG)
    archivist.merge_content()
    archivist.convert_to_pdf()