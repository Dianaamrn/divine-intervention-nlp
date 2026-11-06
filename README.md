# Divine Intervention: Can LLMs Be a Good Homer?

An NLP course project investigating whether instructions based on the twelve
Olympian gods change an LLM's stated decisions compared with a neutral judge.

## Current stage: reviewing the personas and dilemma drafts

The first version contains twelve working profiles: Zeus, Hera, Poseidon, Athena,
Apollo, Artemis, Ares, Aphrodite, Hephaestus, Hermes, Demeter, and Dionysus.
Each has ten research dimensions and a shorter pilot persona for prompting.
No model has been trained or run. Twelve neutral dilemma drafts are included
and await your review.

Read [the twelve dilemma drafts](dilemmas/dilemmas_review.md) to review their
wording, competing requests, and scoring poles. The matching structured records
are in [dilemmas.json](dilemmas/dilemmas.json).

**Read [the personas in plain language](profiles/personas_review.md) first.**
For each god, review the behavioral orientation, qualifications, proposed voice,
and the ten original research fields. Note what to keep, change, remove, or
support with a better reference. The voice is an editorial suggestion.

## Files

| File | Purpose |
| --- | --- |
| [Persona review](profiles/personas_review.md) | Readable version of all twelve profiles, with a review checklist |
| [Structured profiles](profiles/olympians.json) | All ten research dimensions and a source-informed pilot persona for each god |
| [JSON Schema](profiles/olympians.schema.json) | Initial structural specification for the JSON profiles |
| [Shared prompt template](profiles/system_prompt_template.md) | Common template for experimenting with a selected pilot persona |
| [Dilemma review](dilemmas/dilemmas_review.md) | All twelve neutral dilemmas, decision questions, and scoring poles |
| [Structured dilemmas](dilemmas/dilemmas.json) | Machine-readable scenarios and presentation instructions |
| [Research review](research/review.md) | Source checks, qualifications, and remaining verification work |
| [Episode records](research/episodes.json) | The 22 original draft evidence episodes |
| `research/framework_original.txt` | Original user-supplied profiling framework |
| `research/sources.json` | Bibliographic metadata and paths to local source copies |
| `scripts/` | Import, extraction, and readable-copy generation utilities |

## Evidence and limitations

The 120 original research fields are marked `unverified_draft`. The separate
pilot personas paraphrase selected inspected secondary-source passages, with
qualifications to avoid turning one episode into a universal rule. They remain
modeling interpretations, not measured psychological properties.

Primary passages, exact quotations, and original secondary page citations still
need individual verification. Different epic, tragic, and cult traditions may
support different portrayals; those differences should remain visible.

The pilot prompt uses `pilot_persona`, not the unchecked original dimensions.
Pilot prompting does not change model weights. Fine-tuning would require a
separate reviewed dataset and an evaluation design.

## References

- Walter Burkert, *Greek Religion* (English translation, 1985).
- Giulia Sissa and Marcel Detienne, *The Daily Life of the Greek Gods* (2000).
- Jan N. Bremmer and Andrew Erskine, eds., *The Gods of Ancient Greece:
  Identities and Transformations* (2010).

The books, extracted book text, and page images remain local and are excluded
by `.gitignore`. Source IDs identify the books; `pdf_pages` are viewer positions
in the local copies, not necessarily printed page numbers. The research notes,
episode records, and scripts are included. Source extraction requires `pypdf`
and your own local copies of the books. The import scripts document the initial
preparation; they are not an LLM training or generation pipeline.

## Next steps

1. Review and revise all twelve personas, including their exceptions and
   differences across sources.
2. Verify supporting passages and freeze a reviewed persona version.
3. Review the twelve neutral dilemmas and their scoring poles, then define the
   neutral judge baseline and response-labeling rubric before collecting results.
4. Run a small prompting pilot with one local model to check clarity and
   consistency; then decide whether to expand the experiment.

The roster follows this project's chosen twelve, including Dionysus; ancient
lists of twelve gods were not all identical.
