# 100+ AI Concepts for Developers — Part 01 — Q&A

Fast-reference notes for Codist's *100+ AI Concepts for Developers Explained in 20 Minutes* (YouTube).
**Neural networks → Training and inference → Tokens → Embeddings → Attention → Transformers → Context window → Scaling laws → Pre-training and post-training → Large language models.**

---

## Part 1 — Neural Networks

### Pattern learning

**Q: How does a brain recognize a cat, and why did rules fail?**
A: It matches a **pattern** instantly instead of measuring ears or counting whiskers. Hand-written rules such as "fur, four legs, and pointy ears" also match a dog, so the real world is too messy to describe by hand; **neural networks** discover patterns from examples instead.

**Q: What is a neural network?**
A: A machine learning model made of layers of mathematical units called **neurons**. It is loosely inspired by the brain, but it is not a digital brain; it is a pattern-learning machine whose ingredients also power image recognition, fraud detection, language models, and transformers.

### Neurons and layers

**Q: What are the three stages, and what does one neuron compute?**
A: The **input layer** receives raw information such as pixels; **hidden layers** turn it into useful patterns; the **output layer** predicts, e.g., 95% likely a cat. Each **neuron** multiplies inputs by **weights** (volume knobs), adds a **bias** (threshold shift), and passes the result through an **activation function** that decides how strongly it moves forward.

**Q: Why stack many neurons, and who programs the detectors?**
A: One neuron can do almost nothing; thousands or millions across layers can. In an image network, early layers detect edges, later layers form shapes, deeper layers recognize eyes, ears, and whiskers, and the final layers combine those into "cat." Nobody programs the detectors: random starting weights learn from data and encode the discovered patterns.

---

## Part 2 — Training and Inference

**Q: What are a model's two modes?**
A: **Training** is learning; **inference** is answering. An untrained network is empty machinery until weights are learned. Studying is training; exam day is inference: a question arrives, no teacher corrects, and the student produces output.

**Q: How does training update a network?**
A: You show millions of examples, the model predicts, and a wrong prediction is penalized so weights update. Repeat this billions of times and the model improves after each correction, e.g., given "all that glitters," predict "is not gold."

**Q: What happens at inference?**
A: Learning is done. The model is shipped to a server, a user hits an API, and it answers instantly without updating weights, using what it knows to predict the next token. Companies train once, then serve that model to millions of users.

---

## Part 3 — Tokens

**Q: Does an LLM receive your prompt as one sentence?**
A: No: a **tokenizer** cuts the text into **tokens**. "the" may stay whole, while "unbelievable" might become `un`, `believe`, and `able`; unusual names and long terms often split, and spaces, punctuation, and even parts of emojis can be tokens. Chopping keeps a manageable vocabulary, the model never works with letters, and each token gets a barcode-like ID (`cat` might be `8241`, `kitten` `17903`) so the network can predict the next token from a sequence of numbers.

---

## Part 4 — Embeddings

**Q: Why are token IDs not enough, and what is an embedding?**
A: An ID such as `8241` does not say that cats and kittens are related. **Meaning** comes from an **embedding**, a **vector** that places a token on a high-dimensional map where similar ideas sit closer together: `cat` near `kitten` and `dog`, `airplane` far away, using hundreds or thousands of dimensions.

**Q: How do embeddings get their positions, and what can that buy you?**
A: Training adjusts vectors so tokens used in similar contexts develop related positions, and meaning is compared by measuring distance. A search for "repair a dripping tap" can then find "how to fix a leaky faucet" even though the wording differs. `king` minus `man` plus `woman` often lands near `queen`, and `Paris` minus `France` plus `Italy` can land near `Rome` — useful illustrations, not perfect laws, that geometry can represent relationships.

**Q: Why is a single fixed embedding not enough, and what do embeddings power?**
A: A traditional embedding gives a word one coordinate, so `bank` would occupy one point for both money and a river; modern models make representations **contextual**. Embeddings power semantic search, recommendation systems, **retrieval augmented generation (RAG)**, and **vector databases** that retrieve nearest matches, bridging IDs to usable meaning.

---

## Part 5 — Attention

**Q: What missing ingredient lets a model pick the intended meaning?**
A: **Context**. Every word needs a way to examine nearby words and decide which ones matter. A basic embedding gives each token a starting vector; **attention** uses surrounding tokens to build a context-aware representation.

**Q: How does self-attention disambiguate "mouse"?**
A: In "to open the file, I click the mouse," `open`, `file`, and `clicked` get high **attention scores** (volume controls), so `mouse` moves toward keyboard and computer rather than cheese and animal. In "The hungry cat chased the mouse," attention instead connects `mouse` with `cat` and `chased`: same token, different representation.

**Q: What are attention heads, and why stack layers?**
A: Several attention calculations run at once. Different **heads** can capture different relationships, such as an action or a pronoun and the noun it refers to. Stack many layers and the model builds a richer picture of the sentence.

**Q: Was attention invented in 2017, and why did the Transformer paper matter?**
A: No; it already existed for several years. Google's 2017 paper *Attention Is All You Need* introduced the **Transformer**, put **self-attention** at the center, and let the model examine many relationships at once, even between distant words, which made training faster and more scalable. ChatGPT, Claude, Gemini, and most modern language models descend from this design, but attention is only the mechanism and still needs a complete architecture.

---

## Part 6 — Transformers

**Q: Are an LLM and a transformer the same thing?**
A: No. An **LLM** is a trained model that processes and generates language; a **transformer** is the architecture — the blueprint for how information moves. The LLM is the finished car; the transformer is the engine design.

**Q: What happens to a prompt before transformer blocks run?**
A: The prompt is split into tokens, each becomes an embedding vector, and the model adds **positional information** so it knows order. Without position, "dog bites man" and "man bites dog" would be the same pieces.

