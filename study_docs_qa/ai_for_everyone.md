# AI for Everyone — Questions & Answers

Study notes based on Andrew Ng's *AI for Everyone* course (DeepLearning.AI).
Organized by the course's four main topics: **What is AI**, **Building AI Projects**, **Building AI in Your Company**, and **AI and Society**.

---

## Week 1 — What is AI?

### Machine Learning

**Q: What is machine learning (ML)?**
A: ML is the field of AI where a computer learns from data (examples) to perform a task, rather than being explicitly programmed with rules. Given enough labeled examples (A → B mappings), the system learns to produce the right output for new inputs.

**Q: What is the most common type of ML taught in this course?**
A: Supervised learning — learning an A → B, or input → output, mapping from labeled examples. Examples: email → spam or not spam; audio → transcript; ad → will the user click?

**Q: What kinds of A → B mappings are common?**
A: Spam filtering (email → spam/not spam), speech recognition (audio → text), machine translation (English → Spanish), online advertising (ad/user → click?), self-driving (image/radar → other cars' positions), and visual inspection (image → defect?).

**Q: Why is data so important in ML?**
A: ML needs examples to learn from. More and better-quality data usually improves performance. A key rule of thumb: a small, clean dataset is often more valuable than a large, noisy one.

**Q: What is a neural network?**
A: A powerful, flexible ML model loosely inspired by the brain, made of layers of interconnected units. Neural networks excel at complex tasks like speech, image, and language processing. "Deep learning" refers to neural networks with many layers.

**Q: What kinds of data can ML use?**
A: Structured data (tables, numbers) and unstructured data (images, audio, text). Neural networks are especially strong with unstructured data.

**Q: What is the difference between AI and ML?**
A: ML is a subset of AI. AI is the broad goal of building intelligent machines; ML is the main technique used today to achieve it. Deep learning is a subset of ML.

**Q: What is the "data → model → output" idea?**
A: You collect labeled data (A and B), train a model that learns the mapping, then use the model to predict B for new A inputs.

**Q: What is a "narrow AI" vs. "general AI" (AGI)?**
A: Narrow AI (all AI today) does a specific task well — spam filtering, driving, translation. Artificial General Intelligence (AGI) would match humans across many tasks; it does not exist yet. Media often overhype AI as AGI.

### Data Science

**Q: What is data science (DS)?**
A: The practice of extracting actionable insights from data to inform decisions. Whereas ML outputs predictions, data science outputs insights and recommendations for humans.

**Q: How does data science differ from machine learning?**
A: ML learns an A → B mapping to make predictions/automate decisions. Data science analyzes data to produce insights (e.g., a report or dashboard) that help people make decisions. ML output runs automatically; DS output informs humans.

**Q: What is a typical data science workflow?**
A: (1) Collect data, (2) analyze/explore it, (3) derive insights, (4) present findings and recommendations to decision-makers, (5) use those insights to drive action.

**Q: What is a "data science project" example?**
A: Analyzing sales data to discover that a certain customer segment buys more, then recommending a marketing campaign to target that segment.

**Q: Why is data science valuable to companies?**
A: It turns raw data into decisions — improving products, targeting, operations, and strategy.

### AI Terminology and Myths

**Q: What is the difference between ML and DS in one line?**
A: ML automates predictions; DS informs human decisions.

**Q: What are common myths about AI?**
A: That AI will soon replace all jobs, that AI is a magic box that does anything, and that AI equals AGI. In reality, AI is powerful but narrow, and its impact depends on thoughtful application.

**Q: What can AI NOT do well today?**
A: It struggles with tasks needing deep common sense, general reasoning across domains, creativity grounded in real understanding, and tasks with little or no data. It also cannot do everything — it is narrow.

**Q: What determines whether AI can do a task?**
A: Whether the task can be framed as a simple input → output mapping and whether there is sufficient data to learn it. "If a typical person can do it with a second of thought, AI can probably do it" (with data).

---

## Week 2 — Building AI Projects

### The ML Project Workflow

**Q: What is the typical workflow for an ML project?**
A: (1) Collect data, (2) build/train a model, (3) deploy the model, (4) monitor and maintain it. These steps often repeat as you improve the system.

**Q: What are the steps within model building?**
A: Choosing the model and data, training on training data, evaluating on a held-out test set, and tuning to improve error rates before deployment.

**Q: What is the train / test split and why is it needed?**
A: You train on one portion of the data and evaluate on a separate, unseen portion (test set). This checks whether the model generalizes to new data rather than memorizing the training examples.

**Q: What is a "benchmark" or test set for evaluation?**
A: A fixed set of examples used to measure accuracy or error rate. Comparing results on the same benchmark lets you judge whether a change improved the model.

**Q: Why is deployment its own important step?**
A: A model only creates value when it is running in production and used by real users/systems. Deployment involves integration, latency, reliability, and monitoring.

**Q: Why does an ML system need ongoing monitoring and maintenance?**
A: Real-world data changes (data drift), so performance can degrade over time. Systems need monitoring, retraining, and updates.

### Data Science Project Workflow

**Q: What is the typical workflow for a data science project?**
A: (1) Collect data, (2) analyze/explore data, (3) build and iterate on analyses/models, (4) present findings and recommendations, and (5) take action based on the insights.

**Q: What makes a data science project successful?**
A: A clear business question, good data, sound analysis, clear communication of findings, and follow-through that turns insights into action.

### Working with AI Teams and External Tools

**Q: What are the key roles on an AI team?**
A: ML engineers (build models), data scientists (analyze data and insight), data engineers (data pipelines and infrastructure), software engineers (integrate and deploy), and product/project managers (define goals and coordinate).

**Q: What should a non-technical manager know about AI projects?**
A: Enough to set realistic goals, ask good questions, judge feasibility and data readiness, manage timelines, and avoid overpromising.

**Q: What is "build vs. buy" for AI projects?**
A: Building gives you control and differentiation but is slower and costlier. Buying (using vendor tools or APIs) is faster and cheaper but less customizable. Many teams start by buying and build where it matters.

**Q: How do you decide whether a project is feasible?**
A: Check that the task is a clear input → output mapping, that sufficient labeled data exists (or can be collected), and that the potential accuracy/error rate is acceptable for the business.

**Q: What is the "diligence" before starting an AI project?**
A: Define the business goal and success metric, confirm data availability and quality, estimate effort and cost, check technical feasibility, and plan for evaluation and deployment.

---

## Week 3 — Building AI in Your Company

### AI Strategy and Case Selection

**Q: How should a company choose AI projects?**
A: Look for high-value, feasible use cases with available data and clear success metrics. Start with pilots, measure results, and scale what works.

**Q: What is the "AI transformation playbook"?**
A: (1) Execute pilot projects to gain momentum, (2) build an in-house AI team, (3) provide broad AI training, (4) develop an AI strategy, and (5) develop internal/external communications.

**Q: Why start with pilots?**
A: Pilots build momentum, prove value, surface issues, and create internal buy-in before large-scale investment.

**Q: What are the main roles a company needs for AI?**
A: Leadership sponsorship, an AI team (ML engineers, data scientists, data engineers), and business units that own the use cases. Many companies also use outside vendors early on.

**Q: Why is broad AI training important?**
A: Leaders need to know what AI can do, managers need to identify use cases, and engineers need to build and integrate systems. Training across levels makes AI adoption work.

**Q: What should an AI strategy include?**
A: Where AI creates strategic value, which capabilities to build vs. buy, data and infrastructure, talent and training, governance and risk, and measurable goals.

**Q: What is the difference between AI and digital transformation?**
A: Digital transformation modernizes processes and data infrastructure; AI transformation uses AI to make those processes smarter and more automated. AI often depends on good digital foundations.

**Q: Why is data infrastructure critical?**
A: AI needs accessible, high-quality, well-organized data. Inconsistent or siloed data is one of the biggest barriers to successful AI projects.

### AI and Company Roles / Decision-Making

**Q: How does AI affect the roles of leaders, managers, and engineers?**
A: Leaders set strategy and prioritize; managers identify use cases, define metrics, and manage projects; engineers build and deploy. Everyone benefits from AI literacy.

**Q: What are common pitfalls in company AI adoption?**
A: Vague goals, low-value use cases, poor data quality, underestimating change management, skipping evaluation, and expecting AI to solve everything.

**Q: How do you measure AI project success?**
A: Use concrete business metrics — revenue, cost, time saved, error reduction, customer satisfaction — tied to the original goal.

**Q: Why is change management important?**
A: People must trust and adopt AI systems. Training, communication, and involving users early increase adoption and reduce resistance.

**Q: What is the "AI team building" progression?**
A: Start with a small team or vendor support for pilots, build internal capability through training and hiring, then scale the team as AI becomes core to the business.

---

## Week 4 — AI and Society

### Benefits and Risks

**Q: What are the main benefits of AI to society?**
A: Improved productivity, better healthcare and science, safer transportation, more personalized education, and new economic opportunities.

**Q: What are the main risks of AI?**
A: Bias and unfairness, job displacement, privacy and surveillance concerns, misinformation, concentration of power, security risks, and misuse.

**Q: What is bias in AI, and where does it come from?**
A: AI learns from historical data, which can contain human biases. If the data is biased, the model's predictions can be biased — for example, in hiring or lending.

**Q: How can bias be reduced?**
A: Use representative and balanced data, audit models for disparate impact, involve diverse teams, and apply human oversight and fairness testing.

**Q: How does AI affect jobs?**
A: It automates some tasks while augmenting others. It changes the nature of work, shifts demand toward judgment, oversight, and AI collaboration skills, and creates new roles. It is not simply "all jobs disappear."

**Q: What is "augmentation" vs. "automation"?**
A: Augmentation helps people do work better/faster; automation replaces tasks. AI often augments work while automating narrower tasks.

**Q: What are privacy concerns with AI?**
A: AI systems often need large amounts of data, which can include personal information. Concerns include consent, surveillance, data misuse, and security breaches. Strong data governance and privacy practices are essential.

**Q: What is "adversarial" or malicious use of AI?**
A: Using AI to create deepfakes, spread misinformation, conduct fraud, or power cyberattacks. Defenses include detection tools, policy, and public awareness.

**Q: What is "responsible AI"?**
A: Building and deploying AI that is fair, safe, transparent, accountable, privacy-respecting, and aligned with human values.

**Q: How can society manage AI risks?**
A: Education and awareness, regulation and policy, industry standards, transparency, human oversight for high-stakes decisions, and ongoing research on safety and fairness.

**Q: What should individuals do to prepare for an AI-powered world?**
A: Learn AI fundamentals, understand its strengths and limits, develop complementary skills (judgment, communication, creativity), and stay adaptive as tools evolve.

**Q: What is the role of government and regulation?**
A: To set rules for safety, privacy, fairness, and accountability, protect consumers, and encourage beneficial innovation while managing risks.

**Q: How can companies build AI responsibly?**
A: Establish governance, test for bias and safety, ensure transparency and human oversight, protect data privacy, and consider broader societal impact.

---

## Quick Reference — Key Terms

| Term | Meaning |
| --- | --- |
| Artificial Intelligence (AI) | Broad field of building machines that perform intelligent tasks |
| Machine Learning (ML) | Learning input → output mappings from examples/data |
| Supervised learning | Learning from labeled A → B examples |
| Neural network | Flexible ML model with layers of interconnected units |
| Deep learning | Neural networks with many layers |
| Data Science (DS) | Extracting actionable insights from data to inform decisions |
| Narrow AI | AI that performs a specific task (all AI today) |
| AGI | Artificial General Intelligence — human-level ability across tasks (does not exist yet) |
| Train/test split | Data split to train a model and evaluate generalization |
| Deployment | Running a model in production for real use |
| Data drift | Real-world data changing over time, degrading model performance |
| Pilot project | Small initial project to prove value before scaling |
| AI transformation playbook | Pilots → build team → train broadly → strategy → communications |
| Bias | Unfair model behavior learned from biased data |
| Augmentation | AI helping people do work better/faster |
| Automation | AI performing tasks in place of people |
| Responsible AI | AI that is fair, safe, transparent, and accountable |

---

*These notes are a study aid and paraphrase the themes of the course; for authoritative content, refer to the official DeepLearning.AI course.*
