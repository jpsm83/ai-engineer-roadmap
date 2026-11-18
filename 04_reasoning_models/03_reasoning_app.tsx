"use client";

import { useMemo, useState } from "react";
import type { CSSProperties, FormEvent } from "react";

type Rating = 1 | 2 | 3 | 4 | 5;

type Rubric = {
  id: string;
  label: string;
  weight: number;
  description: string;
  scale: Record<Rating, string>;
  prompts: string[];
};

type Ratings = Record<string, Rating>;
type EvidenceMap = Record<string, string>;

type RubricResult = {
  id: string;
  rating: Rating;
  evidence: string;
};

type Submission = {
  interviewer: string;
  candidate: string;
  date: string;
  reference: string;
  rubricResults: RubricResult[];
  overallScore: number;
  recommendation: string;
};

const RATINGS: Rating[] = [1, 2, 3, 4, 5];

const RUBRICS: Rubric[] = [
  {
    id: "technical",
    label: "Technical Skills",
    weight: 0.3,
    description:
      "Proficiency with required tools, coding practices, architecture, and applying knowledge to real problems.",
    scale: {
      1: "Unfamiliar with fundamentals; struggles to complete tasks.",
      2: "Basic knowledge; requires guidance and rework.",
      3: "Proficient and reliable for typical tasks.",
      4: "Strong understanding; efficient and thoughtful problem-solving.",
      5: "Expert-level; anticipates edge cases and optimizes solutions.",
    },
    prompts: [
      "Describe a specific technical challenge they faced and how they approached it.",
      "Did they select appropriate tools/approach? Why or why not?",
      "What was the impact on deliverables or quality?",
      "Provide a concrete example of a technical decision they made.",
    ],
  },
  {
    id: "problem",
    label: "Problem Solving & Debugging",
    weight: 0.25,
    description:
      "Analytical thinking, systematic approach to ambiguous problems, and effective debugging.",
    scale: {
      1: "Struggles to outline a path; reactive rather than proactive.",
      2: "Defines a basic plan but misses edge cases.",
      3: "Uses a methodical approach; handles common scenarios well.",
      4: "Diagnoses root causes quickly; demonstrates iterative refinement.",
      5: "Exhibits exceptional reasoning; innovates robust, scalable solutions.",
    },
    prompts: [
      "Provide a concrete debugging example and the steps taken.",
      "How did they decompose the problem and verify a solution?",
      "What was the outcome and any follow-up improvements?",
      "Did they consider performance or future maintenance implications?",
    ],
  },
  {
    id: "communication",
    label: "Communication",
    weight: 0.2,
    description:
      "Clarity of articulation, listening, documentation, and ability to tailor messages to stakeholders.",
    scale: {
      1: "Poor clarity; struggles to convey thoughts.",
      2: "Somewhat clear but may be scattered; needs follow-up.",
      3: "Clear and concise; communicates key points.",
      4: "Structured and persuasive; uses examples and visuals when helpful.",
      5: "Empathetic; excellent listener; communicates complex topics effectively to diverse audiences.",
    },
    prompts: [
      "Describe how they explained a technical concept to a non-technical stakeholder.",
      "Did they solicit and incorporate feedback effectively?",
      "Provide an example of documenting decisions or outcomes clearly.",
      "How did they handle miscommunications or conflicting viewpoints?",
    ],
  },
  {
    id: "collaboration",
    label: "Collaboration & Teamwork",
    weight: 0.15,
    description:
      "Team interaction, responsiveness to feedback, and ability to contribute in a team setting.",
    scale: {
      1: "Struggles to collaborate; reliant on others.",
      2: "Meets minimum expectations; occasionally contributes.",
      3: "Proactive teammate; shares context and helps others.",
      4: "Mentors others; fosters positive team dynamics.",
      5: "Leads by influence; elevates team performance and morale.",
    },
    prompts: [
      "Give an example of a time they helped a teammate succeed.",
      "How did they handle conflicting opinions within the team?",
      "What was their role in sprint planning or peer reviews?",
      "Describe their approach to giving and receiving feedback.",
    ],
  },
  {
    id: "leadership",
    label: "Leadership Potential",
    weight: 0.1,
    description:
      "Ownership, initiative, and potential to guide initiatives or people.",
    scale: {
      1: "No leadership indicators; reliance on others.",
      2: "Takes ownership of small tasks; limited scope.",
      3: "Leads small tasks or projects; dependable.",
      4: "Often guides others; demonstrates accountability and strategy.",
      5: "Strong leadership with vision; drives impact beyond their role.",
    },
    prompts: [
      "Describe a situation where they took ownership of a project end-to-end.",
      "How do they handle setbacks or accountability when things go off track?",
      "What strategic impact did their actions have on the team or project?",
      "Are they trusted to mentor peers or new hires?",
    ],
  },
];