**Q: What are the two main stages in a transformer block?**
A: **Self-attention**, then a **feed-forward** neural network: attention gathers useful context and the feed-forward network processes it at each position. During generation, every token measures how relevant earlier tokens are, which helps connect pronouns to nouns, resolve ambiguous words, and follow long-range relationships. **Residual connections** help preserve earlier information, and **normalization** keeps the calculation stable.

**Q: Do layers have fixed jobs, and how is a response produced?**
A: No. The attention then feed-forward pattern repeats, and deeper representations become more refined, from words and grammar toward relationships, tone, and instructions. After the final layer, the model scores every possible next token, selects one, adds it, and repeats: a transformer is a repeating architecture that turns token vectors into context-aware predictions.

---

## Part 7 — Context Window

**Q: What is the context window, and why does longer input get expensive so fast?**
A: The model's working desk: how much information it can actively consider at one time. Prompt, conversation history, reference material, and the model's own response must all fit. In standard self-attention, every token compares itself with every other allowed token, so 10 tokens can mean roughly 100 comparisons, 1,000 tokens around 1 million, and doubling length can grow the work about four times.

**Q: What happens when the desk is full, and does a larger window guarantee recall?**
A: The application must reject extra text, compact the context, or drop older tokens; once information leaves the active window, the model cannot directly use it. A larger window still does not guarantee perfect recall: important details can be buried, and extra tokens cost time and money.

**Q: Why is stuffing everything into the prompt a bad plan?**
A: A support assistant may need thousands of pages of policies, and a coding assistant may need a codebase larger than the window, so pasting everything is slow, expensive, and sometimes impossible. **Retrieval augmented generation (RAG)** retrieves only what the current question needs; more scale brings more capability and more cost.

---

## Part 8 — Scaling Laws

**Q: Besides cleverer algorithms, what lever improved AI?**
A: **Scale**: more **parameters**, more **data**, and more **computing power**, balanced together. **Neural scaling laws** say that if those three scale in the right balance, error falls predictably, so smaller models can estimate a larger one's performance before anyone spends millions training it. More GPU does not automatically create intelligence: data quality, architecture, and optimization still matter, a giant model on too little data can waste compute, and gains get more expensive as models grow.

**Q: What appeared as models got larger, and what did that trigger?**
A: Few-shot learning, coding, and more flexible language generation, without every behavior being programmed as a separate rule. Once those improvements could be forecast, investment in chips, data, and data centers exploded. A massive dataset still does not create a helpful assistant; that takes **pre-training** and **post-training**.

---

## Part 9 — Pre-training and Post-training

**Q: What happens in pre-training, and how does the next-token task create a signal?**
A: A transformer begins with random weights and trains on an enormous mixture of text and code, potentially trillions of tokens, to predict the next token. If it reads "The sky is," the real next token provides the correction; no one labels every example because the text creates its own signal. That is **self-supervised learning** at massive scale.

**Q: What is a base model?**
A: The result of pre-training. It learns language patterns, facts, reasoning strategies, and code, but it is optimized to continue text, not necessarily to follow instructions. Asked a question, it might answer correctly or continue the prompt unexpectedly.

**Q: What does post-training teach, and is a base model already an LLM?**
A: Following instructions, holding conversations, and producing safer, more useful responses, using **supervised fine-tuning**, **preference optimization**, and **reinforcement learning from human feedback (RLHF)**. Pre-training is a broad education; post-training is coaching that turns an already-LLM **base model** into the polished assistant you use.

---

## Part 10 — Large Language Models

**Q: What is an LLM, and how does it generate a response?**
A: A neural network trained on enormous amounts of text and code to learn language patterns. Most modern generative LLMs use the transformer architecture and predict the next token: score candidates, select one, append it, and repeat. That loop produces complex results because training encoded vast patterns into parameters.

**Q: What does "large" refer to, and is parameter count intelligence?**
A: **Parameters** are the learned numbers adjusted during training; GPT-3 had 175 billion. Parameter count alone is not intelligence: data quality, architecture, training methods, and compute also matter.

**Q: How is an LLM different from ChatGPT, Claude, or Gemini?**
A: An LLM is a model. ChatGPT, Claude, and Gemini are assistant **products** powered by language models, often combined with tools, safety systems, and a user interface.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| Neural network | Layered pattern-learning model of neurons; not a digital brain |
| Weight / bias / activation | Signal strength / threshold shift / how strongly a result moves forward |
| Training / inference | Update weights from examples / answer without updating weights |
| Token / tokenizer | Text piece after splitting / tool that splits text and assigns IDs |
| Embedding | Vector that places a token in meaning-space |
| Vector database | Store of embeddings that retrieves nearest matches |
| Attention / head | Scores which other tokens matter / one of several parallel calculations |
| Self-attention | Tokens attend to other tokens in the same sequence |
| Transformer | Architecture that stacks attention and feed-forward blocks |
| Positional information | Signal that preserves token order |
| Residual / normalization | Preserve earlier information / keep calculations stable |
| Context window | Maximum tokens the model can consider at once |
| Neural scaling laws | Predictable error drop as parameters, data, and compute scale |
| Pre-training / base model | Next-token training on huge unlabeled text / LLM optimized to continue text |
| Post-training | Instruction, conversation, and safety adaptation |
| Self-supervised learning | Training signal created by the text itself |
| RLHF | Reinforcement learning from human feedback |
| LLM | Neural network trained to model language, usually by next-token prediction |
| RAG | Retrieve only the information needed for the current question |
| Parameter | Learned number adjusted during training |

---

*Study aid; for authoritative content, refer to the official Codist video.*
