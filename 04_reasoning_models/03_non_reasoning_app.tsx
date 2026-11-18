"use client";

import { useMemo, useState } from "react";
import type { FormEvent } from "react";

type Rating = 1 | 2 | 3 | 4 | 5;

type Dimension = {
  id: string;
  title: string;
  weight: number;
  description: string;
  rubric: Record<Rating, string>;
  prompts: string[];
};

type Assessment = {
  rating: Rating | null;
  evidence: string;
};

type Recommendation = {
  label: string;
  detail: string;
  style: "strong" | "hire" | "leaning" | "leaning-no" | "no-hire";
};

const RATINGS: Rating[] = [1, 2, 3, 4, 5];

const INTERVIEW_STAGES = [
  "Recruiter screen",
  "Hiring manager interview",
  "Technical interview",
  "Portfolio / case study",
  "Behavioral interview",
  "Final interview",
  "Other",
] as const;

const dimensions: Dimension[] = [
  {
    id: "problem-solving",
    title: "Problem solving",
    weight: 25,
    description: "How the candidate approaches unfamiliar or ambiguous challenges.",
    rubric: {
      1: "Could not establish a workable approach, even with guidance.",
      2: "Found parts of a solution, but needed frequent direction.",
      3: "Reached a sound solution with reasonable guidance.",
      4: "Worked independently and explained trade-offs clearly.",
      5: "Developed an exceptional approach; anticipated edge cases and alternatives.",
    },
    prompts: [
      "What problem did they identify first?",
      "How did they respond to new information or a dead end?",
      "What trade-offs or edge cases did they consider?",
    ],
  },
  {
    id: "role-skills",
    title: "Role-related skills",
    weight: 25,
    description: "Evidence of the practical skills needed to succeed in this role.",
    rubric: {
      1: "Demonstrated significant gaps in core skills for this role.",
      2: "Showed some relevant skills, but important gaps remain.",
      3: "Met the expected bar for the core skills discussed.",
      4: "Showed strong depth and applied skills effectively.",
      5: "Demonstrated exceptional depth, breadth, and judgment.",
    },
    prompts: [
      "Which specific skill or concept did they demonstrate?",
      "What did they do or explain that showed their level?",
      "How closely does this map to the work they would do here?",
    ],
  },
  {
    id: "communication",
    title: "Communication & collaboration",
    weight: 20,
    description: "How clearly they share ideas, listen, and work through disagreement.",
    rubric: {
      1: "Had difficulty expressing ideas or engaging with discussion.",
      2: "Communication was inconsistent; frequent clarification was needed.",
      3: "Explained ideas clearly and responded constructively.",
      4: "Listened well, adapted explanations, and invited collaboration.",
      5: "Made complex ideas accessible and elevated the discussion.",
    },
    prompts: [
      "How did they explain a complex idea?",
      "What did they do when you asked a follow-up or disagreed?",
      "Did they make space for a two-way conversation?",
    ],
  },
  {
    id: "ownership",
    title: "Ownership & learning",
    weight: 15,
    description: "How they take responsibility, learn from experience, and adapt.",
    rubric: {
      1: "Could not identify their own contribution or learning.",
      2: "Gave limited examples of ownership or growth.",
      3: "Described a clear contribution and a relevant lesson learned.",
      4: "Showed strong accountability and applied learning in practice.",
      5: "Demonstrated exceptional initiative, reflection, and sustained growth.",
    },
    prompts: [
      "What did they personally own or drive?",
      "How did they respond to a mistake, setback, or feedback?",
      "What changed in their approach afterward?",
    ],
  },
  {
    id: "role-motivation",
    title: "Role motivation",
    weight: 15,
    description: "How their goals and interests align with the role’s actual work.",
    rubric: {
      1: "Motivation or expectations appeared substantially misaligned.",
      2: "Showed limited understanding of the role or its day-to-day work.",
      3: "Explained a credible interest in the role and its responsibilities.",
      4: "Connected their goals and strengths thoughtfully to the role.",
      5: "Showed a compelling, well-informed match with the role’s challenges.",
    },
    prompts: [
      "What aspect of the work interested them, specifically?",
      "What did they understand about the role’s day-to-day responsibilities?",
      "Where did their goals align—or not align—with the role?",
    ],
  },
];

