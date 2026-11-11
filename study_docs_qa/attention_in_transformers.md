# Attention in Transformers: Concepts and Code in PyTorch — Q&A

Fast-reference notes for Josh Starmer's *Attention in Transformers* (DeepLearning.AI / StatQuest).
**Foundations → Self-Attention → Masked Self-Attention → Encoder-Decoder & Multi-Head → PyTorch.**

---

## Part 1 — Foundations

### Attention and Transformers

**Q: What is attention?**
A: For each token, compare its **query** against every token's **key**; softmax turns the similarities into weights that combine the **values**. Result: a context-aware embedding — the same word gets different numbers depending on its context.

**Q: Why was attention a breakthrough?**
A: RNNs compressed a whole sentence into one fixed vector and processed tokens sequentially. Attention connects every token to every other token directly, preserves per-token vectors, and parallelizes on GPUs.

**Q: What is the Transformer?**
A: The architecture from *"Attention Is All You Need"* (Vaswani et al., Google Brain, 2017). Three building blocks: **word embedding**, **positional encoding**, **attention**. Basis of modern LLMs.

**Q: Where did attention come from?**
A: Mid-2010s machine translation needed alignment across differing word orders/lengths. Bengio's (Montreal) and Manning's (Stanford) groups independently built encoder-decoder attention: the encoder produced one vector per word; the decoder weighted the relevant input vectors at each output step. The 2017 paper generalized this.

**Q: How do BERT and GPT relate?**
A: BERT uses the **encoder** (basis of embedding models for RAG/recommenders). GPT uses the **decoder** (basis of ChatGPT and most modern LLMs). The original used 6 attention layers; Llama 3.2-405B uses 126 — same architecture.

### Embeddings and Position

**Q: What is word embedding?**
A: A layer converting tokens (words, word parts, symbols) into numeric vectors, typically 512+ dimensions, because neural networks need numeric input.

**Q: Why train embeddings instead of assigning random numbers?**
A: Random numbers make similar words unrelated. Training on next-word prediction clusters words used in similar contexts (e.g., "great"/"awesome"); multiple numbers capture different senses (sincere vs. sarcastic "great"). The learned input-to-activation weights *are* the embeddings.

**Q: Why does context length matter, and what fixes word order?**
A: Predicting from one preceding word gives little context; using ~4 preceding words improves embeddings but still ignores order ("Squatch eats pizza" vs. "Pizza eats Squatch"). **Positional encoding** injects position information so order matters.

**Q: What is a context-aware (contextualized) embedding?**
A: The post-attention representation reflecting relationships with other tokens. Unlike word embeddings, these cluster similar sentences and documents; used for clustering, semantic search, and classifiers (neural nets or logistic regression).

---

## Part 2 — Self-Attention

**Q: What is self-attention?**
A: Attention where Q, K, and V all come from the same sequence. It computes similarity between every word and all others — including later words — then builds new representations. Example: in "The pizza came out of the oven and it tasted good," attention links "it" to "pizza".

**Q: Where do Query, Key, Value come from?**
A: Database search: **query** = search term; **keys** = records compared against it; **value** = returned result (e.g., room number).

**Q: What is the equation, step by step?**
A: `Attention(Q,K,V) = softmax(QKᵀ / √d_k) · V`
1. `X` = word embeddings + positional encoding (one row per token).
2. `Q = XW_q`, `K = XW_k`, `V = XW_v` using learned weights.
3. `QKᵀ` = dot product of every query with every key (all similarity scores).
4. Divide by `√d_k`.
5. Row-wise softmax → weights summing to 1.
6. Weights `· V` → weighted average of values = final score per token.

**Q: Why transpose K?**
A: Required for the matrix multiplication *and* — more importantly — it computes every query–key dot product.

**Q: What is a dot product?**
A: The sum of element-wise products. It is an unscaled similarity measure, closely related to cosine similarity (which scales to [-1, 1]).

**Q: Why divide by √d_k?**
A: Large dimensions produce large dot products, making softmax too sharp and hurting training. The authors reported better performance; simple √d_k scaling is not a systematic normalization.

**Q: What does the softmax do?**
A: Converts each row of scaled similarities into positive weights summing to 1 — the % influence each token has on a given token (e.g., "write" 36% self, 40% "a", 24% "poem").