const RECOMMENDATION_COLORS: Record<string, string> = {
  "Strong Hire": "#065f46",
  Hire: "#166534",
  Consider: "#92400e",
  Hold: "#374151",
  "Do Not Hire": "#b91c1c",
};

const styles: Record<string, CSSProperties> = {
  container: {
    fontFamily:
      "Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial",
    padding: "20px",
    maxWidth: 980,
    margin: "0 auto",
  },
  header: {
    textAlign: "left",
    padding: "20px 24px",
    borderRadius: 12,
    marginBottom: 16,
    background: "linear-gradient(135deg, #f8f9fb 0%, #eef2f7 100%)",
    border: "1px solid #e5e7eb",
    boxShadow: "0 6px 20px rgba(0,0,0,0.04)",
  },
  title: {
    fontSize: 26,
    fontWeight: 700,
    margin: 0,
  },
  subtitle: {
    fontSize: 14,
    marginTop: 6,
    color: "#555",
  },
  form: {
    display: "grid",
    gridTemplateColumns: "1fr",
    gap: 20,
  },
  section: {
    border: "1px solid #e5e7eb",
    borderRadius: 12,
    padding: 16,
    background: "#fff",
    boxShadow: "0 2px 6px rgba(0,0,0,0.04)",
  },
  sectionHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "baseline",
    marginBottom: 6,
  },
  label: {
    fontSize: 16,
    fontWeight: 600,
  },
  weight: {
    fontSize: 12,
    color: "#555",
  },
  rubricCard: {
    padding: 12,
    borderRadius: 10,
    border: "1px solid #e6e6e6",
    background: "#fafafa",
  },
  rubricHeader: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 12,
    marginBottom: 8,
  },
  rubricTitle: {
    fontSize: 15,
    fontWeight: 700,
  },
  rubricDescription: {
    fontSize: 12,
    color: "#555",
    textAlign: "right",
    maxWidth: 360,
  },
  scaleRow: {
    display: "flex",
    gap: 8,
    alignItems: "center",
    marginBottom: 6,
    flexWrap: "wrap",
  },
  ratingOption: {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    width: 36,
    height: 28,
    borderRadius: 6,
    border: "1px solid #cbd5e1",
    cursor: "pointer",
    userSelect: "none",
    background: "#fff",
  },
  ratingSelected: {
    background: "#e0f2fe",
    borderColor: "#93c5fd",
  },
  evidenceBox: {
    width: "100%",
    minHeight: 80,
    padding: 8,
    borderRadius: 8,
    border: "1px solid #d1d5db",
    resize: "vertical",
  },
  prompts: {
    marginTop: 6,
    paddingLeft: 18,
    color: "#374151",
    fontSize: 13,
  },
  promptsItem: {
    marginBottom: 4,
  },
  error: {
    color: "#b91c1c",
    fontSize: 12,
    marginTop: 6,
  },
  guidance: {
    fontSize: 12,
    color: "#374151",
    marginTop: 6,
  },
  summary: {
    padding: 14,
    borderRadius: 12,
    background: "linear-gradient(135deg, #f0f4ff 0%, #ffffff 100%)",
    border: "1px solid #dbeafe",
  },
  scoreBar: {
    height: 12,
    borderRadius: 999,
    background: "#e5e7eb",
    width: "100%",
    overflow: "hidden",
  },
  scoreFill: {
    height: "100%",
    borderRadius: 999,
    background: "linear-gradient(90deg, #a5b4fc, #34d399)",
  },
  metaRow: {
    display: "flex",
    gap: 12,
    alignItems: "center",
    justifyContent: "space-between",
    flexWrap: "wrap",
  },
  input: {
    padding: "10px 12px",
    borderRadius: 8,
    border: "1px solid #d1d5db",
    width: "100%",
    outline: "none",
  },
  fieldLabel: {
    fontSize: 12,
    color: "#555",
  },
  buttonRow: {
    display: "flex",
    gap: 12,
    alignItems: "center",
    marginTop: 12,
  },
  button: {
    padding: "10px 14px",
    borderRadius: 8,
    border: "none",
    cursor: "pointer",
    fontWeight: 600,
  },
  primary: {
    background: "#4f46e5",
    color: "#fff",
  },
  secondary: {
    background: "#e5e7eb",
    color: "#111827",
  },
  hint: {
    fontSize: 12,
    color: "#64748b",
  },
  gridTwo: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 16,
  },
  fieldGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 12,
  },
};