const ratingLabels: Record<Rating, string> = {
  1: "Below bar",
  2: "Developing",
  3: "Meets bar",
  4: "Strong",
  5: "Exceptional",
};

const ratingDescriptions: Record<Rating, string> = {
  1: "Evidence suggests a substantial gap.",
  2: "Some evidence, with notable concerns.",
  3: "Solid evidence at the expected level.",
  4: "Consistently stronger than expected.",
  5: "Outstanding evidence for this level.",
};

const WEIGHT_SUMMARY = dimensions
  .map(({ title, weight }) => `${title} ${weight}%`)
  .join(", ");

function emptyAssessment(): Assessment {
  return { rating: null, evidence: "" };
}

function emptyAssessments(): Record<string, Assessment> {
  return Object.fromEntries(dimensions.map(({ id }) => [id, emptyAssessment()]));
}

function countWords(value: string): number {
  const trimmed = value.trim();
  return trimmed ? trimmed.split(/\s+/).length : 0;
}

function hasEnoughEvidence(evidence: string): boolean {
  return countWords(evidence) >= 5 && evidence.trim().length >= 30;
}

function getRecommendation(score: number): Recommendation {
  if (score >= 4.2) {
    return {
      label: "Strong hire",
      detail: "Evidence is consistently strong across the assessed dimensions.",
      style: "strong",
    };
  }
  if (score >= 3.5) {
    return {
      label: "Hire",
      detail: "The overall evidence meets the bar, with clear strengths.",
      style: "hire",
    };
  }
  if (score >= 2.7) {
    return {
      label: "Leaning hire",
      detail: "The evidence is mixed; review strengths and gaps together.",
      style: "leaning",
    };
  }
  if (score >= 2) {
    return {
      label: "Leaning no hire",
      detail: "Important concerns remain in the evidence collected.",
      style: "leaning-no",
    };
  }
  return {
    label: "No hire",
    detail: "The current evidence does not meet the expected bar.",
    style: "no-hire",
  };
}

function DimensionCard({
  dimension,
  assessment,
  submitted,
  onChange,
}: {
  dimension: Dimension;
  assessment: Assessment;
  submitted: boolean;
  onChange: (update: Partial<Assessment>) => void;
}) {
  const selectedRating = assessment.rating;
  const words = countWords(assessment.evidence);
  const evidenceOk = hasEnoughEvidence(assessment.evidence);

  return (
    <article className="dimension">
      <div className="dimension-top">
        <div>
          <h3 className="dimension-title">{dimension.title}</h3>
          <p className="dimension-description">{dimension.description}</p>
        </div>
        <span className="weight">{dimension.weight}% weight</span>
      </div>

      <div className="rating-label" id={`rating-${dimension.id}`}>
        <span>
          Your rating <span className="required">*</span>
        </span>
        <span>Use the rubric as your anchor</span>
      </div>
      <div
        className="rating-options"
        role="radiogroup"
        aria-label={`${dimension.title} rating`}
      >
        {RATINGS.map((rating) => (
          <button
            type="button"
            key={rating}
            role="radio"
            aria-checked={selectedRating === rating}
            aria-label={`${rating}: ${ratingLabels[rating]}. ${dimension.rubric[rating]}`}
            title={ratingDescriptions[rating]}
            className={`rating-option${selectedRating === rating ? " selected" : ""}`}
            onClick={() => onChange({ rating })}
          >
            <span className="rating-number">{rating}</span>
            <span className="rating-name">{ratingLabels[rating]}</span>
          </button>
        ))}
      </div>
      <div className="rubric-hint" aria-live="polite">
        {selectedRating
          ? dimension.rubric[selectedRating]
          : "Select a rating to see its behavioral anchor."}
      </div>

      <div className="evidence-block">
        <div className="evidence-heading">
          <label htmlFor={`evidence-${dimension.id}`}>
            Evidence &amp; examples <span className="required">*</span>
          </label>
          <span className={`word-count${evidenceOk ? " good" : ""}`}>
            {words} words · aim for 5+
          </span>
        </div>
        <textarea
          id={`evidence-${dimension.id}`}
          value={assessment.evidence}
          onChange={(event) => onChange({ evidence: event.target.value })}
          placeholder="Describe a specific moment: what was the situation, what did the candidate do or say, and what was the result?"
          aria-describedby={`prompts-${dimension.id}`}
          aria-invalid={submitted && !evidenceOk}
        />
        <div className="prompts" id={`prompts-${dimension.id}`}>
          {dimension.prompts.map((prompt) => (
            <span className="prompt-chip" key={prompt}>
              {prompt}
            </span>
          ))}
        </div>
        {submitted && !evidenceOk && (
          <p className="field-error">
            Add a specific example (at least 30 characters and 5 words) so this
            rating is grounded in evidence.
          </p>
        )}
        {submitted && !selectedRating && (
          <p className="field-error">Choose a rubric rating for this dimension.</p>
        )}
      </div>
    </article>
  );
}

