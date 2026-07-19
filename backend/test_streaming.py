#!/usr/bin/env python3
"""
Test script to verify the streaming response functionality
"""
import requests
import json
import time

BACKEND_URL = "http://127.0.0.1:8000"

def test_streaming():
    """Test the streaming chat endpoint"""
    print("🧪 Testing Streaming Chat Endpoint...\n")

    test_question = "If an employee hasn't gone to work for six consecutive days, what will happen?"

    print(f"📝 Question: {test_question}\n")
    print("=" * 60)
    print("🔄 Streaming Response:\n")

    try:
        # Make request with streaming enabled
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": test_question},
            stream=True,
            timeout=60
        )

        if response.status_code == 200:
            sources_received = False
            response_text = ""
            start_time = time.time()

            # Process streaming response line by line
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    # Check for sources metadata
                    if "[SOURCES]:" in line:
                        sources_received = True
                        source_json = line.split("[SOURCES]:")[-1].strip()
                        try:
                            sources = json.loads(source_json)
                            print("✅ Sources received:")
                            for src in sources:
                                print(f"   - Chunk {src['chunk_id']}: {src['source']}")
                            print()
                        except json.JSONDecodeError:
                            print("⚠️  Failed to parse sources JSON\n")
                    else:
                        # Regular response text
                        response_text += line
                        print(line, end="", flush=True)

            elapsed_time = time.time() - start_time
            print("\n\n" + "=" * 60)
            print(f"✅ Streaming completed in {elapsed_time:.2f} seconds")
            print(f"📊 Response length: {len(response_text)} characters")
            print(f"📌 Sources received: {'Yes' if sources_received else 'No'}")

        else:
            print(f"❌ Backend error: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to backend at {BACKEND_URL}")
        print("   Make sure FastAPI is running: uvicorn backend.main:app --reload")
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_streaming()