function todayIsoDate(): string {
  return new Date().toISOString().slice(0, 10);
}

function createInitialRatings(): Ratings {
  return Object.fromEntries(
    RUBRICS.map((rubric) => [rubric.id, 3 as Rating])
  );
}

function createInitialEvidence(): EvidenceMap {
  return Object.fromEntries(RUBRICS.map((rubric) => [rubric.id, ""]));
}

function computeWeightedScore(ratings: Ratings): number {
  return RUBRICS.reduce(
    (total, rubric) => total + ratings[rubric.id] * rubric.weight,
    0
  );
}

function getRecommendation(score: number): string {
  if (score >= 4.5) return "Strong Hire";
  if (score >= 4.0) return "Hire";
  if (score >= 3.0) return "Consider";
  if (score >= 2.0) return "Hold";
  return "Do Not Hire";
}

function isEvidenceAdequate(text: string): boolean {
  const evidence = text.trim();
  if (evidence.length >= 40) return true;
  const sentences = evidence
    .split(/[.!?]+/)
    .filter((part) => part.trim().length > 0);
  return sentences.length >= 2;
}

function rubricError(rating: Rating | undefined, evidence: string): string {
  if (!rating || rating < 1 || rating > 5) {
    return "Please provide a rating between 1 and 5.";
  }
  if (!isEvidenceAdequate(evidence)) {
    return "Provide more concrete evidence/examples (try 2-3 sentences).";
  }
  return "";
}

function truncate(text: string, maxLength: number): string {
  return text.length > maxLength ? `${text.slice(0, maxLength)}…` : text;
}

function RatingSelector({
  rubric,
  value,
  onChange,
}: {
  rubric: Rubric;
  value: Rating;
  onChange: (value: Rating) => void;
}) {
  return (
    <div style={{ marginTop: 6 }}>
      <div role="radiogroup" aria-label={rubric.label} style={styles.scaleRow}>
        {RATINGS.map((rating) => (
          <label
            key={rating}
            style={{
              ...styles.ratingOption,
              ...(value === rating ? styles.ratingSelected : {}),
            }}
          >
            <input
              type="radio"
              name={`rating-${rubric.id}`}
              value={rating}
              checked={value === rating}
              onChange={() => onChange(rating)}
              style={{ display: "none" }}
            />
            <span style={{ fontSize: 12 }}>{rating}</span>
          </label>
        ))}
      </div>
      <div className="scale-description" style={styles.guidance}>
        {rubric.scale[value]}
      </div>
    </div>
  );
}

function RubricCard({
  rubric,
  rating,
  evidence,
  error,
  onRatingChange,
  onEvidenceChange,
}: {
  rubric: Rubric;
  rating: Rating;
  evidence: string;
  error: string;
  onRatingChange: (value: Rating) => void;
  onEvidenceChange: (text: string) => void;
}) {
  const promptPreview = rubric.prompts.slice(0, 3).join(" ");

  return (
    <div style={styles.rubricCard} aria-label={rubric.label}>
      <div style={styles.rubricHeader}>
        <div style={styles.rubricTitle}>
          {rubric.label}{" "}
          <span style={styles.weight}>
            (Weight {Math.round(rubric.weight * 100)}%)
          </span>
        </div>
        <div style={styles.rubricDescription}>{rubric.description}</div>
      </div>

      <RatingSelector
        rubric={rubric}
        value={rating}
        onChange={onRatingChange}
      />

      <div style={{ marginTop: 8 }}>
        <label style={{ fontSize: 13, color: "#374151" }}>
          Evidence / Specific Examples:
        </label>
        <textarea
          aria-label={`Evidence for ${rubric.label}`}
          style={styles.evidenceBox}
          placeholder={`Provide concrete, behavior-based evidence for ${rubric.label}. Example prompts: ${promptPreview}`}
          value={evidence}
          onChange={(event) => onEvidenceChange(event.target.value)}
        />
        <div className="evidence-guidance" style={styles.guidance}>
          Helpful prompts:
          <ul style={styles.prompts}>
            {rubric.prompts.map((prompt) => (
              <li key={prompt} style={styles.promptsItem}>
                "{prompt}"
              </li>
            ))}
          </ul>
        </div>
        {error ? (
          <div style={styles.error} role="alert">
            {error}
          </div>
        ) : null}
      </div>

      <hr
        style={{
          border: "none",
          borderTop: "1px solid #eee",
          marginTop: 12,
        }}
      />
      <div style={{ fontSize: 12, color: "#555" }}>
        Example reflection: Focus on concrete actions, outcomes, and the
        candidate’s behavior in specific situations. Tie feedback to observable
        actions.
      </div>
    </div>
  );
}

