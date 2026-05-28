"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import time
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD) — update if pricing changes
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"


# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
from openai import OpenAI

def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.

    Args:
        prompt:      The user message to send.
        model:       The OpenAI model to use (default: gpt-4o).
        temperature: Sampling temperature (0.0 – 2.0).
        top_p:       Nucleus sampling threshold.
        max_tokens:  Maximum number of tokens to generate.

    Returns:
        A tuple of (response_text: str, latency_seconds: float).

    Hint:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    """
    # TODO: import OpenAI, create client, call chat.completions.create,
    #       measure start/end time, return (response_text, latency)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [{"role": "user", "content": prompt}]

    start = time.time()
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    end = time.time()

    # Extract text from response (new SDK shape)
    try:
        response_text = resp.choices[0].message.content
    except Exception:
        # Fallback to raw string conversion
        response_text = str(resp)

    latency = end - start
    return response_text, latency

# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API using gpt-4o-mini and return the
    response text + latency.

    Args:
        prompt:      The user message to send.
        temperature: Sampling temperature (0.0 – 2.0).
        top_p:       Nucleus sampling threshold.
        max_tokens:  Maximum number of tokens to generate.

    Returns:
        A tuple of (response_text: str, latency_seconds: float).

    Hint:
        Reuse call_openai() by passing model=OPENAI_MINI_MODEL.
    """
    # Reuse the call_openai helper with the mini model identifier
    return call_openai(
        prompt=prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Call both gpt-4o and gpt-4o-mini with the same prompt and return a
    comparison dictionary.

    Args:
        prompt: The user message to send to both models.

    Returns:
        A dict with keys:
            - "gpt4o_response":      str
            - "mini_response":       str
            - "gpt4o_latency":       float
            - "mini_latency":        float
            - "gpt4o_cost_estimate": float  (estimated USD for the response)

    Hint:
        Cost estimate = (len(response.split()) / 0.75) / 1000 * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
        (0.75 words ≈ 1 token is a rough approximation)
    """
    # Call the full model
    gpt4o_response, gpt4o_latency = call_openai(prompt=prompt)

    # Call the mini model
    mini_response, mini_latency = call_openai_mini(prompt=prompt)

    # Estimate cost for gpt-4o output using hint: (len(words)/0.75)/1000 * cost_per_1k
    words = gpt4o_response.split()
    approx_tokens = (len(words) / 0.75)
    cost_per_1k = COST_PER_1K_OUTPUT_TOKENS.get("gpt-4o", 0.0)
    gpt4o_cost_estimate = (approx_tokens / 1000.0) * cost_per_1k

    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": gpt4o_cost_estimate,
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal.

    Behaviour:
        - Streams tokens from OpenAI as they arrive (print each chunk).
        - Maintains the last 3 conversation turns in history.
        - Typing 'quit' or 'exit' ends the loop.

    Hints:
        - Keep a list `history` of {"role": ..., "content": ...} dicts.
        - Use stream=True in client.chat.completions.create() and iterate:
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                print(delta, end="", flush=True)
        - After each turn, append the assistant reply to history.
        - Trim history to the last 3 turns: history = history[-3:]
    """
    # Interactive loop
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    history: list[dict] = []

    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit"):
                print("Exiting chat...")
                break

            # Append user message to history for context
            history.append({"role": "user", "content": user_input})

            # Build messages payload from history
            messages = history.copy()

            # Stream response
            stream = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                stream=True,
            )

            assistant_reply = ""
            print("Assistant: ", end="", flush=True)
            for chunk in stream:
                # New SDK uses choices[0].delta.content for streamed pieces
                try:
                    delta = chunk.choices[0].delta.content or ""
                except Exception:
                    # Fallback if shape differs
                    delta = getattr(chunk.choices[0].delta, "content", "") or ""
                if delta:
                    print(delta, end="", flush=True)
                    assistant_reply += delta
            print()  # newline after finished stream

            # Append assistant reply to history and trim to last 3 entries
            history.append({"role": "assistant", "content": assistant_reply})
            history = history[-3:]

    except KeyboardInterrupt:
        print("\nInterrupted. Exiting chat...")
        return


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). If it raises an exception, retry up to max_retries times
    with exponential backoff (base_delay * 2^attempt).

    Args:
        fn:          Zero-argument callable to execute.
        max_retries: Maximum number of retry attempts.
        base_delay:  Initial delay in seconds before the first retry.

    Returns:
        The return value of fn() on success.

    Raises:
        The last exception raised by fn() after all retries are exhausted.
    """
    # TODO: implement retry loop with exponential backoff
    last_exc = None
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            last_exc = e
            # If this was the last attempt, re-raise
            if attempt == max_retries - 1:
                break
            # Wait exponential backoff before next retry
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)

    # Retries exhausted; raise the last exception
    if last_exc is not None:
        raise last_exc
    # Fallback (should not happen)
    raise RuntimeError("retry_with_backoff failed without exception")


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Run compare_models on each prompt in the list.

    Args:
        prompts: List of prompt strings.

    Returns:
        List of dicts, each being the compare_models result with an extra
        key "prompt" containing the original prompt string.
    """
    # TODO: iterate over prompts, call compare_models, add "prompt" key
    results = []
    for prompt in prompts:
        result = compare_models(prompt)
        result["prompt"] = prompt
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format a list of compare_models results as a readable text table.

    Args:
        results: List of dicts as returned by batch_compare.

    Returns:
        A formatted string table with columns:
        Prompt | GPT-4o Response | Mini Response | GPT-4o Latency | Mini Latency

    Hint:
        Truncate long text to 40 characters for readability.
    """
    # Build and return a formatted table string
    def trunc(s: str, n: int = 40) -> str:
        if s is None:
            return ""
        s = str(s)
        return s if len(s) <= n else s[: n - 3] + "..."

    # Column widths
    w_prompt = 40
    w_resp = 40
    w_mini = 40
    w_lat = 12

    headers = [
        ("Prompt", w_prompt),
        ("GPT-4o Response", w_resp),
        ("Mini Response", w_mini),
        ("GPT-4o Latency", w_lat),
        ("Mini Latency", w_lat),
    ]

    # Build header line
    header_line = " | ".join(h.ljust(w) for h, w in headers)
    sep_line = "-+-".join("".ljust(w, "-") for _, w in headers)

    lines = [header_line, sep_line]

    for r in results:
        p = trunc(r.get("prompt", ""), w_prompt)
        gresp = trunc(r.get("gpt4o_response", ""), w_resp)
        mresp = trunc(r.get("mini_response", ""), w_mini)
        glat = r.get("gpt4o_latency", "")
        mlat = r.get("mini_latency", "")

        try:
            glat_s = f"{float(glat):.3f}s"
        except Exception:
            glat_s = str(glat)
        try:
            mlat_s = f"{float(mlat):.3f}s"
        except Exception:
            mlat_s = str(mlat)

        row = " | ".join([
            p.ljust(w_prompt),
            gresp.ljust(w_resp),
            mresp.ljust(w_mini),
            glat_s.rjust(w_lat),
            mlat_s.rjust(w_lat),
        ])
        lines.append(row)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()
