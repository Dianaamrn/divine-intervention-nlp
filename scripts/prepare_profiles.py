"""Build research drafts from the supplied framework, retaining provenance.

This is a one-time importer, not a claim that the imported material is verified.
Existing outputs are protected to avoid overwriting later editorial work.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS = {
    'Personality & Temperament': 'personality_temperament',
    'Values & Priorities': 'values_priorities',
    'Decision Patterns': 'decision_patterns',
    'Conflicting Priorities': 'conflicting_priorities',
    'Triggers & Motivations': 'triggers_motivations',
    'Relationships & Partiality': 'relationships_partiality',
    'Methods of Action': 'methods_of_action',
    'Limits & Exceptions': 'limits_exceptions',
    'Communication Style': 'communication_style',
    'Knowledge & Worldview': 'knowledge_worldview',
}

# Paraphrased pilot interpretations of the inspected passages. These are
# operational choices for role play, not measured psychological properties.
CORE = {
 'Zeus': ([179,182,183],
    'Consider sovereignty, existing obligations, hospitality, supplication, and the consequences of a decision for other gods. Personal sympathy may conflict with preserving an established settlement.',
    'Do not assume impartial benevolence or unlimited awareness. Treat fate and divine freedom as a contextual tension, not an automatic physical impossibility.',
    'Commanding and deliberative'),
 'Hera': ([186,189],
    'Attend to marriage, status, and recognition of authority. Consider alliances and indirect leverage when a stronger rival obstructs a goal.',
    'Do not make loyalty to marriage equivalent to universally following rules. Cult traditions and epic disputes require separate contexts.',
    'Assertive and politically attentive'),
 'Poseidon': ([192,193],
    'Attend to recognition of an allotted share of power. Forceful intervention and destructive retaliation are available responses, alongside protection of seafarers and negotiated deference to Zeus.',
    'Do not assume every response must be violent or that he is only a sea god. Do not assign every misfortune of Odysseus to him.',
    'Forceful and attentive to status'),
 'Athena': ([198,199],
    'Favor practical skill, planning, disciplined action, and effective assistance to chosen allies. Restraint and deception can each serve a strategic goal.',
    'Do not turn cunning into impartial moral rationality. Benefits for a favored hero can entail deliberate harm to an opponent.',
    'Clear and strategic'),
 'Apollo': ([205,207,208],
    'Attend to purification, recognition of divine authority, limits of mortal life, and the relationship between destructive and healing powers. Consider atonement and an end to excessive retaliation.',
    'Do not make every answer an oracle or every offense require the same remedy. Apollo can intervene for particular people as well as distance himself from mortal conflicts.',
    'Measured and attentive to limits'),
 'Artemis': ([211,212,213],
    'Attend to hunting, purity, transitions in young lives, and recognition of sacred claims. Protection and danger can coexist within her sphere.',
    'Do not generalize one defeat by Hera into universal helplessness. Epic and cult portrayals differ; she also has civic, healing, and birth-related associations.',
    'Direct and attentive to sacred boundaries'),
 'Ares': ([237,238],
    'Give weight to immediate confrontation, martial force, and a personal response to injury or a child\'s death. His Iliadic portrayal emphasizes destructive conflict and setbacks against Athena.',
    'Do not infer total lack of intelligence, foresight, or affection from an unfavorable literary portrayal. Keep the contrast with Athena specific to the evidence.',
    'Forceful and emotionally immediate'),
 'Aphrodite': ([216,218],
    'Attend to attraction, attachment, persuasion, and the power of desire. Her influence can bind people together or coerce them, and is vulnerable to exposure and counteraction.',
    'Do not assume love is always consensual or benevolent. A battlefield injury does not establish a universal ban on martial associations; civic roles also matter.',
    'Persuasive and attentive to attachment'),
 'Hephaestus': ([236,237],
    'Use craft, constructed solutions, and ingenuity to secure a goal. Humor and mediation can restore a feast, while technical traps can expose betrayal and assert a claim.',
    'Do not infer incapacity for intervention from disability: he uses fire against a river god. Preserve the different marriage traditions rather than combining them into one biography.',
    'Practical and inventive'),
 'Hermes': ([220,222],
    'Consider discreet guidance, communication, disguise, and crossing dangerous boundaries. Cunning may support rescue or negotiation; messenger duties can require delivering an unwelcome command.',
    'Do not make every decision evasive or every relationship friendly. Guiding a living person is not itself evidence of escorting a dead soul.',
    'Adaptable and resourceful'),
 'Demeter': ([224,225,226],
    'Give substantial weight to the mother-daughter bond, loss, recognition, and control of sustenance. Withdrawing a gift can become coercive leverage; a settlement can restore life without undoing the original loss.',
    'Do not assume universal mercy or automatic preference for the vulnerable. Her withdrawal threatens humanity, and a simple seasonal allegory does not exhaust the myth.',
    'Solemn and firm'),
 'Dionysus': ([226,232,233],
    'Attend to recognition of divinity, participation in rites, altered experience, and challenges to established control. Denial can provoke devastating punishment, while recognition can bring favor.',
    'Do not assume every disruption is emancipatory or benevolent. Do not exclude civic or political relevance, or identify all violent frenzy with cannibalism.',
    'Composed and unsettling'),
}

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def build(input_path):
    target = ROOT / 'profiles' / 'olympians.json'
    if target.exists():
        raise FileExistsError('Profiles already exist; edit them directly instead of overwriting reviewed work.')
    raw = input_path.read_text(encoding='utf-8-sig')
    original = ROOT / 'research' / 'framework_original.txt'
    original.parent.mkdir(parents=True, exist_ok=True)
    if original.exists():
        raise FileExistsError(original)
    original.write_text(raw, encoding='utf-8')
    blocks = re.findall(r'^4\.(\d+) (\w+) [^\n]*\n(.*?)(?=^4\.\d+ |^5\. Dual)', raw, re.M | re.S)
    profiles, episodes = [], []
    for number, name, block in blocks:
        slug = name.lower()
        dimensions = {}
        for label, key in DIMENSIONS.items():
            match = re.search(r'^\* ' + re.escape(label) + r': (.+)$', block, re.M)
            if not match:
                raise ValueError(f'Missing {name}: {label}')
            dimensions[key] = {'claim': match.group(1).strip(),
                'provenance': 'user_framework', 'verification_status': 'unverified_draft',
                'evidence_ids': [], 'note': 'A citation in the draft is not an independently checked citation.'}
        episode_ids = []
        found = re.findall(r'^Episode ([^:]+): ([^\n]+)\n(.*?)(?=^Episode |\Z)', block, re.M | re.S)
        for index, (original_id, title, content) in enumerate(found, 1):
            eid = f'{slug}_episode_{index:02d}'
            episode_ids.append(eid)
            fields = {}
            for label in ['Situation','Motivation','Action','Interpretation','Source','Uncertainty']:
                match = re.search(r'^\* ' + label + r': (.+)$', content, re.M)
                if not match:
                    raise ValueError(f'Missing {eid}: {label}')
                fields[label.lower()] = match.group(1).strip()
            episodes.append({'id': eid, 'deity_id': slug, 'original_id': original_id,
                'title': title.strip(), 'draft_fields': fields,
                'primary_text_verification': 'not_performed',
                'quotation_verification': 'not_performed',
                'motivation_evidence_type': 'needs_separate_review',
                'interpretation_evidence_type': 'analyst_inference',
                'training_eligible': False,
                'note': 'Original Explicit labels are retained as draft metadata, not accepted as verification.'})
        pages, behavior, caution, voice = CORE[name]
        evidence = [{'source_id':'burkert_1985', 'pdf_pages':pages,
            'printed_pages': None, 'section': f'III.2 Individual Gods: {name}',
            'verification_scope':'Relevant secondary-source pages inspected; primary texts and draft quotations not independently checked.'}]
        if name in ['Artemis','Hephaestus']:
            is_artemis = name == 'Artemis'
            evidence.append({'source_id':'bremmer_erskine_2010',
                'pdf_pages':[233,234,235] if is_artemis else [217,218],
                'printed_pages':[210,211,212] if is_artemis else [194,195],
                'chapter_author':'Ivana Petrovic' if is_artemis else 'Jan N. Bremmer',
                'section':'Transforming Artemis' if is_artemis else 'Hephaistos Sweats',
                'verification_scope':'Selected chapter pages inspected, not whole chapter.'})
        profiles.append({'id':slug, 'deity_name':name, 'status':'working_draft',
            'tradition_scope':'Epic-centered research profile with selected cult and scholarly qualifications; not a timeless canonical personality.',
            'dimensions':dimensions, 'episode_ids':episode_ids,
            'pilot_persona':{'status':'source_informed_analyst_synthesis',
                'behavioral_orientation':behavior, 'qualifications':caution,
                'voice':{'suggestion':voice, 'evidence_type':'editorial_roleplay_choice'},
                'source_support':evidence},
            'research_gaps':['Check each imported claim against a specific passage.',
                'Check primary episode wording and translators before using quotations.',
                'Add counterexamples and record source-specific variants.',
                'Establish conditional priorities; do not impose a universal ranked value list.']})
    expected = set(x.lower() for x in CORE)
    if len(profiles) != 12 or {p['id'] for p in profiles} != expected:
        raise ValueError('Expected the twelve deities from the agreed roster.')
    data = {'$schema':'./olympians.schema.json','schema_version':'0.1.0',
        'status':'research_draft_with_pilot_personas',
        'methodology':{'source_of_imported_claims':'research/framework_original.txt',
            'no_numeric_personality_scores':True,'no_automatic_fine_tuning_export':True,
            'primary_citations_and_quotations_audited':False,
            'supported_summaries':'Pilot personas paraphrase selected inspected secondary passages; they remain modeling interpretations.'},
        'deities':profiles}
    write_json(target,data)
    write_json(ROOT/'research'/'episodes.json',{'schema_version':'0.1.0','episodes':episodes})
    schema = {'$schema':'https://json-schema.org/draft/2020-12/schema',
        'title':'Olympian research profiles','type':'object',
        'required':['schema_version','status','methodology','deities'],
        'properties':{'schema_version':{'const':'0.1.0'},
            'deities':{'type':'array','minItems':12,'maxItems':12,'items':{
                'type':'object','required':['id','deity_name','status','dimensions','episode_ids','pilot_persona','research_gaps'],
                'properties':{'id':{'enum':sorted(expected)},'status':{'const':'working_draft'},
                    'dimensions':{'type':'object','required':list(DIMENSIONS.values()),
                        'additionalProperties':False,'properties':{k:{'type':'object',
                            'required':['claim','verification_status','provenance','evidence_ids'],
                            'properties':{'claim':{'type':'string','minLength':1},
                                'verification_status':{'enum':['unverified_draft','source_supported','qualified','rejected']},
                                'evidence_ids':{'type':'array','items':{'type':'string'}}}}
                            for k in DIMENSIONS}}}}}}}
    write_json(ROOT/'profiles'/'olympians.schema.json',schema)
    print(f'Created {len(profiles)} profiles, {sum(len(p["dimensions"]) for p in profiles)} imported dimensions, {len(episodes)} episodes.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('framework', type=Path)
    build(parser.parse_args().framework)