export default function FeedbackForm() {
  const [interviewerName, setInterviewerName] = useState("");
  const [candidateName, setCandidateName] = useState("");
  const [interviewDate, setInterviewDate] = useState(todayIsoDate);
  const [internalReference, setInternalReference] = useState("");
  const [ratings, setRatings] = useState(createInitialRatings);
  const [evidence, setEvidence] = useState(createInitialEvidence);
  const [submittedData, setSubmittedData] = useState<Submission | null>(null);

  const weightedScore = useMemo(() => computeWeightedScore(ratings), [ratings]);
  const recommendation = getRecommendation(weightedScore);
  const numericScore = Math.round(weightedScore * 10) / 10;

  const errors = useMemo(
    () =>
      Object.fromEntries(
        RUBRICS.map((rubric) => [
          rubric.id,
          rubricError(ratings[rubric.id], evidence[rubric.id] ?? ""),
        ])
      ),
    [ratings, evidence]
  );

  const allValid =
    candidateName.trim().length > 0 &&
    interviewerName.trim().length > 0 &&
    interviewDate.trim().length > 0 &&
    RUBRICS.every((rubric) => errors[rubric.id] === "");

  function handleRatingChange(rubricId: string, value: Rating) {
    setRatings((current) => ({ ...current, [rubricId]: value }));
    setSubmittedData(null);
  }

  function handleEvidenceChange(rubricId: string, text: string) {
    setEvidence((current) => ({ ...current, [rubricId]: text }));
    setSubmittedData(null);
  }

  function resetForm() {
    setInterviewDate(todayIsoDate());
    setInterviewerName("");
    setCandidateName("");
    setInternalReference("");
    setRatings(createInitialRatings());
    setEvidence(createInitialEvidence());
    setSubmittedData(null);
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!allValid) return;

    setSubmittedData({
      interviewer: interviewerName.trim(),
      candidate: candidateName.trim(),
      date: interviewDate,
      reference: internalReference.trim(),
      rubricResults: RUBRICS.map((rubric) => ({
        id: rubric.id,
        rating: ratings[rubric.id],
        evidence: evidence[rubric.id],
      })),
      overallScore: weightedScore,
      recommendation,
    });
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>Interview Feedback Form</h2>
        <div style={styles.subtitle}>
          Help us collect structured, objective feedback. Rate across rubrics,
          provide concrete evidence, and receive an auto-generated
          recommendation.
        </div>
      </div>

      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.gridTwo}>
          <div style={styles.section}>
            <div style={styles.sectionHeader}>
              <div style={styles.label}>Interviewer & Candidate Details</div>
              <span style={styles.weight}>All fields required</span>
            </div>

            <div style={styles.fieldGrid}>
              <div>
                <label style={styles.fieldLabel}>Interviewer Name</label>
                <input
                  type="text"
                  value={interviewerName}
                  onChange={(event) => setInterviewerName(event.target.value)}
                  placeholder="e.g., Jordan Lee"
                  style={styles.input}
                  required
                />
              </div>
              <div>
                <label style={styles.fieldLabel}>Candidate Name</label>
                <input
                  type="text"
                  value={candidateName}
                  onChange={(event) => setCandidateName(event.target.value)}
                  placeholder="e.g., Alex Kim"
                  style={styles.input}
                  required
                />
              </div>
            </div>

            <div style={{ ...styles.fieldGrid, marginTop: 12 }}>
              <div>
                <label style={styles.fieldLabel}>Interview Date</label>
                <input
                  type="date"
                  value={interviewDate}
                  onChange={(event) => setInterviewDate(event.target.value)}
                  style={styles.input}
                  required
                />
              </div>
              <div>
                <label style={styles.fieldLabel}>
                  Optional: Internal Reference
                </label>
                <input
                  type="text"
                  value={internalReference}
                  onChange={(event) => setInternalReference(event.target.value)}
                  placeholder="e.g., Ref ID or project tag"
                  style={styles.input}
                />
              </div>
            </div>

            <div style={styles.buttonRow}>
              <button
                type="button"
                onClick={resetForm}
                style={{ ...styles.button, ...styles.secondary }}
              >
                Reset
              </button>
              <span style={styles.hint}>
                Tip: Use behavioral prompts in each rubric to ensure objective
                feedback.
              </span>
            </div>
          </div>

          <div style={{ ...styles.section, ...styles.summary }}>
            <div style={styles.sectionHeader}>
              <div style={styles.label}>Score Summary</div>
              <span style={styles.weight}>Auto-calculated</span>
            </div>

            <div style={{ display: "grid", gap: 8 }}>
              <div style={{ fontSize: 14, color: "#374151" }}>
                Overall Score: <strong>{numericScore.toFixed(1)} / 5</strong>
              </div>
              <div
                style={styles.scoreBar}
                role="progressbar"
                aria-label={`Overall score ${numericScore}`}
                aria-valuemin={0}
                aria-valuemax={5}
                aria-valuenow={numericScore}
                title={`Score ${numericScore.toFixed(1)}`}
              >
                <div
                  style={{
                    ...styles.scoreFill,
                    width: `${(numericScore / 5) * 100}%`,
                  }}
                />
              </div>
              <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
                <span style={{ fontSize: 12, color: "#555" }}>
                  Recommendation:
                </span>
                <span
                  style={{
                    fontWeight: 700,
                    color:
                      RECOMMENDATION_COLORS[recommendation] ?? "#b91c1c",
                  }}
                >
                  {recommendation}
                </span>
              </div>
              <div style={{ fontSize: 12, color: "#555" }}>
                Note: This is a structured estimate. Final hiring decision
                should also consider team fit and business needs.
              </div>
            </div>
          </div>
        </div>

        <div style={styles.section}>
          <div style={styles.sectionHeader}>
            <div style={styles.label}>Rubrics & Evidence</div>
            <span style={styles.weight}>
              Each rating requires specific, behavioral evidence
            </span>
          </div>

          {RUBRICS.map((rubric) => (
            <RubricCard
              key={rubric.id}
              rubric={rubric}
              rating={ratings[rubric.id]}
              evidence={evidence[rubric.id] ?? ""}
              error={errors[rubric.id]}
              onRatingChange={(value) => handleRatingChange(rubric.id, value)}
              onEvidenceChange={(text) => handleEvidenceChange(rubric.id, text)}
            />
          ))}
        </div>

        <div style={styles.section}>
          <div style={styles.sectionHeader}>
            <div style={styles.label}>Finalization</div>
            <span style={styles.weight}>Validation & Submission</span>
          </div>
          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <button
              type="submit"
              disabled={!allValid}
              style={{
                ...styles.button,
                ...styles.primary,
                opacity: allValid ? 1 : 0.5,
                cursor: allValid ? "pointer" : "not-allowed",
              }}
              aria-disabled={!allValid}
            >
              Submit Feedback
            </button>
            <span style={styles.hint}>
              Validation ensures all rubrics have a rating and adequate
              evidence.
            </span>
          </div>
          {!allValid && (
            <div style={styles.error} role="alert" aria-live="polite">
              Please complete all rubrics with valid ratings and provide
              adequate evidence (minimum ~40 chars or 2 sentences) per rubric.
            </div>
          )}
        </div>

        {submittedData && (
          <div style={styles.section} aria-live="polite">
            <div style={styles.sectionHeader}>
              <div style={styles.label}>Submission Summary</div>
              <span style={styles.weight}>Saved locally for this session</span>
            </div>
            <div style={styles.metaRow}>
              <div>
                <strong>Candidate:</strong> {submittedData.candidate}
                <br />
                <strong>Interviewer:</strong> {submittedData.interviewer}
                <br />
                <strong>Date:</strong> {submittedData.date}
                {submittedData.reference ? (
                  <>
                    <br />
                    <strong>Reference:</strong> {submittedData.reference}
                  </>
                ) : null}
              </div>
              <div style={{ textAlign: "right" }}>
                <div>
                  <strong>Overall Score:</strong>{" "}
                  {submittedData.overallScore.toFixed(1)} / 5
                </div>
                <div>
                  <strong>Recommendation:</strong> {submittedData.recommendation}
                </div>
              </div>
            </div>
            <div style={{ marginTop: 12 }}>
              <strong>Rubric Details:</strong>
              <ul style={{ marginTop: 6, paddingLeft: 18 }}>
                {submittedData.rubricResults.map((result) => (
                  <li key={result.id}>
                    <strong>
                      {RUBRICS.find((rubric) => rubric.id === result.id)?.label}:
                    </strong>{" "}
                    Rating {result.rating} • Evidence:{" "}
                    {truncate(result.evidence, 60)}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </form>
    </div>
  );
}
