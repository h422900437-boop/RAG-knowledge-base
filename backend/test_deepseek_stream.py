#!/usr/bin/env python3
"""
Test if DeepSeek actually supports streaming
"""
import os
from langchain_openai import ChatOpenAI
import time

token_api = os.environ.get("DEEPSEEK_TOKEN")

if not token_api:
    print("❌ Error: DEEPSEEK_TOKEN not set")
    print("Set it with: export DEEPSEEK_TOKEN='your_token'")
    exit(1)

print("🧪 Testing DeepSeek Streaming Support\n")

llm = ChatOpenAI(
    model_name="deepseek-v4-flash",
    temperature=0.2,
    openai_api_key=token_api,
    openai_api_base="https://api.deepseek.com",
)

prompt = "What is 2+2? Answer very concisely in 2-3 sentences."

print("=" * 60)
print("📝 Prompt: What is 2+2? Answer very concisely in 2-3 sentences.")
print("=" * 60)

print("\n🔄 Streaming response:\n")

start_time = time.time()
chunk_count = 0

try:
    for chunk in llm.stream(prompt):
        chunk_count += 1
        if chunk.content:
            print(chunk.content, end="", flush=True)
            # Add a small delay to see if streaming is actually happening
            time.sleep(0.01)

    elapsed = time.time() - start_time
    print(f"\n\n{'=' * 60}")
    print(f"✅ Streaming completed!")
    print(f"📊 Chunks received: {chunk_count}")
    print(f"⏱️  Total time: {elapsed:.2f} seconds")
    print(f"📈 Avg time per chunk: {elapsed/chunk_count*1000:.1f}ms")

    if chunk_count <= 1:
        print("\n⚠️  WARNING: Only 1 chunk received!")
        print("   This means DeepSeek is NOT streaming - returning full response at once")
        print("   This is likely a DeepSeek API limitation or configuration issue")
    else:
        print("\n✅ True streaming detected!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
