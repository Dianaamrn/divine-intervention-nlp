"""Render the neutral dilemma drafts as a readable Markdown review copy."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def render():
    data = json.loads((ROOT/'dilemmas/dilemmas.json').read_text(encoding='utf-8'))
    lines = ['# Divine Intervention: Twelve Moral Dilemmas', '',
        '**Version 0.1 - drafts for your review.** These are the twelve selected situations, written as neutral disputes. They are fictional adaptations, with no graphic descriptions. No adversarial appeals or divine favoritism have been added.', '',
        '## Shared instruction for the judging god', '', data['shared_judge_instruction'], '',
        '## Contents', '']
    for item in data['dilemmas']:
        anchor = item['id'].lower()+'-'+item['title'].lower().replace("'",'').replace(' ','-')
        lines.append(f"- [{item['id']}: {item['title']}](#{anchor})")
    for item in data['dilemmas']:
        lines.extend(['', f"## {item['id']}: {item['title']}", '', item['neutral_text'], '',
            '**Decision:** '+item['decision_question'], '', '**Research labels - do not show these to the judging model:**', '',
            '- **Pole A:** '+item['poles']['A'], '- **Pole B:** '+item['poles']['B'],
            '- **Main conflict:** '+item['axis'], '', '**Review notes:**', ''])
        lines.extend('- '+note for note in item['review_notes'])
    lines.extend(['', '## What to review before running the experiment', '',
        '- Can you explain each side\'s strongest reason in your own words?',
        '- Are the practical constraints credible, or does an obvious available action dissolve the dispute?',
        '- Are the facts and uncertainties clear without giving away a preferred verdict?',
        '- Does the affected person have a voice, even when someone else is the formal disputant?',
        '- Do any two dilemmas repeat the same conflict too closely?',
        '- Does the prose fit the atmosphere and level of darkness you want?', '',
        'These are candidates, not claims that both sides are equally justified or that readers will split evenly. Their balance must be checked through human review and a pilot.', '',
        'Keep research labels out of model prompts. The presentation order of the two requests should be counterbalanced later. A and B identify the local requests, not a common moral direction across all twelve.', '',
        'After your edits, freeze the neutral texts and their scoring poles together. Then prepare the persuasion variants and experimental plan. These drafts await human review.', ''])
    (ROOT/'dilemmas/dilemmas_review.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f"Rendered {len(data['dilemmas'])} dilemmas.")

if __name__ == '__main__':
    render()
