# Review of the Olympian profiling framework

## Assessment

The framework is sufficiently detailed to start building personas. It covers
the agreed ten dimensions and provides episodes for every god. It is a research
draft, not yet a fully verified account of ancient evidence or a training dataset.

The machine-readable version preserves the original material, separates it from
new pilot interpretations, and records the remaining verification work explicitly.
No personality measurements, priority rankings, or model results have been invented.

## What was checked

- All twelve deity sections and their ten dimensions were imported.
- All 22 episodes were imported with new globally unique IDs. The original uses
  `Ar1` and `Ar2` for both Artemis and Ares; the new IDs remove that collision.
- Selected relevant pages in Burkert were read for all twelve gods.
- Selected pages of Petrovic's Artemis chapter and Bremmer's Hephaistos chapter
  were read in the edited collection. Chapter authors are identified separately
  from the volume editors.
- The Sissa/Detienne file is an image scan: extraction produced no searchable
  text. Its contents page was inspected visually. Its substantive passages and
  the draft's page-specific citations have not been checked.
- Ancient texts and translations are not supplied as separate primary sources
  in this folder. Primary episode citations and quotations remain unverified.

The check covers the specified passages, not the three books in their entirety.
PDF page numbers below are one-based viewer positions. Burkert is a reflowed
779-page file: do not substitute these positions for printed book pagination.

## Changes needed before accepting the full profiles

1. **Separate action, motivation, and interpretation.** An action can be explicit
   while its proposed motivation and psychological explanation remain inferred.
   One `Explicit` label for a whole episode obscures that distinction.
2. **Make tendencies conditional.** Words such as `never`, `entirely`, `absolute`,
   and `proves` often claim more than an individual episode establishes.
3. **Keep traditions identifiable.** Epic, tragedy, hymns, and cult evidence need
   source/genre labels. They can describe different divine identities. A general
   research profile can retain these differences without resolving them into a
   single biography.
4. **Avoid imposing a value hierarchy without evidence.** Retain competing
   considerations and their contexts. An ordered list in JSON would otherwise
   quietly become an unsupported universal rule.
5. **Verify quotations against a named translation.** Preserve draft wording in
   the archive; do not treat it as a verified quotation or use it as a training
   target. Page references to secondary sources also need individual checks.
6. **Separate scholarship from model instructions.** Tone suggestions are
   editorial choices. Requiring every god to punish disrespect or always obey
   the same rule about fate would erase the differences under investigation.
7. **Remove the claim that the framework eliminates hallucinations.** Grounding
   improves traceability; fidelity still requires evaluation on new situations.

## Source-supported qualifications for the pilot personas

These are paraphrased modeling interpretations of inspected secondary passages,
not assertions that ancient gods have measurable, fixed psychological traits.

| God | Qualification incorporated into the pilot | Inspected source locator |
| --- | --- | --- |
| Zeus | Authority and obligations can conflict with sympathy; fate is not simply an absolute inability to act. Protection of guests and suppliants uses distinct epithets, Xenios and Hikesios. | Burkert, PDF pp. 179, 182-183 |
| Hera | Marriage and status coexist with subversion and contested power; they do not establish universal obedience to rules. | Burkert, PDF pp. 186, 189 |
| Poseidon | Destructive sea power coexists with protection of seafarers and claims to an allotted share of authority. | Burkert, PDF pp. 192-193 |
| Athena | Cunning, discipline, and aid to chosen heroes can include lethal deception; they do not imply impartial ethical reason. | Burkert, PDF pp. 198-199 |
| Apollo | Healing, purification, destruction, and distance from mortals coexist; neither perpetual neutrality nor perpetual vengeance follows. | Burkert, PDF pp. 205, 207-208 |
| Artemis | One epic humiliation does not define every context; hunting, transitions, birth, healing, and civic roles require distinct treatment. | Burkert, PDF pp. 211-213; Petrovic, printed pp. 210-212 / PDF pp. 233-235 |
| Ares | An unfavorable Iliadic contrast with Athena does not establish total lack of intelligence or attachment. | Burkert, PDF pp. 237-238 |
| Aphrodite | Attraction can involve compulsion; desire also has civic dimensions. A battlefield wound does not establish universal incapacity in every martial tradition. | Burkert, PDF pp. 216, 218 |
| Hephaestus | Technical ingenuity and disability coexist with effective intervention in battle through fire. Different spouse traditions remain separate. | Burkert, PDF pp. 236-237; Bremmer, printed pp. 194-195 / PDF pp. 217-218 |
| Hermes | Guidance, cunning, communication, and messenger duties vary by situation. Escorting living Priam is not itself an episode of escorting a soul after death. | Burkert, PDF pp. 220, 222 |
| Demeter | Maternal grief and restoration coexist with coercion that threatens human survival. Seasonal nature allegory is not an exhaustive interpretation. | Burkert, PDF pp. 224-226 |
| Dionysus | Recognition and ritual participation can bring favor or devastating punishment; disruption does not automatically mean benevolent liberation. | Burkert, PDF pp. 226, 232-233 |

## How to use the files now

`profiles/olympians.json` has two clearly separated components per deity:

- `dimensions`: all ten original research fields, retained as `unverified_draft`.
- `pilot_persona`: a compact source-informed interpretation, source locators,
  qualifications, and an explicitly editorial voice suggestion.

Use the pilot component with `profiles/system_prompt_template.md` for initial
persona prompting. Treat outputs as pilot results. Check and annotate the
individual research claims before upgrading their verification status.

For a checked claim, add an evidence record with a stable ID, source ID, exact
locator, and the observation supporting it; then reference that ID from the
claim. A scholarly interpretation should identify its author. Preserve
counterexamples rather than silently deleting them. `research/episodes.json`
currently retains the user's episode wording and uncertainty labels as draft
metadata only; every episode is excluded from automatic training use.

For eventual fine-tuning, the remaining work includes verified examples, coverage
of varied situations, independently reviewed target responses, and evaluation
cases kept out of training. The current JSON profiles alone are not SFT data.

## Local references

Source filenames and page counts are recorded in `research/sources.json`.

- Walter Burkert, *Greek Religion*, English translation first published 1985;
  the local PDF includes later reprint details.
- Giulia Sissa and Marcel Detienne, *The Daily Life of the Greek Gods*;
  bibliographic year 2000 supplied in the research draft, not checked against the
  scan's copyright page during this pass.
- Jan N. Bremmer and Andrew Erskine, eds., *The Gods of Ancient Greece:
  Identities and Transformations* (2010). Selected chapters: Jan N. Bremmer,
  'Hephaistos Sweats or How to Construct an Ambivalent God'; Ivana Petrovic,
  'Transforming Artemis: from the Goddess of the Outdoors to City Goddess'.
