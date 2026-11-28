# LangChain: Chat with Your Data — Q&A

Fast-reference notes for Harrison Chase's *LangChain: Chat with Your Data* (DeepLearning.AI).
**Document loading → Document splitting → Vector stores and embeddings → Retrieval → Question answering → Chat.**

---

## Part 1 — Introduction

### Retrieval augmented generation

**Q: Why can't a trained LLM answer from your own files?**
A: It answers from its training data. Private documents, and anything published after the cutoff, stay unknown until that text is placed in the prompt.

**Q: What is retrieval augmented generation (RAG)?**
A: An application that **retrieves** passages from an external dataset and sends them to the LLM with the question, so the reply is grounded in those passages. The pipeline is (1) **load** sources into documents, (2) **split** them into chunks, (3) **embed** and store the vectors, (4) **retrieve** the chunks closest to the question, (5) **generate** an answer. A chatbot adds memory and rewrites follow-ups before step 4.

**Q: What does LangChain add beyond one model call?**
A: One interface each for loaders, splitters, embeddings, vector stores, retrievers, and chains, so changing the source or the store leaves the rest of the pipeline in place. The course cites more than 80 loaders and more than 30 vector stores.

---

## Part 2 — Document loading

### The Document

**Q: What does a document loader return?**
A: A list of **Document** objects, each with `page_content` (the text) and `metadata` (a dict, usually source path and page). Loaders turn websites, databases, PDFs, HTML, and JSON into that same object. Public unstructured sources (YouTube, Twitter, Hacker News), private ones (Notion, Figma), and tables that still hold text (Airbyte, Stripe, Airtable) all end in `load()`.

### Loaders

**Q: How do you load a PDF, a URL, or a Notion export?**
A: `PyPDFLoader(path).load()` (`pypdf`) returns one Document per page, with metadata `source` and 0-based `page`. `WebBaseLoader(url).load()` fetches a page; long runs of whitespace in `page_content` should be cleaned before splitting. For Notion, export Markdown and CSV, unzip, and pass the folder to `NotionDirectoryLoader(directory).load()`.

**Q: How do you turn audio or a YouTube video into documents?**
A: `GenericLoader` pairs a blob loader with a parser. `YoutubeAudioLoader(urls, save_dir)` downloads the audio (`yt_dlp`, `pydub`); `OpenAIWhisperParser()` transcribes it with Whisper. `loader.load()` returns the transcript. Audio already on disk uses `FileSystemBlobLoader` in that same pair.

---

## Part 3 — Document splitting

### Chunk size and overlap

**Q: Why does the way you split change the answer?**
A: Retrieval returns a chunk, so a fact cut in half is whole in neither chunk. Split after loading and before the vector store, on boundaries that keep one idea together. `chunk_size` is the target length (`length_function`, default `len`) and `chunk_overlap` repeats text at each edge. On real files the course uses overlap `150` with `chunk_size` `1500` for the index and `1000` for the chatbot.

**Q: How do `split_documents` and `create_documents` differ?**
A: `split_documents` splits Documents and copies parent metadata onto every chunk. `create_documents` runs the same split on raw strings and returns Documents.

### Splitter types

**Q: How does `CharacterTextSplitter` decide where to cut?**
A: It splits on one `separator`. The default is a newline (`"\n\n"`). Pieces stay near `chunk_size` when that separator occurs often enough; if it never occurs, the string stays one chunk even past `chunk_size`. `separator=" "` breaks on spaces and can land mid-sentence.

**Q: How does `RecursiveCharacterTextSplitter` split, and when should you use it?**
A: It is the recommended splitter for generic text. It tries separators in order — default `["\n\n", "\n", " ", ""]` — and uses the next only while a piece is still too long; `""` splits character by character last, so a paragraph break wins over a mid-sentence cut. Split on sentences with the lookbehind `"(?<=\. )"`, because a plain `"\. "` leaves the periods on the wrong side.

**Q: When should you split by tokens, or by document structure?**
A: `TokenTextSplitter(chunk_size, chunk_overlap)` counts **tokens** (about four characters each), which is how a context window is measured. `MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")])` cuts on headings and stores the heading path in metadata. A language-aware splitter uses per-language separators (Python, Ruby, C), and some splitters call a small model to find sentence ends.

---

## Part 4 — Vector stores and embeddings

### Embeddings and Chroma

**Q: What is an embedding?**
A: A numeric vector for a piece of text, so similar meanings sit near each other. Compare two vectors with a **dot product**; higher means more similar. `OpenAIEmbeddings()` embeds both chunks and questions, and the query must use the same model as the index.