**Q: Why multiply the weights by V?**
A: The weights say how much each token contributes; multiplying and summing gives a weighted average of values.

**Q: The equation in one line?**
A: Scaled dot-product similarities → softmax percentages → scale and combine the values.

---

## Part 3 — Masked Self-Attention

**Q: Self-attention vs. masked self-attention?**
A: Self-attention sees words before **and after** the current word. Masked self-attention ignores everything after it.

**Q: How does the math change?**
A: Only the mask matrix `M` is added: `softmax(QKᵀ/√d_k + M) · V`. Q, K, V are computed identically.

**Q: What is in the mask?**
A: `0` for allowed positions, `-∞` for hidden ones. Adding 0 changes nothing; `-∞` becomes 0% after softmax.

**Q: Why `-∞` instead of zero?**
A: Zeroing a score before softmax still leaves it with probability after normalization. `-∞` guarantees exactly 0%.

**Q: Mask for "Write a poem"?**
A: Lower-triangular: "write" → itself; "a" → "write", "a"; "poem" → all three.

**Q: How is the mask built in PyTorch?**
A: `mask = (torch.tril(torch.ones(n, n)) == 0)` gives a boolean upper-triangular mask; apply `scaled.masked_fill(mask, float('-inf'))` before softmax.

**Q: Encoder-only transformer?**
A: Uses only self-attention; produces context-aware embeddings for clustering, search, and classification. BERT is the example.

**Q: Decoder-only transformer?**
A: Uses only masked self-attention; trained to predict the next token; produces generative inputs for new tokens. GPT/ChatGPT are examples.

**Q: Why can decoder-only models generate?**
A: Training shows a prefix (e.g., up to "it") and updates weights until the continuation ("tasted good") is produced. Inference generates one token at a time, feeding each output back as context.

**Q: Why is masking essential for generation?**
A: Without it, the model would copy future tokens instead of learning to predict them. At generation time only the past exists.

---

## Part 4 — Encoder-Decoder and Multi-Head

**Q: What is encoder-decoder (cross) attention?**
A: **Q comes from the decoder; K and V come from the encoder.** The decoder asks which encoder outputs are relevant to what it is generating now.

**Q: Where do "encoder-only" / "decoder-only" names come from?**
A: The original sequence-to-sequence transformer had an encoder (self-attention) and a decoder (masked self-attention) linked by cross-attention. Models keeping one half are named accordingly.

**Q: What was the original transformer designed for?**
A: Machine translation (e.g., English → Spanish). The encoder embeds the source in one pass; the decoder generates the target token by token while attending to the encoder.

**Q: Is encoder-decoder attention still used?**
A: Yes — notably in **multimodal models**, where an image/audio encoder feeds context-aware embeddings into a text decoder for captions or audio responses.

**Q: How does the encoder/decoder each process data?**
A: Encoder: full input once with self-attention. Decoder: output-so-far with masked self-attention, then cross-attention to the encoder; each output is fed back as the next input.

**Q: What is multi-head attention?**
A: Multiple attention heads run in parallel, each with its own `W_q`, `W_k`, `W_v`. Outputs are concatenated and passed through a linear projection. The original paper used 8 heads.

**Q: Why multiple heads?**
A: One attention pattern cannot capture all relationships. Heads can specialize (syntax, coreference, nearby context), giving a richer representation.

**Q: 3 heads × 2 values — how return to 2?**
A: You get 6 values; a fully connected layer with 2 outputs projects them down. Alternatively, make each head output fewer values (e.g., a one-column `W_v`).

**Q: How is it coded?**
A: One attention module per head; loop in `forward`, collect outputs, `torch.cat`, then an output `nn.Linear`.

---

## Part 5 — PyTorch Implementation

**Q: Structure of the self-attention class?**
A: Subclass `nn.Module`; `__init__` creates `W_q`, `W_k`, `W_v` as `nn.Linear`; `forward` computes Q/K/V and applies the equation.

**Q: What is `d_model`?**
A: Number of embedding values per token; sets weight-matrix size (d_model=2 → 2×2 matrices; 512+ typical). Only constraint: matrix math must be dimensionally valid.

**Q: Why `bias=False`?**
A: The original Transformer adds no bias terms when computing attention.

