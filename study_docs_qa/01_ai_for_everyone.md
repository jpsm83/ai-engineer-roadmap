# AI for Everyone — Q&A

Fast-reference notes for Andrew Ng's *AI for Everyone* (DeepLearning.AI).
**What is AI → Building AI Projects → Building AI in Your Company → AI and Society.**

---

## Week 1 — What is AI?

### Machine Learning

**Q: What is machine learning (ML)?**
A: A computer learns from data (examples) to perform a task instead of being explicitly programmed with rules. Given labeled A → B examples, it learns to produce the right output for new inputs.

**Q: What is the most common type of ML in this course?**
A: **Supervised learning** — learning an input → output mapping from labeled examples.

**Q: What are common A → B mappings?**
A: Email → spam/not spam; audio → transcript; English → Spanish; ad/user → click?; image/radar → other cars' positions; image → defect?

**Q: Why is data so important?**
A: ML needs examples to learn from; more and better data usually improves performance. A small, clean dataset is often more valuable than a large, noisy one.

**Q: What is a neural network?**
A: A flexible ML model loosely inspired by the brain, made of layers of interconnected units. It excels at complex tasks like speech, image, and language. **Deep learning** = neural networks with many layers.

**Q: What kinds of data can ML use?**
A: Structured data (tables, numbers) and unstructured data (images, audio, text). Neural networks are especially strong with unstructured data.

**Q: AI vs. ML?**
A: ML is a subset of AI. AI is the broad goal of building intelligent machines; ML is today's main technique. Deep learning is a subset of ML.

**Q: What is the "data → model → output" idea?**
A: Collect labeled A and B, train a model that learns the mapping, then use it to predict B for new A inputs.

**Q: Narrow AI vs. AGI?**
A: Narrow AI (all AI today) does one task well. Artificial General Intelligence would match humans across many tasks and does not exist yet; media often overhype AI as AGI.

### Data Science

**Q: What is data science (DS)?**
A: Extracting actionable insights from data to inform decisions. ML outputs predictions; DS outputs insights and recommendations for humans.

**Q: How does DS differ from ML?**
A: ML learns an A → B mapping to make predictions/automate decisions. DS analyzes data to produce insights (reports, dashboards) that help people decide. ML output runs automatically; DS output informs humans.

**Q: What is a typical DS workflow?**
A: (1) Collect data, (2) analyze/explore, (3) derive insights, (4) present findings and recommendations, (5) drive action.

**Q: What is a DS project example?**
A: Analyzing sales data to find that a customer segment buys more, then recommending a campaign targeting it.

**Q: Why is DS valuable?**
A: It turns raw data into decisions — improving products, targeting, operations, and strategy.

### Terminology and Myths

**Q: ML vs. DS in one line?**
A: ML automates predictions; DS informs human decisions.

**Q: What are common AI myths?**
A: That AI will soon replace all jobs, that AI is a magic box that does anything, and that AI equals AGI. In reality AI is powerful but narrow, and its impact depends on thoughtful application.

**Q: What can AI NOT do well today?**
A: Tasks needing deep common sense, general reasoning across domains, creativity grounded in real understanding, or little/no data. It is narrow, not universal.

**Q: What determines whether AI can do a task?**
A: Whether it can be framed as an input → output mapping and whether enough data exists. Rule of thumb: "if a typical person can do it with a second of thought, AI can probably do it" (with data).

---

## Week 2 — Building AI Projects

### ML Project Workflow

**Q: What is the typical ML project workflow?**
A: (1) Collect data, (2) build/train a model, (3) deploy it, (4) monitor and maintain. Steps repeat as you improve the system.

**Q: What are the steps within model building?**
A: Choose model and data, train on training data, evaluate on a held-out test set, and tune to reduce error before deployment.

**Q: Why a train/test split?**
A: Train on one portion and evaluate on a separate, unseen portion to check generalization rather than memorization.

**Q: What is a benchmark/test set?**
A: A fixed set of examples used to measure accuracy or error rate. Using the same benchmark lets you judge whether a change improved the model.

**Q: Why is deployment its own step?**
A: A model creates value only when running in production for real users/systems. Deployment involves integration, latency, reliability, and monitoring.

**Q: Why monitor and maintain?**
A: Real-world data changes (**data drift**), so performance can degrade; systems need monitoring, retraining, and updates.

### Data Science Projects

**Q: What is the typical DS project workflow?**
A: (1) Collect data, (2) analyze/explore, (3) build and iterate on analyses/models, (4) present findings and recommendations, (5) take action.

**Q: What makes a DS project successful?**
A: A clear business question, good data, sound analysis, clear communication, and follow-through that turns insights into action.

### Teams and External Tools

**Q: What are the key AI team roles?**
A: ML engineers (models), data scientists (analysis/insight), data engineers (pipelines/infrastructure), software engineers (integration/deployment), and product/project managers (goals/coordination).