**Q: What is a vector store, and why does the course use Chroma?**
A: A database of those vectors plus the chunks and metadata: embed the question and take the nearest chunks. **Chroma** (`chromadb`) is lightweight and in memory. Hosted stores hold a large index or cloud data.

**Q: How do you build, save, reload, and search a Chroma index?**
A: `Chroma.from_documents(documents=splits, embedding=embedding, persist_directory=directory)` builds it, `vectordb.persist()` writes it, and `Chroma(persist_directory=directory, embedding_function=embedding)` reloads it. `similarity_search(question, k=n)` returns the `k` nearest Documents; a larger `k` adds less relevant tail hits.

### Failure modes

**Q: Where does plain similarity search fall short?**
A: It covers the common case (about 80% of questions) and still fails in two ways. It has no **diversity** term, so duplicate chunks — the same file indexed twice — crowd out a second passage. It has no **specificity** term: naming one file in the question still returns other files, because one embedding of the whole question tracks the topic and misses the metadata constraint.

---

## Part 5 — Retrieval

### Maximum marginal relevance

**Q: What is a retriever?**
A: The object that, at query time, returns the splits to pass onward. `vectordb.as_retriever()` wraps the store; `get_relevant_documents(question)` runs it. `search_type` is `"similarity"` or `"mmr"`. `search_kwargs` such as `{"k": 4}` sets how many chunks return.

**Q: What is maximum marginal relevance (MMR)?**
A: A search that keeps hits relevant and different from each other. `max_marginal_relevance_search(question, k, fetch_k)` (1) queries the store, (2) takes the `fetch_k` nearest chunks by similarity, (3) returns `k` of them that add new information. The retriever form is `as_retriever(search_type="mmr")`.

### Metadata, self-query, and compression

**Q: How do you limit retrieval to one source by hand?**
A: Pass a metadata `filter`, for example `similarity_search(question, k=3, filter={"source": path})`. Only matching chunks are eligible. `source` and `page` are the fields the PDF loader wrote.

**Q: What is a self-query retriever?**
A: An LLM splits the question into a **query string** and a **metadata filter** (a topic plus a constraint such as year or file). Describe the corpus with `document_content_description` and each field with `AttributeInfo(name, description, type)`; the model reads those strings, so name the allowed values. `SelfQueryRetriever.from_llm(..., verbose=True)` runs `get_relevant_documents` and prints the inferred query and filter. The store must already support filters. The course uses `OpenAI` at `temperature=0`, and `lark` parses the query.

**Q: What is contextual compression, and what does it cost?**
A: After retrieval, an LLM keeps only the sentences that bear on the question. `LLMChainExtractor.from_llm(llm)` extracts; `ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)` retrieves, then extracts. Extra model calls are the cost. Pair it with MMR (`search_type="mmr"`), or the short hits can still be near-duplicates.

**Q: Which retrievers skip the vector store?**
A: `SVMRetriever.from_texts(splits, embedding)` ranks with an SVM over embeddings. `TFIDFRetriever.from_texts(splits)` ranks by TF-IDF overlap and takes no embedding model. Both implement `get_relevant_documents`.

---

## Part 6 — Question answering

### RetrievalQA

**Q: How do you answer from the retrieved chunks?**
A: `RetrievalQA.from_chain_type(llm, retriever=vectordb.as_retriever())` sends the chunks, a system prompt, and the question to the model in one shot. The course uses `ChatOpenAI` (`gpt-3.5-turbo`) at `temperature=0`. Invoke with `{"query": question}` and read `result["result"]`. With no stored history, a follow-up such as "why are those needed?" is searched as written and answers a different topic.

**Q: How do you fix the answer format and keep the evidence?**
A: Pass a `PromptTemplate` with `{context}` and `{question}` via `chain_type_kwargs={"prompt": prompt}`. Tell the model to use the context, to say it does not know when the context is silent, to stay within three sentences, and to end with a phrase you specify. `return_source_documents=True` puts the chunks at `result["source_documents"]`.

### Chain types

**Q: What do `stuff`, `map_reduce`, `refine`, and `map_rerank` change?**
A: `stuff` (the default) puts every chunk in one prompt: one call, and it fails past the context window. `map_reduce` answers per chunk, then merges, so it scales; it is slower and misses a fact that exists only across two chunks. `refine` answers from the first chunk, then updates that answer with each next chunk ("only if needed"), carrying information across chunks in sequential calls. `map_rerank` scores each chunk's answer and returns the highest score. Set `LANGCHAIN_TRACING_V2=true` plus `LANGCHAIN_ENDPOINT` and `LANGCHAIN_API_KEY` to inspect each child call.

---

## Part 7 — Chat

### Memory and conversational retrieval