**Q: What does `forward` do?**
A: `q = W_q(x)`, `k = W_k(x)`, `v = W_v(x)`; `similarities = q @ k.transpose(-2,-1)`; divide by `sqrt(d_k)`; softmax; return `attention_percents @ v`.

```python
import math, torch, torch.nn as nn, torch.nn.functional as F

class SelfAttention(nn.Module):
    def __init__(self, d_model):
        super().__init__()
        self.W_q = nn.Linear(d_model, d_model, bias=False)
        self.W_k = nn.Linear(d_model, d_model, bias=False)
        self.W_v = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x):
        q, k, v = self.W_q(x), self.W_k(x), self.W_v(x)
        sim = q @ k.transpose(-2, -1)
        scaled = sim / math.sqrt(k.shape[-1])
        weights = F.softmax(scaled, dim=-1)
        return weights @ v
```

**Q: Why the transpose symbol on the weights?**
A: PyTorch stores `nn.Linear` weights transposed relative to math notation; transpose `W_q.weight` to verify by hand.

**Q: How do you verify correctness?**
A: Print the weight matrices, compute Q/K/V manually (or call `W_q(x)`), and compare with the class output.

**Q: Why set a manual seed?**
A: Weights are randomly initialized; `torch.manual_seed(...)` makes results reproducible.

**Q: Are the weights trained?**
A: No — the lessons implement only an attention class, not a full transformer. The tensors are set up so backpropagation could train them later.

**Q: What changes for masked self-attention?**
A: Same Q/K/V; `forward` also takes a mask and calls `scaled.masked_fill(mask, float('-inf'))` before softmax.

```python
class MaskedSelfAttention(nn.Module):
    def __init__(self, d_model):
        super().__init__()
        self.W_q = nn.Linear(d_model, d_model, bias=False)
        self.W_k = nn.Linear(d_model, d_model, bias=False)
        self.W_v = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x, mask):
        q, k, v = self.W_q(x), self.W_k(x), self.W_v(x)
        scaled = (q @ k.transpose(-2, -1)) / math.sqrt(k.shape[-1])
        scaled = scaled.masked_fill(mask, float('-inf'))
        return F.softmax(scaled, dim=-1) @ v
```

**Q: One class for all three attention types?**
A: Either a mode switch or separate classes. The only differences: whether a mask is applied, and whether Q vs. K/V come from the same input (self) or different inputs (cross).

**Q: What happens with more heads?**
A: More attention values per token; the final linear projection restores the desired dimension.

**Q: Why use dimension 2 in the examples?**
A: So the math can be verified by hand. The same code generalizes to 512.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Transformer | 2017 architecture; basis of modern LLMs |
| Token | Word, word part, or symbol processed by the model |
| Word embedding | Learned numeric vector for a token |
| Positional encoding | Adds token-order information |
| Attention | Weighted combination of values via query-key similarity |
| Self-attention | Q, K, V from the same sequence |
| Masked self-attention | Cannot see future tokens |
| Cross-attention | Q from decoder; K/V from encoder |
| Query / Key / Value | Search vector / compared vectors / returned vectors |
| Dot product | Unscaled similarity (sum of element-wise products) |
| `d_model` / `d_k` | Embedding size per token / key dimension used in √d_k |
| Softmax | Scores → positive weights summing to 1 |
| Mask (M) | 0 = allowed, -∞ = hidden |
| Context-aware embedding | Representation reflecting surrounding context |
| Encoder-only | Self-attention; embeddings (BERT) |
| Decoder-only | Masked self-attention; generation (GPT) |
| Encoder-decoder | Self + masked + cross-attention (translation) |
| Multi-head | Parallel heads, concatenated and projected |
| `nn.Linear` | Holds weights and performs the matrix math |
| `bias=False` | No bias, as in the original paper |
| `torch.tril` / `masked_fill` | Build mask / set masked scores to -∞ |
| `torch.matmul` / `@` | Matrix multiplication |

---

## Formulas

- **Self:** `softmax(QKᵀ / √d_k) · V`
- **Masked:** `softmax(QKᵀ / √d_k + M) · V`
- **Cross:** `Q = X_decoder·W_q`, `K,V = X_encoder·W_k, X_encoder·W_v`
- **Multi-head:** `Concat(head₁ … headₕ) · W_o`

---

*Study aid; for authoritative content and notebooks, refer to the official DeepLearning.AI course.*
