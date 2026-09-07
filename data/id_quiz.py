from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Literal


BattleStage = Literal["identify", "classify", "cover", "checkpoint"]


@dataclass(frozen=True)
class Choice:
    id: str
    text: str
    feedback: str


@dataclass(frozen=True)
class BattleQuestion:
    id: str
    stage: BattleStage
    topic: str
    prompt: str
    choices: tuple[Choice, Choice, Choice, Choice]
    correct_choice_id: str
    explanation: str
    memory_hook: str
    source_title: str
    source_section: str
    tags: tuple[str, ...]
    difficulty: str = "Foundational"


@dataclass(frozen=True)
class LearningStage:
    id: BattleStage
    title: str
    goal: str


LEARNING_SEQUENCE = (
    LearningStage("identify", "Identify the enemy", "Classify bacteria using Gram stain, shape, arrangement, and key tests."),
    LearningStage("classify", "Know your antimicrobial", "Recall drug class, mechanism target, route, brand/generic name, and Top 250 status."),
    LearningStage("cover", "Choose effective coverage", "Match a named organism and clinical context to course-listed agents of choice."),
    LearningStage("checkpoint", "Mixed checkpoint", "Retrieve identification, drug-family, route, and coverage facts without stage-specific hints."),
)


BACTERIA_SOURCE = "MOST V - Bacteria Identification Fall 2026"
AGENTS_SOURCE = "MOST V - Course Antimicrobial Agents Fall 2026"
ACTIVITY_SOURCE = "MOST V - Common Antibacterial Activity Fall 2026"


