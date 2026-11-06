"""Create the readable persona review and the README for the initial upload."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = """# Divine Intervention: Can LLMs Be a Good Homer?

An NLP course project investigating whether instructions based on the twelve
Olympian gods change an LLM's stated decisions compared with a neutral judge.

## Current stage: reviewing the personas

The first version contains twelve working profiles: Zeus, Hera, Poseidon, Athena,
Apollo, Artemis, Ares, Aphrodite, Hephaestus, Hermes, Demeter, and Dionysus.
Each has ten research dimensions and a shorter pilot persona for prompting.
No model has been trained or run, and dilemmas have not yet been designed.

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

The books, extracted book text, page images, research archive, and local scripts
are kept outside this initial repository upload. Source IDs in the profiles
identify these books; `pdf_pages` are viewer positions in the local copies,
not necessarily printed page numbers. Original episode IDs and research paths
refer to the local archive, which is not included here.

## Next steps

1. Review and revise all twelve personas, including their exceptions and
   differences across sources.
2. Verify supporting passages and freeze a reviewed persona version.
3. Design a small set of dilemmas and define the neutral judge baseline and
   response-labeling rubric before collecting results.
4. Run a small prompting pilot with one local model to check clarity and
   consistency; then decide whether to expand the experiment.

The roster follows this project's chosen twelve, including Dionysus; ancient
lists of twelve gods were not all identical.
"""

def build():
    data = json.loads((ROOT/'profiles/olympians.json').read_text(encoding='utf-8'))
    lines = ['# Twelve Olympian personas: review copy', '',
        'These are working interpretations for you to review. The pilot summaries draw on selected inspected secondary passages. The ten original research fields below each summary remain unchecked draft claims. Suggested voices are editorial choices.', '',
        'For each god, note what to keep, change, remove, or support with a better reference. A single episode should not become an unconditional rule.', '', '## Contents', '']
    for p in data['deities']:
        lines.append(f"- [{p['deity_name']}](#{p['id']})")
    for p in data['deities']:
        pilot = p['pilot_persona']
        lines.extend(['', f"## {p['deity_name']}", '', '### Pilot persona', '',
            pilot['behavioral_orientation'], '', '**Qualifications:** '+pilot['qualifications'], '',
            '**Suggested voice (editorial):** '+pilot['voice']['suggestion'], '', '### Source support', ''])
        for ref in pilot['source_support']:
            loc = ', '.join(map(str,ref['pdf_pages']))
            printed = '; printed pages '+', '.join(map(str,ref['printed_pages'])) if ref.get('printed_pages') else ''
            author = '; chapter by '+ref['chapter_author'] if 'chapter_author' in ref else ''
            lines.append(f"- `{ref['source_id']}`{author}; local PDF pages {loc}{printed}. Selected passages inspected; primary citations and draft quotations still need checking.")
        lines.extend(['', '### Original research fields: unchecked', ''])
        for key, value in p['dimensions'].items():
            lines.extend(['**'+key.replace('_',' ').capitalize()+'**', '', value['claim'], ''])
        lines.extend(['### Your review', '',
            '- [ ] Behavioral orientation is appropriate.',
            '- [ ] Qualifications and counterexamples are adequate.',
            '- [ ] Values are supported without imposing a universal ranking.',
            '- [ ] Voice fits the intended portrayal.',
            '- [ ] Unsupported or overly absolute claims are flagged.', '',
            '**Keep:**', '', '**Change or remove:**', '',
            '**Additional evidence or different tradition:**', ''])
    (ROOT/'profiles/personas_review.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    (ROOT/'README.md').write_text(README, encoding='utf-8')
    print(f"Created readable review for {len(data['deities'])} gods and repository README.")

if __name__ == '__main__':
    build()
