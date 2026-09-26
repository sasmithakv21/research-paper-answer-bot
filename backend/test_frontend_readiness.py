import os
import sys
import time
import requests
import subprocess
from pathlib import Path

# Fix Windows console UTF-8 printing
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from app.core.config import PAPERS_DIR

def run_tests():
    print("=" * 70)
    print("      FRONTEND READINESS BACKEND AUDIT TEST SUITE")
    print("=" * 70)

    # 1. Start FastAPI server process
    python_exe = sys.executable
    server_process = subprocess.Popen(
        [python_exe, "-m", "uvicorn", "app.main:app", "--port", "8000"],
        cwd=str(BASE_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)  # Wait for server startup

    real_pdf_path = Path(PAPERS_DIR) / "attention_is_all_you_need.pdf"

    test_results = {}
    sample_responses = {}

    try:
        # A. GET /api/papers
        print("\n[TEST A] GET /api/papers...")
        res_a = requests.get("http://localhost:8000/api/papers", timeout=5)
        print(f"  Status: {res_a.status_code}")
        print(f"  Response JSON: {res_a.json()}")
        if res_a.status_code == 200 and "papers" in res_a.json():
            test_results["GET /api/papers"] = "PASS"
            sample_responses["GET /api/papers"] = res_a.json()
        else:
            test_results["GET /api/papers"] = "FAIL"

        # B. POST /api/upload with a real PDF
        print("\n[TEST B] POST /api/upload with real PDF...")
        with open(real_pdf_path, "rb") as f:
            pdf_bytes = f.read()
        files_b = {"file": ("attention_is_all_you_need.pdf", pdf_bytes, "application/pdf")}
        res_b = requests.post("http://localhost:8000/api/upload", files=files_b, timeout=30)
        print(f"  Status: {res_b.status_code}")
        print(f"  Response JSON: {res_b.json()}")
        if res_b.status_code == 200 and res_b.json().get("status") == "success":
            test_results["POST /api/upload (real PDF)"] = "PASS"
            sample_responses["POST /api/upload"] = res_b.json()
        else:
            test_results["POST /api/upload (real PDF)"] = "FAIL"

        # C. POST /api/upload with a non-PDF file
        print("\n[TEST C] POST /api/upload with non-PDF...")
        files_c = {"file": ("test.txt", b"Plain text content", "text/plain")}
        res_c = requests.post("http://localhost:8000/api/upload", files=files_c, timeout=5)
        print(f"  Status: {res_c.status_code}")
        print(f"  Response JSON: {res_c.json()}")
        if res_c.status_code == 400:
            test_results["POST /api/upload (non-PDF)"] = "PASS"
        else:
            test_results["POST /api/upload (non-PDF)"] = "FAIL"

        # D. POST /api/chat with a real question
        print("\n[TEST D] POST /api/chat with real question...")
        payload_d = {"question": "What is the Transformer architecture and multi-head attention?"}
        res_d = requests.post("http://localhost:8000/api/chat", json=payload_d, timeout=20)
        print(f"  Status: {res_d.status_code}")
        json_d = res_d.json()
        print(f"  Response JSON keys: {list(json_d.keys())}")
        if res_d.status_code == 200 and "answer" in json_d and "sources" in json_d:
            test_results["POST /api/chat (real question)"] = "PASS"
            sample_responses["POST /api/chat"] = {
                "answer": json_d["answer"][:150] + "...",
                "sources": json_d["sources"]
            }
        else:
            test_results["POST /api/chat (real question)"] = "FAIL"

        # E. POST /api/chat with an empty question
        print("\n[TEST E] POST /api/chat with empty question...")
        payload_e = {"question": "   "}
        res_e = requests.post("http://localhost:8000/api/chat", json=payload_e, timeout=5)
        print(f"  Status: {res_e.status_code}")
        print(f"  Response JSON: {res_e.json()}")
        if res_e.status_code == 400:
            test_results["POST /api/chat (empty question)"] = "PASS"
        else:
            test_results["POST /api/chat (empty question)"] = "FAIL"

        # F. Duplicate PDF upload check
        print("\n[TEST F] Duplicate PDF upload check...")
        files_f = {"file": ("attention_is_all_you_need.pdf", pdf_bytes, "application/pdf")}
        res_f = requests.post("http://localhost:8000/api/upload", files=files_f, timeout=30)
        print(f"  Status: {res_f.status_code}")
        print(f"  Response JSON: {res_f.json()}")
        if res_f.status_code == 200 and res_f.json().get("status") == "success":
            test_results["Duplicate PDF upload"] = "PASS"
        else:
            test_results["Duplicate PDF upload"] = "FAIL"

        # G. Complete upload -> retrieval -> answer flow
        print("\n[TEST G] Complete upload -> retrieval -> answer flow...")
        if test_results.get("POST /api/upload (real PDF)") == "PASS" and test_results.get("POST /api/chat (real question)") == "PASS":
            test_results["Complete upload -> retrieval -> answer flow"] = "PASS"
        else:
            test_results["Complete upload -> retrieval -> answer flow"] = "FAIL"

    finally:
        server_process.terminate()

    print("\n" + "=" * 70)
    print("                 FINAL TEST SUMMARY REPORT")
    print("=" * 70)
    for test_name, result in test_results.items():
        print(f" - {test_name:<45}: {result}")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