ID_QUIZ_01 = (
    BattleQuestion(
        "id-001", "identify", "Gram-positive cocci",
        "The enemy is a Gram-positive coccus in clusters and is coagulase-positive. Identify it.",
        (
            Choice("a", "Staphylococcus aureus", "Correct: the course map places coagulase-positive S. aureus in Gram-positive clusters."),
            Choice("b", "Staphylococcus epidermidis", "S. epidermidis is shown as coagulase-negative."),
            Choice("c", "Streptococcus pneumoniae", "S. pneumoniae is shown among alpha-hemolytic pairs/chains."),
            Choice("d", "Enterococcus faecalis", "E. faecalis is shown among nonhemolytic pairs/chains."),
        ), "a",
        "Gram-positive clusters plus a positive coagulase test points to Staphylococcus aureus.",
        "Aureus adds the plus: S. aureus = coagulase positive.",
        BACTERIA_SOURCE, "Gram-positive bacteria - aerobic cocci - clusters", ("gram-positive", "clusters", "coagulase"),
    ),
    BattleQuestion(
        "id-002", "identify", "Gram-positive cocci",
        "Which organism is mapped as Gram-positive cocci in clusters that are coagulase-negative?",
        (
            Choice("a", "Staphylococcus epidermidis", "Correct: S. epidermidis is the coagulase-negative cluster-forming organism on the map."),
            Choice("b", "Staphylococcus aureus", "S. aureus is coagulase-positive."),
            Choice("c", "Streptococcus pyogenes", "S. pyogenes is beta-hemolytic and arranged in pairs/chains."),
            Choice("d", "Listeria monocytogenes", "Listeria is a Gram-positive bacillus, not a coccus in clusters."),
        ), "a",
        "The course identification tree separates clustered staphylococci with the coagulase test.",
        "Epidermidis is the negative neighbor of aureus.",
        BACTERIA_SOURCE, "Gram-positive bacteria - aerobic cocci - clusters", ("gram-positive", "clusters", "coagulase"),
    ),
    BattleQuestion(
        "id-003", "identify", "Hemolysis",
        "Which organism appears under Gram-positive pairs/chains and alpha-hemolysis?",
        (
            Choice("a", "Streptococcus pneumoniae", "Correct: S. pneumoniae is listed in the alpha-hemolytic branch."),
            Choice("b", "Streptococcus pyogenes", "S. pyogenes is listed under beta-hemolysis."),
            Choice("c", "Enterococcus faecium", "E. faecium is listed under the nonhemolytic branch."),
            Choice("d", "Staphylococcus aureus", "S. aureus is listed in clusters rather than pairs/chains."),
        ), "a",
        "The map places S. pneumoniae and viridans streptococci in the alpha-hemolytic branch.",
        "Alpha: pneumoniae and viridans travel together.",
        BACTERIA_SOURCE, "Gram-positive bacteria - pairs/chains - alpha-hemolytic", ("gram-positive", "alpha-hemolytic", "streptococcus"),
    ),
    BattleQuestion(
        "id-004", "identify", "Hemolysis",
        "Which Group A organism is located in the beta-hemolytic branch?",
        (
            Choice("a", "Streptococcus pyogenes", "Correct: the map labels S. pyogenes as Group A and beta-hemolytic."),
            Choice("b", "Streptococcus agalactiae", "S. agalactiae is beta-hemolytic but is labeled Group B."),
            Choice("c", "Streptococcus pneumoniae", "S. pneumoniae is alpha-hemolytic on this map."),
            Choice("d", "Enterococcus faecalis", "E. faecalis is in the nonhemolytic branch."),
        ), "a",
        "Streptococcus pyogenes is the Group A beta-hemolytic organism in the course tree.",
        "Pyogenes = Group A; agalactiae = Group B.",
        BACTERIA_SOURCE, "Gram-positive bacteria - pairs/chains - beta-hemolytic", ("gram-positive", "beta-hemolytic", "group-a"),
    ),
    BattleQuestion(
        "id-005", "identify", "Gram-negative bacilli",
        "A Gram-negative bacillus is non-lactose-fermenting and oxidase-positive. Which enemy matches?",
        (
            Choice("a", "Pseudomonas aeruginosa", "Correct: the map places P. aeruginosa in the non-lactose-fermenting, oxidase-positive branch."),
            Choice("b", "Escherichia coli", "E. coli appears under lactose-fermenting, oxidase-negative organisms."),
            Choice("c", "Proteus species", "Proteus appears in the non-lactose-fermenting, oxidase-negative branch."),
            Choice("d", "Haemophilus influenzae", "H. influenzae is presented as a coccobacillus."),
        ), "a",
        "Non-lactose fermentation plus oxidase positivity identifies the Pseudomonas branch on the course map.",
        "Pseudomonas stays positive when lactose is negative.",
        BACTERIA_SOURCE, "Gram-negative bacteria - bacilli - non-lactose fermenting", ("gram-negative", "oxidase-positive", "pseudomonas"),
    ),
    BattleQuestion(
        "id-006", "identify", "Atypical bacteria",
        "Which organism is classified as an aerobic atypical bacterium on the course map?",
        (
            Choice("a", "Mycoplasma species", "Correct: Mycoplasma and Chlamydia are shown in the aerobic atypical branch."),
            Choice("b", "Bacteroides", "Bacteroides is shown as a Gram-negative anaerobe."),
            Choice("c", "Listeria monocytogenes", "Listeria is shown as an aerobic Gram-positive bacillus."),
            Choice("d", "Neisseria species", "Neisseria is shown as an aerobic Gram-negative diplococcus."),
        ), "a",
        "The atypical branch contains aerobic Mycoplasma and Chlamydia species.",
        "The atypical pair: Mycoplasma and Chlamydia.",
        BACTERIA_SOURCE, "Atypical bacteria", ("atypical", "aerobic", "mycoplasma"),
    ),
    BattleQuestion(
        "id-007", "classify", "Cephalosporins",
        "Which antimicrobial is a fourth-generation cephalosporin?",
        (
            Choice("a", "Cefepime", "Correct: cefepime is listed in the fourth-generation cephalosporin row."),
            Choice("b", "Cefazolin", "Cefazolin is a first-generation cephalosporin."),
            Choice("c", "Cefuroxime", "Cefuroxime is a second-generation cephalosporin."),
            Choice("d", "Ceftriaxone", "Ceftriaxone is a third-generation cephalosporin."),
        ), "a",
        "The course antimicrobial table places cefepime in the fourth-generation cephalosporin group.",
        "Cefepime = fourth; ceftriaxone = third; cefuroxime = second; cefazolin = first.",
        AGENTS_SOURCE, "Cell wall synthesis - beta-lactams - cephalosporins", ("cephalosporin", "generation", "cell-wall"),
    ),
    BattleQuestion(
        "id-008", "classify", "Beta-lactams",
        "Which drug is the monobactam in the antimicrobial-agent table?",
        (
            Choice("a", "Aztreonam", "Correct: aztreonam is listed under monobactam."),
            Choice("b", "Meropenem", "Meropenem is a carbapenem."),
            Choice("c", "Cefiderocol", "Cefiderocol is listed as a cephalosporin/siderophore."),
            Choice("d", "Amoxicillin", "Amoxicillin is an extended-spectrum penicillin."),
        ), "a",
        "Aztreonam is the monobactam listed in the beta-lactam section.",
        "AZTReonam is the lone monobacTAM.",
        AGENTS_SOURCE, "Cell wall synthesis - beta-lactams - monobactam", ("beta-lactam", "monobactam", "aztreonam"),
    ),
    BattleQuestion(
        "id-009", "classify", "Protein synthesis",
        "Which drug is listed as a 30S tetracycline?",
        (
            Choice("a", "Doxycycline", "Correct: doxycycline is listed in the 30S tetracycline group."),
            Choice("b", "Azithromycin", "Azithromycin is a macrolide in the 50S group."),
            Choice("c", "Linezolid", "Linezolid is a 50S oxazolidinone."),
            Choice("d", "Clindamycin", "Clindamycin is a 50S lincosamide."),
        ), "a",
        "Doxycycline belongs to the tetracyclines acting at the 30S ribosomal subunit.",
        "Tetracyclines take the thirty-S seat.",
        AGENTS_SOURCE, "Protein synthesis - 30S ribosomal subunit - tetracyclines", ("30s", "tetracycline", "doxycycline", "top-250"),
    ),
    BattleQuestion(
        "id-010", "classify", "Protein synthesis",
        "Which antimicrobial is a 50S oxazolidinone?",
        (
            Choice("a", "Linezolid", "Correct: linezolid is listed as a 50S oxazolidinone."),
            Choice("b", "Gentamicin", "Gentamicin is a 30S aminoglycoside."),
            Choice("c", "Doxycycline", "Doxycycline is a 30S tetracycline."),
            Choice("d", "Tigecycline", "Tigecycline is a 30S glycylcycline."),
        ), "a",
        "Linezolid and tedizolid are grouped as 50S oxazolidinones in the course table.",
        "Linezolid lines up at 50S.",
        AGENTS_SOURCE, "Protein synthesis - 50S ribosomal subunit - oxazolidinones", ("50s", "oxazolidinone", "linezolid"),
    ),
    BattleQuestion(
        "id-011", "classify", "Brand and generic",
        "Which generic medication is paired with the brand name Augmentin?",
        (
            Choice("a", "Amoxicillin/clavulanate", "Correct: Augmentin is the listed brand for amoxicillin/clavulanate."),
            Choice("b", "Ampicillin/sulbactam", "Ampicillin/sulbactam is paired with Unasyn."),
            Choice("c", "Piperacillin/tazobactam", "Piperacillin/tazobactam is paired with Zosyn."),
            Choice("d", "Meropenem/vaborbactam", "Meropenem/vaborbactam is paired with Vabomere."),
        ), "a",
        "The table pairs Augmentin with amoxicillin/clavulanate and marks it as a Top 250 medication.",
        "Augment amoxicillin with clavulanate.",
        AGENTS_SOURCE, "Beta-lactam/beta-lactamase inhibitor combinations", ("brand-generic", "augmentin", "top-250", "oral"),
    ),
    BattleQuestion(
        "id-012", "classify", "Route",
        "Which medication is listed as oral and used for CDI only in the infectious-diarrhea section?",
        (
            Choice("a", "Vancomycin", "Correct: oral vancomycin is labeled for CDI only in this section."),
            Choice("b", "Daptomycin", "Daptomycin is listed as intravenous and is not in the CDI-only row."),
            Choice("c", "Polymyxin B", "Polymyxin B is not listed as an oral CDI-only agent."),
            Choice("d", "Gentamicin", "Gentamicin is listed as intravenous and is not a CDI-only therapy in the table."),
        ), "a",
        "In the infectious-diarrhea section, vancomycin is specifically listed as oral for CDI only.",
        "For this course table: CDI vancomycin goes by mouth.",
        AGENTS_SOURCE, "Infectious diarrhea", ("route", "oral", "vancomycin", "cdi", "top-250"),
    ),
    BattleQuestion(
        "id-013", "cover", "MSSA",
        "The enemy is methicillin/oxacillin-sensitive Staphylococcus aureus (MSSA). Which option is a course-listed agent-of-choice category?",
        (
            Choice("a", "First-generation cephalosporin", "Correct: first-generation cephalosporins and anti-staphylococcal penicillins are listed as agents of choice."),
            Choice("b", "Macrolide", "Macrolides are not listed as an MSSA agent-of-choice category in this section."),
            Choice("c", "Fluoroquinolone", "Fluoroquinolones are not listed as an MSSA agent-of-choice category here."),
            Choice("d", "Nitroimidazole", "Metronidazole's category is not listed as an MSSA agent of choice."),
        ), "a",
        "The course activity sheet prioritizes an anti-staphylococcal penicillin or first-generation cephalosporin for MSSA.",
        "MSSA: narrow beta-lactams lead the attack.",
        ACTIVITY_SOURCE, "Gram-positive cocci - MSSA", ("mssa", "staphylococcus", "coverage"),
    ),
    BattleQuestion(
        "id-014", "cover", "MRSA",
        "The enemy is MRSA causing a serious infection. Which drug is listed as an agent of choice?",
        (
            Choice("a", "Vancomycin", "Correct: vancomycin and daptomycin are listed as agents of choice for serious MRSA infection."),
            Choice("b", "Amoxicillin", "Amoxicillin is not listed as an agent of choice for serious MRSA infection."),
            Choice("c", "Penicillin V", "Penicillin V is not listed as an agent of choice for serious MRSA infection."),
            Choice("d", "Nitrofurantoin", "Nitrofurantoin is presented as a urinary-tract agent, not serious MRSA therapy."),
        ), "a",
        "For serious MRSA infection, the sheet lists vancomycin and daptomycin as agents of choice.",
        "Serious MRSA raises the shield: vancomycin or daptomycin.",
        ACTIVITY_SOURCE, "Gram-positive cocci - MRSA - serious infections", ("mrsa", "vancomycin", "coverage"),
    ),
    BattleQuestion(
        "id-015", "cover", "Streptococcus pneumoniae",
        "The enemy is penicillin-susceptible Streptococcus pneumoniae. Which medication is listed as an agent of choice?",
        (
            Choice("a", "Amoxicillin", "Correct: penicillin G, ampicillin, and amoxicillin are listed as agents of choice when susceptible."),
            Choice("b", "Daptomycin", "Daptomycin is not listed in the penicillin-susceptible S. pneumoniae options."),
            Choice("c", "Aztreonam", "Aztreonam is not listed in this organism's course options."),
            Choice("d", "Polymyxin B", "Polymyxin B is not listed in this organism's course options."),
        ), "a",
        "Susceptible S. pneumoniae is matched with penicillin G, ampicillin, or amoxicillin on the course sheet.",
        "Susceptible pneumo stays with the penicillin family.",
        ACTIVITY_SOURCE, "Gram-positive pairs/chains - Streptococcus pneumoniae", ("streptococcus-pneumoniae", "penicillin-susceptible", "coverage"),
    ),
    BattleQuestion(
        "id-016", "cover", "Listeria",
        "Which drug is listed as an agent of choice against Listeria monocytogenes?",
        (
            Choice("a", "Ampicillin", "Correct: penicillin G and ampicillin are listed as agents of choice."),
            Choice("b", "Azithromycin", "Azithromycin is not listed in the Listeria section."),
            Choice("c", "Cefazolin", "Cefazolin is not listed in the Listeria section."),
            Choice("d", "Nitrofurantoin", "Nitrofurantoin is not listed in the Listeria section."),
        ), "a",
        "The sheet lists penicillin G and ampicillin as agents of choice for Listeria.",
        "Listeria likes ampicillin.",
        ACTIVITY_SOURCE, "Gram-positive bacilli - Listeria monocytogenes", ("listeria", "ampicillin", "coverage"),
    ),
    BattleQuestion(
        "id-017", "cover", "Pseudomonas",
        "The enemy is Pseudomonas aeruginosa. Which cephalosporin is listed as an agent of choice?",
        (
            Choice("a", "Cefepime", "Correct: cefepime is listed among the agents of choice for P. aeruginosa."),
            Choice("b", "Cephalexin", "Cephalexin is not listed in the Pseudomonas options."),
            Choice("c", "Cefadroxil", "Cefadroxil is not listed in the Pseudomonas options."),
            Choice("d", "Cefaclor", "Cefaclor is not listed in the Pseudomonas options."),
        ), "a",
        "The course sheet includes cefepime among its agents of choice for Pseudomonas aeruginosa.",
        "Pseudomonas: remember cefepime in the primary lineup.",
        ACTIVITY_SOURCE, "Gram-negative bacilli - Pseudomonas aeruginosa", ("pseudomonas", "cefepime", "coverage"),
    ),
    BattleQuestion(
        "id-018", "cover", "Atypical organisms",
        "Which drug is listed as an agent of choice for Chlamydia pneumoniae and Mycoplasma pneumoniae?",
        (
            Choice("a", "Azithromycin", "Correct: macrolides such as azithromycin and clarithromycin, plus doxycycline, are listed as agents of choice."),
            Choice("b", "Vancomycin", "Vancomycin is not listed in the atypical-organism section."),
            Choice("c", "Cefazolin", "Cefazolin is not listed in the atypical-organism section."),
            Choice("d", "Fosfomycin", "Fosfomycin is not listed in the atypical-organism section."),
        ), "a",
        "The activity sheet lists macrolides and doxycycline as agents of choice for these atypical organisms.",
        "Atypicals: think AZI or DOXY.",
        ACTIVITY_SOURCE, "Atypical organisms", ("atypical", "azithromycin", "doxycycline", "coverage"),
    ),
    BattleQuestion(
        "id-019", "checkpoint", "Integrated identification",
        "A culture clue shows Gram-positive cocci in pairs/chains with nonhemolytic behavior. Which pair belongs to that branch?",
        (
            Choice("a", "Enterococcus faecium and Enterococcus faecalis", "Correct: both Enterococcus species are shown in the nonhemolytic branch."),
            Choice("b", "Staphylococcus aureus and Staphylococcus epidermidis", "These organisms are placed in clusters."),
            Choice("c", "Streptococcus pyogenes and Streptococcus agalactiae", "These organisms are placed in the beta-hemolytic branch."),
            Choice("d", "Streptococcus pneumoniae and viridans streptococci", "These organisms are placed in the alpha-hemolytic branch."),
        ), "a",
        "The nonhemolytic pairs/chains branch contains E. faecium and E. faecalis.",
        "Nonhemolytic pairs/chains point to the Enterococcus pair.",
        BACTERIA_SOURCE, "Gram-positive bacteria - pairs/chains - nonhemolytic", ("enterococcus", "nonhemolytic", "checkpoint"),
    ),
    BattleQuestion(
        "id-020", "checkpoint", "Integrated classification",
        "Which complete match is correct according to the antimicrobial-agent table?",
        (
            Choice("a", "Gentamicin - 30S aminoglycoside - IV", "Correct: all three features match the table."),
            Choice("b", "Linezolid - 30S tetracycline - PO only", "Linezolid is a 50S oxazolidinone and is listed as IV and PO."),
            Choice("c", "Daptomycin - glycopeptide - PO", "Daptomycin is a lipopeptide and is listed as IV."),
            Choice("d", "Rifampin - folate synthesis inhibitor - topical only", "Rifampin is listed under RNA synthesis and as IV/PO."),
        ), "a",
        "Gentamicin is listed as an intravenous aminoglycoside acting at the 30S ribosomal subunit.",
        "Gentamicin: aminoglycoside, thirty-S, IV.",
        AGENTS_SOURCE, "Protein synthesis - 30S ribosomal subunit - aminoglycosides", ("gentamicin", "30s", "route", "checkpoint", "top-250"),
    ),
    BattleQuestion(
        "id-021", "checkpoint", "Brand and generic",
        "Which brand/generic pairing is correct?",
        (
            Choice("a", "Zosyn - piperacillin/tazobactam", "Correct: Zosyn is paired with piperacillin/tazobactam."),
            Choice("b", "Unasyn - amoxicillin/clavulanate", "Unasyn is paired with ampicillin/sulbactam."),
            Choice("c", "Bactrim - nitrofurantoin", "Bactrim is paired with trimethoprim/sulfamethoxazole."),
            Choice("d", "Macrobid - fosfomycin", "Macrobid is a listed brand for nitrofurantoin."),
        ), "a",
        "The antimicrobial table pairs Zosyn with piperacillin/tazobactam.",
        "Zosyn = PIP/TAZO.",
        AGENTS_SOURCE, "Beta-lactam/beta-lactamase inhibitor combinations", ("brand-generic", "zosyn", "checkpoint", "top-250"),
    ),
    BattleQuestion(
        "id-022", "checkpoint", "Coverage distinction",
        "Which statement correctly distinguishes the course-listed MRSA categories?",
        (
            Choice("a", "Doxycycline is listed for MRSA SSTI/CAP; vancomycin is listed for serious MRSA infection.", "Correct: this matches the two MRSA subsections."),
            Choice("b", "Amoxicillin is listed for serious MRSA; nitrofurantoin is listed for MRSA CAP.", "Neither pairing appears in the MRSA subsections."),
            Choice("c", "Penicillin V is listed for MRSA SSTI; cefadroxil is listed for serious MRSA.", "Neither pairing appears in the MRSA subsections."),
            Choice("d", "Metronidazole is listed for MRSA SSTI; rifaximin is listed for serious MRSA.", "These drugs are not listed in the MRSA subsections."),
        ), "a",
        "The course sheet separates MRSA SSTI/CAP options from agents used for serious MRSA infections.",
        "Context changes the weapon: doxy for the listed SSTI/CAP group, vancomycin for serious infection.",
        ACTIVITY_SOURCE, "Gram-positive cocci - MRSA", ("mrsa", "context", "checkpoint"),
    ),
    BattleQuestion(
        "id-023", "checkpoint", "Restriction",
        "Which agent carries the course-sheet reminder 'cystitis only' when used as an Enterococcus faecalis UTI alternative?",
        (
            Choice("a", "Nitrofurantoin", "Correct: nitrofurantoin is marked cystitis only in this context."),
            Choice("b", "Ampicillin", "Ampicillin is listed as an agent of choice, without that reminder."),
            Choice("c", "Amoxicillin", "Amoxicillin is listed as an agent of choice, without that reminder."),
            Choice("d", "Fosfomycin", "Fosfomycin is listed as an alternative, but the parenthetical reminder is attached to nitrofurantoin."),
        ), "a",
        "For E. faecalis UTI, nitrofurantoin is listed as an alternative with the limitation 'cystitis only.'",
        "Nitrofurantoin stays low: cystitis only.",
        ACTIVITY_SOURCE, "Enterococcus faecalis - urinary tract infections", ("enterococcus", "nitrofurantoin", "cystitis", "checkpoint"),
    ),
    BattleQuestion(
        "id-024", "checkpoint", "Mechanism",
        "Which mechanism-target pairing is correct according to the course antimicrobial table?",
        (
            Choice("a", "Rifampin - RNA synthesis", "Correct: rifampin is listed in the RNA-synthesis section."),
            Choice("b", "Ciprofloxacin - folate synthesis", "Ciprofloxacin is listed with the DNA-synthesis agents."),
            Choice("c", "Trimethoprim/sulfamethoxazole - cell membrane", "TMP/SMX is listed under folate synthesis."),
            Choice("d", "Vancomycin - 50S protein synthesis", "Vancomycin is listed under cell-wall synthesis."),
        ), "a",
        "Rifampin is the rifamycin shown under RNA synthesis.",
        "RIF writes on RNA.",
        AGENTS_SOURCE, "RNA synthesis - rifamycin", ("mechanism", "rifampin", "checkpoint"),
    ),
)


QUESTIONS_BY_ID = {question.id: question for question in ID_QUIZ_01}


def questions_for_stage(stage: BattleStage) -> tuple[BattleQuestion, ...]:
    return tuple(question for question in ID_QUIZ_01 if question.stage == stage)


def display_choices(question: BattleQuestion) -> tuple[Choice, Choice, Choice, Choice]:
    """Return a stable per-question order so answers do not move across reruns."""
    return tuple(sorted(
        question.choices,
        key=lambda choice: hashlib.sha256(f"{question.id}:{choice.id}".encode()).digest(),
    ))
