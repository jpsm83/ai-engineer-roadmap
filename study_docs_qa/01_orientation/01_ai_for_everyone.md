# AI for Everyone — Q&A

### Machine Learning

**Q: What is machine learning?**
A: A computer learns from data (examples) to perform a task instead of being programmed with explicit rules. Given labeled input → output examples, it learns to produce the right output for new inputs.

**Q: What is supervised learning?**
A: The most common kind of ML: learning an input → output mapping from labeled examples.

**Q: What kinds of input → output mappings can ML learn?**
A: Email → spam/not spam; audio → transcript; one language → another; ad and user → click?; image or radar → nearby objects; image → defect?. Any task that can be framed as A → B with enough examples.

**Q: Why does data quality matter so much?**
A: ML needs examples to learn from; more and better data usually improves performance. A small, clean dataset is often more valuable than a large, noisy one.

**Q: What is a neural network?**
A: A flexible ML model loosely inspired by the brain, made of layers of interconnected units. It excels at speech, image, and language. **Deep learning** means neural networks with many layers.

**Q: What kinds of data can ML use?**
A: **Structured** data (tables, numbers) and **unstructured** data (images, audio, text). Neural networks are especially strong on unstructured data.

**Q: How do AI, machine learning, and deep learning relate?**
A: ML is a subset of AI. AI is the broad goal of building intelligent machines; ML is today's main technique. Deep learning is a subset of ML.

**Q: How does an ML system go from data to a prediction?**
A: Collect labeled A and B, train a model that learns the mapping, then use it to predict B for new A inputs.

**Q: What is narrow AI vs. AGI?**
A: **Narrow AI** (all AI today) does one task well. **Artificial general intelligence (AGI)** would match humans across many tasks and does not exist yet; media often overhype AI as AGI.

### Data science

**Q: What is data science?**
A: Extracting actionable insights from data to inform decisions. ML outputs predictions; data science outputs insights and recommendations for humans.

**Q: How does data science differ from machine learning?**
A: ML learns an A → B mapping to predict or automate. Data science analyzes data to produce reports and dashboards that help people decide. ML output can run automatically; DS output informs humans.

**Q: What is a typical data science workflow?**
A: (1) Collect data, (2) analyze and explore, (3) derive insights, (4) present findings and recommendations, (5) drive action.

**Q: Why is data science valuable?**
A: It turns raw data into decisions — improving products, targeting, operations, and strategy.

### Terminology and myths

**Q: What are common myths about AI?**
A: That AI will soon replace all jobs, that it is a magic box that does anything, and that AI equals AGI. In reality AI is powerful but narrow, and its impact depends on thoughtful application.

**Q: What can AI not do well today?**
A: Tasks that need deep common sense, general reasoning across domains, creativity grounded in real understanding, or little or no data. It is narrow, not universal.

**Q: How do you tell whether AI can do a task?**
A: Check whether it can be framed as an input → output mapping and whether enough data exists. Rule of thumb: if a typical person can do it with a second of thought, AI can probably do it — given data.

### ML project workflow

**Q: What is the typical ML project workflow?**
A: (1) Collect data, (2) build and train a model, (3) deploy it, (4) monitor and maintain. The steps repeat as you improve the system.

**Q: What happens inside model building?**
A: Choose model and data, train on training data, evaluate on a held-out test set, and tune to reduce error before deployment.

**Q: Why split data into train and test sets?**
A: Train on one portion and evaluate on a separate, unseen portion to check **generalization** rather than memorization.

**Q: What is a benchmark or test set?**
A: A fixed set of examples used to measure accuracy or error. Using the same benchmark lets you judge whether a change improved the model.

**Q: Why is deployment its own step?**
A: A model creates value only when it runs in production for real users. Deployment involves integration, latency, reliability, and monitoring.

**Q: Why monitor a deployed model?**
A: Real-world data changes (**data drift**), so performance can degrade. Systems need monitoring, retraining, and updates.

### Data science projects

**Q: What is the typical data science project workflow?**
A: (1) Collect data, (2) analyze and explore, (3) iterate on analyses or models, (4) present findings and recommendations, (5) take action.

**Q: What makes a data science project successful?**
A: A clear business question, good data, sound analysis, clear communication, and follow-through that turns insights into action.

### Teams and tools

**Q: What roles does an AI team need?**
A: ML engineers (models), data scientists (analysis and insight), data engineers (pipelines and infrastructure), software engineers (integration and deployment), and product or project managers (goals and coordination).

**Q: What should a non-technical manager know about AI?**
A: Enough to set realistic goals, ask good questions, judge feasibility and data readiness, manage timelines, and avoid overpromising.

**Q: When should a team build vs. buy AI?**
A: Building gives control and differentiation but is slower and costlier. Buying vendor tools or APIs is faster and cheaper but less customizable. Many teams buy first and build where it matters.

**Q: How do you judge whether an AI project is feasible?**
A: The task is a clear input → output mapping, enough labeled data exists or can be collected, and the expected accuracy is acceptable for the business.

**Q: What should you check before starting a project?**
A: Define the business goal and success metric, confirm data availability and quality, estimate effort and cost, check technical feasibility, and plan evaluation and deployment.