**Q: What should a non-technical manager know?**
A: Enough to set realistic goals, ask good questions, judge feasibility and data readiness, manage timelines, and avoid overpromising.

**Q: Build vs. buy?**
A: Building gives control and differentiation but is slower and costlier. Buying (vendor tools/APIs) is faster and cheaper but less customizable. Many teams buy first and build where it matters.

**Q: How do you judge feasibility?**
A: Check that the task is a clear input → output mapping, sufficient labeled data exists (or can be collected), and the expected accuracy/error rate is acceptable for the business.

**Q: What diligence is needed before starting?**
A: Define the business goal and success metric, confirm data availability/quality, estimate effort and cost, check technical feasibility, and plan evaluation and deployment.

---

## Week 3 — Building AI in Your Company

### Strategy and Case Selection

**Q: How should a company choose AI projects?**
A: Look for high-value, feasible use cases with available data and clear success metrics. Start with pilots, measure results, and scale what works.

**Q: What is the AI transformation playbook?**
A: (1) Run pilot projects for momentum, (2) build an in-house AI team, (3) provide broad AI training, (4) develop an AI strategy, (5) handle internal/external communications.

**Q: Why start with pilots?**
A: Pilots build momentum, prove value, surface issues, and create buy-in before large investment.

**Q: What roles does a company need?**
A: Leadership sponsorship, an AI team (ML engineers, data scientists, data engineers), and business units owning the use cases. Many use outside vendors early on.

**Q: Why is broad AI training important?**
A: Leaders need to know what AI can do, managers need to spot use cases, and engineers need to build and integrate. Training across levels makes adoption work.

**Q: What should an AI strategy include?**
A: Where AI creates strategic value, build vs. buy choices, data and infrastructure, talent and training, governance and risk, and measurable goals.

**Q: AI vs. digital transformation?**
A: Digital transformation modernizes processes and data infrastructure; AI transformation makes those processes smarter and more automated. AI often depends on good digital foundations.

**Q: Why is data infrastructure critical?**
A: AI needs accessible, high-quality, well-organized data. Inconsistent or siloed data is one of the biggest barriers.

### Roles and Decision-Making

**Q: How does AI affect leaders, managers, and engineers?**
A: Leaders set strategy and prioritize; managers identify use cases, define metrics, and manage projects; engineers build and deploy. Everyone benefits from AI literacy.

**Q: What are common adoption pitfalls?**
A: Vague goals, low-value use cases, poor data quality, underestimating change management, skipping evaluation, and expecting AI to solve everything.

**Q: How do you measure success?**
A: Concrete business metrics — revenue, cost, time saved, error reduction, customer satisfaction — tied to the original goal.

**Q: Why is change management important?**
A: People must trust and adopt the systems. Training, communication, and involving users early increase adoption and reduce resistance.

**Q: What is the team-building progression?**
A: Start with a small team or vendor support for pilots, build internal capability through training and hiring, then scale as AI becomes core to the business.

---

## Week 4 — AI and Society

### Benefits and Risks

**Q: What are AI's main benefits?**
A: Productivity, better healthcare and science, safer transportation, more personalized education, and new economic opportunities.

**Q: What are AI's main risks?**
A: Bias and unfairness, job displacement, privacy and surveillance, misinformation, concentration of power, security risks, and misuse.

**Q: What is bias and where does it come from?**
A: AI learns from historical data containing human biases; biased data produces biased predictions (e.g., hiring, lending).

**Q: How can bias be reduced?**
A: Use representative and balanced data, audit for disparate impact, involve diverse teams, and apply human oversight and fairness testing.

**Q: How does AI affect jobs?**
A: It automates some tasks and augments others, changing the nature of work, shifting demand toward judgment, oversight, and AI collaboration, and creating new roles. It is not simply "all jobs disappear."

**Q: Augmentation vs. automation?**
A: Augmentation helps people do work better/faster; automation performs tasks in place of people. AI often augments work while automating narrower tasks.

**Q: What are privacy concerns?**
A: AI often needs large amounts of data, including personal information. Concerns include consent, surveillance, misuse, and breaches; strong governance and privacy practices are essential.

**Q: What is adversarial/malicious use?**
A: Deepfakes, misinformation, fraud, and cyberattacks. Defenses include detection tools, policy, and public awareness.

**Q: What is responsible AI?**
A: Building and deploying AI that is fair, safe, transparent, accountable, privacy-respecting, and aligned with human values.

**Q: How can society manage risks?**
A: Education and awareness, regulation and policy, industry standards, transparency, human oversight for high-stakes decisions, and research on safety and fairness.

**Q: What should individuals do to prepare?**
A: Learn AI fundamentals, understand its strengths and limits, develop complementary skills (judgment, communication, creativity), and stay adaptive.

**Q: What is government's role?**
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
| Augmentation | AI helping people do work better/faster |
| Automation | AI performing tasks in place of people |
| Responsible AI | Fair, safe, transparent, accountable AI |

---

*Study aid; for authoritative content, refer to the official DeepLearning.AI course.*