export default function FeedbackForm() {
  const [candidate, setCandidate] = useState("");
  const [role, setRole] = useState("");
  const [interviewer, setInterviewer] = useState("");
  const [interviewStage, setInterviewStage] = useState("Technical interview");
  const [assessments, setAssessments] = useState(emptyAssessments);
  const [overallNotes, setOverallNotes] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const { scoredCount, weightedScore } = useMemo(() => {
    let earned = 0;
    let totalWeight = 0;
    let scored = 0;

    for (const dimension of dimensions) {
      const rating = assessments[dimension.id].rating;
      if (rating === null) continue;
      scored += 1;
      earned += rating * dimension.weight;
      totalWeight += dimension.weight;
    }

    return {
      scoredCount: scored,
      weightedScore: totalWeight === 0 ? null : earned / totalWeight,
    };
  }, [assessments]);

  const recommendation =
    weightedScore === null ? null : getRecommendation(weightedScore);

  const missingRatings = dimensions.filter(
    ({ id }) => assessments[id].rating === null
  );
  const missingEvidence = dimensions.filter(
    ({ id }) => !hasEnoughEvidence(assessments[id].evidence)
  );

  const canSubmit =
    candidate.trim().length > 0 &&
    role.trim().length > 0 &&
    interviewer.trim().length > 0 &&
    missingRatings.length === 0 &&
    missingEvidence.length === 0;

  function updateAssessment(id: string, update: Partial<Assessment>) {
    setAssessments((current) => ({
      ...current,
      [id]: { ...current[id], ...update },
    }));
    setSubmitted(false);
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitted(true);
    if (canSubmit) return;

    const targetId = missingRatings[0]
      ? `rating-${missingRatings[0].id}`
      : missingEvidence[0]
        ? `evidence-${missingEvidence[0].id}`
        : "candidate";

    document.getElementById(targetId)?.scrollIntoView({
      behavior: "smooth",
      block: "center",
    });
  }

  return (
    <main className="feedback-page">
      <style>{pageStyles}</style>

      <form className="form-shell" onSubmit={handleSubmit} noValidate>
        <div className="topline">
          <span className="topline-mark">✳</span>
          Structured interview feedback
        </div>

        <h1 className="page-title">A clearer picture, together.</h1>
        <p className="intro">
          Capture what the candidate actually demonstrated—not just a gut
          feeling. Your evidence helps the hiring team make fair, consistent
          decisions.
        </p>

        <div className="principle">
          <span className="principle-icon" aria-hidden="true">
            ✦
          </span>
          <span>
            <strong>Anchor every rating in observable behavior.</strong> Focus on
            what they said, did, or decided. Avoid assumptions about personality
            or potential that aren’t supported by the interview.
          </span>
        </div>

        <section className="card" aria-labelledby="details-heading">
          <div className="section-heading">
            <div>
              <h2 className="section-title" id="details-heading">
                Interview details
              </h2>
              <p className="section-subtitle">
                A little context helps feedback land in the right place.
              </p>
            </div>
            <span className="step-label">01 · Context</span>
          </div>
          <div className="field-grid">
            <div className="field">
              <label htmlFor="candidate">
                Candidate name <span className="required">*</span>
              </label>
              <input
                id="candidate"
                value={candidate}
                onChange={(event) => setCandidate(event.target.value)}
                placeholder="e.g. Jordan Lee"
                autoComplete="off"
                required
              />
            </div>
            <div className="field">
              <label htmlFor="role">
                Role <span className="required">*</span>
              </label>
              <input
                id="role"
                value={role}
                onChange={(event) => setRole(event.target.value)}
                placeholder="e.g. Senior Product Designer"
                required
              />
            </div>
            <div className="field">
              <label htmlFor="interviewer">
                Your name <span className="required">*</span>
              </label>
              <input
                id="interviewer"
                value={interviewer}
                onChange={(event) => setInterviewer(event.target.value)}
                placeholder="Your name"
                required
              />
            </div>
            <div className="field">
              <label htmlFor="stage">Interview stage</label>
              <select
                id="stage"
                value={interviewStage}
                onChange={(event) => setInterviewStage(event.target.value)}
              >
                {INTERVIEW_STAGES.map((stage) => (
                  <option key={stage}>{stage}</option>
                ))}
              </select>
            </div>
          </div>
        </section>

        <section className="card" aria-labelledby="assessment-heading">
          <div className="section-heading">
            <div>
              <h2 className="section-title" id="assessment-heading">
                Evaluate the evidence
              </h2>
              <p className="section-subtitle">
                Choose the closest rubric level, then include a concrete example
                for every dimension.
              </p>
            </div>
            <span className="step-label">02 · Assessment</span>
          </div>

          <div className="dimensions">
            {dimensions.map((dimension) => (
              <DimensionCard
                key={dimension.id}
                dimension={dimension}
                assessment={assessments[dimension.id]}
                submitted={submitted}
                onChange={(update) => updateAssessment(dimension.id, update)}
              />
            ))}
          </div>
        </section>

        <section className="card" aria-labelledby="recommendation-heading">
          <div className="section-heading">
            <div>
              <h2 className="section-title" id="recommendation-heading">
                Recommendation
              </h2>
              <p className="section-subtitle">
                Calculated from your weighted rubric scores as you go.
              </p>
            </div>
            <span className="step-label">03 · Decision</span>
          </div>

          <div className="summary-card" aria-live="polite">
            <div>
              <div className="summary-kicker">Weighted assessment</div>
              <div
                className={`recommendation-title${recommendation ? ` ${recommendation.style}` : ""}`}
              >
                {recommendation?.label ?? "Your recommendation will appear here"}
              </div>
              <p className="recommendation-detail">
                {recommendation?.detail ??
                  "Rate the dimensions above to see a preliminary recommendation."}
              </p>
              <div
                className="progress-line"
                role="progressbar"
                aria-label="Weighted interview score"
                aria-valuemin={0}
                aria-valuemax={5}
                aria-valuenow={weightedScore ?? 0}
              >
                <div
                  className="progress-fill"
                  style={{ width: `${((weightedScore ?? 0) / 5) * 100}%` }}
                />
              </div>
              <p className="recommendation-note">
                {scoredCount < dimensions.length
                  ? `${scoredCount} of ${dimensions.length} dimensions rated. The score uses only completed ratings until all are assessed.`
                  : `Weighted score: ${WEIGHT_SUMMARY}.`}
              </p>
            </div>
            <div className="score-badge">
              {weightedScore === null ? "—" : weightedScore.toFixed(1)}
              <small>OUT OF 5</small>
            </div>
          </div>

          <div className="field overall-note">
            <label htmlFor="overall-notes">
              Overall context{" "}
              <span className="optional-label">(optional)</span>
            </label>
            <textarea
              id="overall-notes"
              value={overallNotes}
              onChange={(event) => setOverallNotes(event.target.value)}
              placeholder="What should the hiring team keep in mind? Note relevant context, unresolved questions, or areas to explore in another interview."
            />
          </div>
        </section>

        <div className="footer">
          <p className="footer-hint">
            Each dimension needs a rating and a specific example before feedback
            can be submitted. Recommendations are a decision aid—not a
            substitute for reviewing the evidence together.
          </p>
          <button className="submit-button" type="submit">
            Submit feedback <span aria-hidden="true">→</span>
          </button>
        </div>

        {submitted && canSubmit && (
          <div className="success-banner" role="status">
            Feedback is complete for <strong>{candidate}</strong>. Your
            preliminary recommendation is{" "}
            <strong>{recommendation?.label}</strong> (
            {weightedScore?.toFixed(1)} / 5).
          </div>
        )}

        {submitted && !canSubmit && (
          <div className="success-banner incomplete" role="alert">
            Please complete the required details, rate every dimension, and add
            a specific evidence example for each one.
          </div>
        )}

        <p className="form-footnote">
          Structured feedback supports fairer hiring. Rate only job-relevant
          evidence from this interview.
        </p>
      </form>
    </main>
  );
}