**Q: What does `ConversationalRetrievalChain` add for follow-up questions?**
A: It condenses chat history plus the new question into a **standalone question**, searches that question, and asks it in the answer prompt. The vector store has no memory, so a bare follow-up matches the wrong chunks. `ConversationBufferMemory(memory_key="chat_history", return_messages=True)` stores turns as messages under `chat_history`. Build with `ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)`, call `qa({"question": question})`, and read `result["answer"]`.

**Q: How do you keep memory outside the chain, and what else can you swap?**
A: Pass `chat_history` as a list of `(question, answer)` pairs and append the new pair after the reply. `return_source_documents=True` adds the chunks; `return_generated_question=True` exposes the standalone question at `result["generated_question"]`. You can replace the condense prompt, use another memory class, and pass an MMR, self-query, or compression retriever. The pieces stay independent.

**Q: How is the end-to-end chatbot assembled?**
A: (1) `PyPDFLoader` loads the file. (2) `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)` splits it. (3) `OpenAIEmbeddings` embeds the chunks into `DocArrayInMemorySearch`. (4) `as_retriever(search_type="similarity", search_kwargs={"k": k})` returns the top `k`. (5) `ConversationalRetrievalChain.from_llm` answers; `chain_type` selects stuff, map-reduce, or refine. The caller holds `chat_history`.

---

## Part 8 — Conclusion

### Choosing the chain

**Q: When should you use a one-pass chain, and when a conversational one?**
A: Use `RetrievalQA` for a single question: retrieve, then generate. Use `ConversationalRetrievalChain` when the next question depends on earlier turns: condense, retrieve, then generate. Add MMR, a metadata filter, self-query, or compression when similarity search returns duplicates or the wrong source.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| RAG | Retrieve external passages and generate an answer from them |
| Document | `page_content` plus `metadata`; the unit every loader returns |
| `PyPDFLoader` | One Document per PDF page; metadata `source` and 0-based `page` |
| `WebBaseLoader` | Loads a URL; clean long whitespace before splitting |
| `NotionDirectoryLoader` | Loads a Markdown/CSV Notion export from a folder |
| `GenericLoader` | Pairs a blob loader with a parser, such as audio plus Whisper |
| `YoutubeAudioLoader` | Downloads YouTube audio into a directory |
| `OpenAIWhisperParser` | Transcribes audio with Whisper |
| `chunk_size` | Target length, via `length_function` (default `len`) |
| `chunk_overlap` | Text repeated at boundaries so a cut sentence survives |
| `CharacterTextSplitter` | One separator, default `"\n\n"`; no match leaves one chunk |
| `RecursiveCharacterTextSplitter` | Tries `["\n\n", "\n", " ", ""]` in order; default for generic text |
| `TokenTextSplitter` | Splits on token count to fit a context window |
| `MarkdownHeaderTextSplitter` | Splits on headings and stores the heading path in metadata |
| Embedding | Vector of meaning; higher dot product means closer text |
| `OpenAIEmbeddings` | Embedding model for both chunks and queries |
| Vector store | Vectors plus chunks and metadata, searched by nearest neighbor |
| Chroma | Local store; `from_documents`, `persist`, reload by directory |
| `similarity_search` | `k` nearest Documents; the tail is less relevant |
| Retriever | Query in, documents out; `as_retriever()` then `get_relevant_documents` |
| MMR | From `fetch_k` nearest chunks, return `k` relevant and diverse ones |
| Metadata filter | Keeps chunks whose metadata matches, such as `source` |
| `SelfQueryRetriever` | LLM writes the vector query and the metadata filter |
| `AttributeInfo` | Name, description, and type of one metadata field; the LLM reads it |
| Contextual compression | Keeps query-relevant sentences; costs extra model calls |
| `LLMChainExtractor` | Compressor inside `ContextualCompressionRetriever` |
| `SVMRetriever` | Ranks splits with an SVM over embeddings |
| `TFIDFRetriever` | Ranks splits by TF-IDF, with no embedding call |
| `RetrievalQA` | One-pass retrieve-then-answer; input `query`, output `result` |
| Stuff | Default; all chunks go into one prompt |
| Map-reduce | Answer per chunk, then merge; misses facts split across chunks |
| Refine | Updates one running answer with each next chunk |
| Map-rerank | Scores each chunk's answer and keeps the highest |
| `ConversationBufferMemory` | Full history under `chat_history` with `return_messages=True` |
| `ConversationalRetrievalChain` | Condenses a follow-up, retrieves, answers; input `question` |
| Standalone question | History plus follow-up; the search query and the asked question |
| `DocArrayInMemorySearch` | In-memory store used to assemble the chatbot |

---

*Study aid; for authoritative content, refer to the official DeepLearning.AI course.*