### Strategy and case selection

**Q: How should a company choose AI projects?**
A: Look for high-value, feasible use cases with available data and clear success metrics. Start with pilots, measure results, and scale what works.

**Q: What is the AI transformation playbook?**
A: (1) Run pilot projects for momentum, (2) build an in-house AI team, (3) provide broad AI training, (4) develop an AI strategy, (5) handle internal and external communications.

**Q: Why start with pilots?**
A: Pilots prove value, surface issues, and create buy-in before a large investment.

**Q: Why is broad AI training important?**
A: Leaders need to know what AI can do, managers need to spot use cases, and engineers need to build and integrate. Training across levels makes adoption work.

**Q: What should an AI strategy include?**
A: Where AI creates strategic value, build vs. buy choices, data and infrastructure, talent and training, governance and risk, and measurable goals.

**Q: How does AI transformation differ from digital transformation?**
A: Digital transformation modernizes processes and data infrastructure; AI transformation makes those processes smarter and more automated. AI often depends on good digital foundations.

**Q: Why is data infrastructure critical?**
A: AI needs accessible, high-quality, well-organized data. Inconsistent or siloed data is one of the biggest barriers.

### Roles and decision-making

**Q: How does AI change the work of leaders, managers, and engineers?**
A: Leaders set strategy and prioritize; managers identify use cases, define metrics, and run projects; engineers build and deploy. Everyone benefits from AI literacy.

**Q: What are common AI adoption pitfalls?**
A: Vague goals, low-value use cases, poor data quality, underestimating change management, skipping evaluation, and expecting AI to solve everything.

**Q: How do you measure whether an AI project succeeded?**
A: Concrete business metrics — revenue, cost, time saved, error reduction, customer satisfaction — tied to the original goal.

**Q: Why does change management matter?**
A: People must trust and adopt the systems. Training, communication, and involving users early increase adoption and reduce resistance.

**Q: How should a company grow its AI team?**
A: Start with a small team or vendor support for pilots, build internal capability through training and hiring, then scale as AI becomes core to the business.

### Benefits and risks

**Q: What are AI's main benefits?**
A: Productivity, better healthcare and science, safer transportation, more personalized education, and new economic opportunities.

**Q: What are AI's main risks?**
A: Bias and unfairness, job displacement, privacy and surveillance, misinformation, concentration of power, security risks, and misuse.

**Q: What is bias in AI, and where does it come from?**
A: AI learns from historical data that contains human biases; biased data produces biased predictions in areas such as hiring and lending.

**Q: How can bias be reduced?**
A: Use representative, balanced data; audit for disparate impact; involve diverse teams; apply human oversight and fairness testing.

**Q: How does AI affect jobs?**
A: It automates some tasks and augments others, shifting demand toward judgment, oversight, and collaboration with AI, and creating new roles. It is not simply "all jobs disappear."

**Q: What is the difference between augmentation and automation?**
A: **Augmentation** helps people work better or faster; **automation** performs tasks in place of people. AI often augments work while automating narrower tasks.

**Q: What privacy issues does AI raise?**
A: AI often needs large amounts of data, including personal information. Concerns include consent, surveillance, misuse, and breaches; strong governance is essential.

**Q: What is adversarial or malicious use of AI?**
A: Deepfakes, misinformation, fraud, and cyberattacks. Defenses include detection tools, policy, and public awareness.

**Q: What is responsible AI?**
A: Building and deploying AI that is fair, safe, transparent, accountable, privacy-respecting, and aligned with human values.

**Q: How can society manage AI risks?**
A: Education, regulation and policy, industry standards, transparency, human oversight for high-stakes decisions, and research on safety and fairness.

**Q: How should individuals prepare for AI at work?**
A: Learn AI fundamentals, understand strengths and limits, develop complementary skills (judgment, communication, creativity), and stay adaptive.

**Q: What is government's role in AI?**
A: Set rules for safety, privacy, fairness, and accountability; protect consumers; encourage beneficial innovation while managing risk.

**Q: How can companies build AI responsibly?**
A: Establish governance, test for bias and safety, ensure transparency and human oversight, protect data privacy, and consider broader societal impact.

---

## Quick Reference

| Term | Meaning |
| --- | --- |
| AI | Broad field of building machines that perform intelligent tasks |
| ML | Learning input → output mappings from data |
| Supervised learning | Learning from labeled A → B examples |
| Neural network | Flexible model with layers of interconnected units |
| Deep learning | Neural networks with many layers |
| Data science | Extracting actionable insights to inform decisions |
| Narrow AI | AI that performs a specific task (all AI today) |
| AGI | Human-level ability across tasks (does not exist yet) |
| Train/test split | Data split to train a model and evaluate generalization |
| Deployment | Running a model in production |
| Data drift | Real-world data changing over time, degrading performance |
| Pilot project | Small initial project to prove value before scaling |
| AI transformation playbook | Pilots → team → training → strategy → communications |
| Bias | Unfair behavior learned from biased data |
| Augmentation | AI helping people do work better or faster |
| Automation | AI performing tasks in place of people |
| Responsible AI | Fair, safe, transparent, accountable AI |

---