const pageStyles = `
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

  * { box-sizing: border-box; }
  .feedback-page {
    --ink: #202824;
    --muted: #77817b;
    --line: #e6e9e4;
    --green: #426c55;
    --green-dark: #315840;
    --green-pale: #edf3ed;
    min-height: 100vh;
    padding: 48px 20px 80px;
    background:
      radial-gradient(ellipse at 14% 0%, rgba(224, 235, 222, .55), transparent 34%),
      #f7f8f5;
    color: var(--ink);
    font-family: 'DM Sans', sans-serif;
  }
  .form-shell { width: min(100%, 850px); margin: 0 auto; }
  .topline {
    display: flex; align-items: center; gap: 9px;
    margin-bottom: 23px; color: var(--green);
    font-size: 12px; font-weight: 700; letter-spacing: .11em;
    text-transform: uppercase;
  }
  .topline-mark {
    display: grid; place-items: center; width: 28px; height: 28px;
    border: 1px solid #d5e1d4; border-radius: 9px;
    background: #eff5ed; font-size: 15px;
  }
  h1, h2, h3, p { margin-top: 0; }
  .page-title {
    margin-bottom: 9px; font: 800 clamp(30px, 5vw, 42px)/1.12 'Manrope', sans-serif;
    letter-spacing: -.045em;
  }
  .intro {
    max-width: 590px; margin-bottom: 30px; color: #68736c;
    font-size: 15px; line-height: 1.7;
  }
  .principle {
    display: flex; gap: 12px; align-items: flex-start;
    padding: 15px 17px; margin-bottom: 27px;
    border: 1px solid #e0e9df; border-radius: 13px;
    background: rgba(240, 246, 238, .8);
    color: #526455; font-size: 13px; line-height: 1.6;
  }
  .principle-icon { font-size: 17px; }
  .principle strong { color: #334c39; }
  .card {
    margin-top: 18px; padding: 25px;
    border: 1px solid var(--line); border-radius: 17px;
    background: rgba(255, 255, 255, .94);
    box-shadow: 0 5px 20px rgba(34, 47, 37, .035);
  }
  .section-heading {
    display: flex; justify-content: space-between; align-items: flex-start;
    gap: 16px; margin-bottom: 20px;
  }
  .section-title {
    margin-bottom: 5px; font: 700 18px 'Manrope', sans-serif;
    letter-spacing: -.025em;
  }
  .section-subtitle { margin-bottom: 0; color: var(--muted); font-size: 13px; line-height: 1.5; }
  .step-label {
    flex: none; padding: 6px 9px; border: 1px solid #e9ece7;
    border-radius: 999px; color: #78817a; font-size: 11px; font-weight: 700;
  }
  .field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .field { min-width: 0; }
  .field label, .field-label {
    display: block; margin-bottom: 7px; color: #3b443e;
    font-size: 12px; font-weight: 700;
  }
  .required { color: #bd6e50; }
  .optional-label { color: #89918a; font-weight: 500; }
  input, select, textarea {
    width: 100%; border: 1px solid #dfe4de; border-radius: 9px;
    outline: none; background: #fff; color: var(--ink);
    font: 13px 'DM Sans', sans-serif; transition: border-color .16s, box-shadow .16s;
  }
  input, select { height: 42px; padding: 0 12px; }
  textarea { min-height: 108px; padding: 12px; resize: vertical; line-height: 1.6; }
  input::placeholder, textarea::placeholder { color: #a4aca5; }
  input:focus, select:focus, textarea:focus {
    border-color: #78967d; box-shadow: 0 0 0 3px rgba(87, 125, 94, .11);
  }
  .dimensions { display: grid; gap: 14px; }
  .dimension {
    padding: 19px 20px; border: 1px solid #e7eae5; border-radius: 13px;
    background: #fdfefd;
  }
  .dimension-top {
    display: flex; justify-content: space-between; align-items: flex-start;
    gap: 14px; margin-bottom: 15px;
  }
  .dimension-title {
    margin-bottom: 4px; font: 700 15px 'Manrope', sans-serif;
    letter-spacing: -.02em;
  }
  .dimension-description { margin: 0; color: var(--muted); font-size: 12px; line-height: 1.5; }
  .weight {
    flex: none; padding: 5px 8px; border-radius: 7px;
    background: #f1f3ef; color: #69746b; font-size: 11px; font-weight: 700;
  }
  .rating-label {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 8px; color: #58625b; font-size: 11px; font-weight: 700;
  }
  .rating-options { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; }
  .rating-option {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    min-height: 62px; padding: 7px 4px; border: 1px solid #e5e9e3;
    border-radius: 9px; background: white; color: #7c857e;
    cursor: pointer; transition: .16s ease;
  }
  .rating-option:hover { border-color: #aac0aa; background: #f8fbf7; }
  .rating-option.selected {
    border-color: #5c8063; background: #edf4ed; color: #315840;
    box-shadow: inset 0 0 0 1px #5c8063;
  }
  .rating-number { margin-bottom: 3px; font: 700 17px 'Manrope', sans-serif; }
  .rating-name { font-size: 10px; font-weight: 600; text-align: center; }
  .rubric-hint {
    min-height: 34px; padding: 8px 10px; margin-top: 8px;
    border-radius: 7px; background: #f6f8f5; color: #707b72;
    font-size: 11px; line-height: 1.45;
  }
  .evidence-block { margin-top: 16px; }
  .evidence-heading {
    display: flex; align-items: baseline; justify-content: space-between;
    gap: 10px; margin-bottom: 7px;
  }
  .evidence-heading label { color: #3b443e; font-size: 12px; font-weight: 700; }
  .word-count { color: #8b948c; font-size: 10px; }
  .word-count.good { color: #4c7955; }
  .prompts {
    display: flex; flex-wrap: wrap; gap: 6px; margin: 9px 0 0;
  }
  .prompt-chip {
    padding: 5px 8px; border: 1px solid #edf0eb; border-radius: 6px;
    background: #f8f9f7; color: #7b857d; font-size: 10px; line-height: 1.35;
  }
  .field-error { margin: 7px 0 0; color: #ae5a48; font-size: 11px; line-height: 1.5; }
  .summary-card {
    position: relative; overflow: hidden;
    display: grid; grid-template-columns: 1fr auto; align-items: center;
    gap: 20px; padding: 22px 24px; border: 1px solid #dce7dc;
    border-radius: 14px; background: linear-gradient(115deg, #f0f6ef, #fbfcfa);
  }
  .summary-card::after {
    position: absolute; content: ""; width: 160px; height: 160px;
    right: -55px; top: -100px; border-radius: 50%; background: rgba(181, 205, 181, .18);
  }
  .summary-kicker {
    margin-bottom: 6px; color: #718074; font-size: 10px; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
  }
  .recommendation-title {
    margin-bottom: 4px; font: 800 22px 'Manrope', sans-serif;
    letter-spacing: -.035em; color: #34563c;
  }
  .recommendation-title.strong { color: #234d32; }
  .recommendation-title.hire { color: #34563c; }
  .recommendation-title.leaning { color: #6b5f2e; }
  .recommendation-title.leaning-no { color: #8a5530; }
  .recommendation-title.no-hire { color: #8a3a32; }
  .recommendation-detail { margin: 0; color: #748077; font-size: 12px; line-height: 1.5; }
  .score-badge {
    position: relative; z-index: 1; display: grid; place-items: center;
    width: 76px; height: 76px; border: 1px solid #d7e3d5; border-radius: 50%;
    background: white; color: #426c4a; font: 800 21px 'Manrope', sans-serif;
  }
  .score-badge small { margin-top: -16px; color: #8b958c; font: 500 9px 'DM Sans', sans-serif; }
  .progress-line { height: 4px; margin-top: 15px; overflow: hidden; border-radius: 8px; background: #e4eae2; }
  .progress-fill { height: 100%; border-radius: inherit; background: #759477; transition: width .25s ease; }
  .recommendation-note { margin-top: 11px; color: #7a847b; font-size: 11px; line-height: 1.5; }
  .overall-note { margin-top: 20px; }
  .overall-note textarea { min-height: 90px; }
  .footer {
    display: flex; align-items: center; justify-content: space-between;
    gap: 16px; margin-top: 20px;
  }
  .footer-hint { max-width: 440px; margin: 0; color: #89918a; font-size: 11px; line-height: 1.5; }
  .submit-button {
    display: inline-flex; align-items: center; justify-content: center; gap: 9px;
    min-height: 45px; padding: 0 18px; border: 0; border-radius: 9px;
    background: var(--green); color: white; font: 700 13px 'DM Sans', sans-serif;
    cursor: pointer; transition: background .16s, transform .16s;
  }
  .submit-button:hover { background: var(--green-dark); transform: translateY(-1px); }
  .success-banner {
    margin-top: 14px; padding: 12px 14px; border: 1px solid #d9e8d8;
    border-radius: 9px; background: #f0f7ef; color: #426c4a;
    font-size: 12px; line-height: 1.5;
  }
  .success-banner.incomplete {
    border-color: #ecd9cd; background: #fbf5f0; color: #985d43;
  }
  .form-footnote { margin: 21px 0 0; color: #9aa29b; text-align: center; font-size: 10px; }
  @media (max-width: 620px) {
    .feedback-page { padding: 30px 14px 52px; }
    .card { padding: 19px 16px; }
    .field-grid { grid-template-columns: 1fr; gap: 13px; }
    .dimension { padding: 16px 13px; }
    .dimension-top { gap: 8px; }
    .rating-options { gap: 5px; }
    .rating-option { min-height: 57px; }
    .rating-name { font-size: 9px; }
    .summary-card { padding: 18px; }
    .score-badge { width: 66px; height: 66px; }
    .footer { align-items: stretch; flex-direction: column; }
    .submit-button { width: 100%; }
  }
`;
