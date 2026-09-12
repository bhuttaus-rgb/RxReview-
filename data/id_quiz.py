from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Literal


BattleStage = Literal["identify", "classify", "mechanism", "cover", "brand"]


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
    LearningStage("classify", "Classify the antimicrobial", "Match antimicrobial agents to their drug classes."),
    LearningStage("mechanism", "Find the target", "Match antimicrobial agents and classes to their cellular targets and mechanisms."),
    LearningStage("cover", "Choose effective coverage", "Match a named organism and clinical context to course-listed agents of choice."),
    LearningStage("brand", "Match brand and generic", "Recall both directions for the starred Top 250 brand and generic names."),
)


BACTERIA_SOURCE = "MOST V - Bacteria Identification Fall 2026"
AGENTS_SOURCE = "MOST V - Course Antimicrobial Agents Fall 2026"
ACTIVITY_SOURCE = "MOST V - Common Antibacterial Activity Fall 2026"
TOP250_SOURCE = "PHM 516 Top 250 LIST_2026"


# Only entries marked with an asterisk in the professor's Top 250 document.
# An empty brand tuple means the source document does not list a brand name.
STARRED_BRAND_PAIRS = (
    ("Penicillin VK", ("Veetids",)),
    ("Penicillin G", ("Pfizerpen",)),
    ("Penicillin G benzathine", ("Bicillin L-A",)),
    ("Penicillin G procaine", ()),
    ("Amoxicillin", ("Amoxil", "Moxatag")),
    ("Cephalexin", ("Keflex",)),
    ("Cefuroxime", ("Ceftin", "Zinacef")),
    ("Ceftriaxone", ()),
    ("Cefdinir", ("Omnicef",)),
    ("Amoxicillin/clavulanate", ("Augmentin",)),
    ("Piperacillin/tazobactam", ("Zosyn",)),
    ("Vancomycin", ("Firvanq", "Vancocin")),
    ("Bacitracin/neomycin/polymyxin B/trimethoprim", ("Neosporin", "Polytrim")),
    ("Gentamicin", ()),
    ("Doxycycline", ("Vibramycin", "Doxy 100")),
    ("Minocycline", ("Minocin",)),
    ("Erythromycin", ("Ery-Tab",)),
    ("Azithromycin", ("Zithromax", "Z-Pak")),
    ("Clarithromycin", ("Biaxin",)),
    ("Fidaxomicin", ("Dificid",)),
    ("Clindamycin", ("Cleocin",)),
    ("Trimethoprim/sulfamethoxazole", ("Bactrim", "Septra")),
    ("Metronidazole", ("Flagyl",)),
    ("Mupirocin", ("Bactroban",)),
    ("Nitrofurantoin", ("Macrobid", "Macrodantin")),
    ("Chlorhexidine", ("Peridex", "Periogard", "Hibiclens", "Paroex")),
    ("Levofloxacin", ("Levaquin",)),
    ("Ciprofloxacin", ("Cipro", "Cipro XR")),
    ("Ciprofloxacin - otic products", ("Cipro HC Otic", "Cetraxal")),
    ("Moxifloxacin", ("Avelox", "Vigamox", "Moxeza")),
    ("Gatifloxacin", ("Zymaxid", "Zymar")),
    ("Rifaximin", ("Xifaxan",)),
    ("Acyclovir", ("Zovirax",)),
    ("Oseltamivir", ("Tamiflu",)),
    ("Nirmatrelvir/ritonavir", ("Paxlovid",)),
    ("COVID-19 mRNA vaccine", ("Comirnaty", "Spikevax")),
    ("Influenza virus vaccine", ("Fluzone", "Afluria", "Fluad", "Flublok", "FluLaval", "Fluarix", "Flucelvax")),
    ("Haemophilus influenzae type B vaccine", ("PedvaxHIB", "Hiberix", "ActHIB")),
    ("Pneumococcal vaccines", ("Prevnar 13", "Pneumovax 23", "Vaxneuvance", "Prevnar 20", "Capvaxive")),
    ("Meningococcal vaccines", ("MenQuadfi", "Menveo", "Trumenba", "Bexsero", "Penbraya")),
    ("Respiratory syncytial virus vaccines", ("mResvia", "Abrysvo", "Arexvy")),
    ("Phenazopyridine", ("Pyridium", "AZO", "Uristat", "Baridium")),
)


CORE_QUESTIONS = (
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
        "id-009", "mechanism", "Protein synthesis",
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
        "id-010", "mechanism", "Protein synthesis",
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
        "id-011", "brand", "Brand and generic",
        "Which generic medication is paired with the brand name Augmentin?",
        (
            Choice("a", "Amoxicillin/clavulanate", "Correct: Augmentin is the listed brand for amoxicillin/clavulanate."),
            Choice("b", "Ampicillin/sulbactam", "Ampicillin/sulbactam is paired with Unasyn."),
            Choice("c", "Piperacillin/tazobactam", "Piperacillin/tazobactam is paired with Zosyn."),
            Choice("d", "Meropenem/vaborbactam", "Meropenem/vaborbactam is paired with Vabomere."),
        ), "a",
        "The table pairs Augmentin with amoxicillin/clavulanate and marks it as a Top 250 medication.",
        "Augment amoxicillin with clavulanate.",
        AGENTS_SOURCE, "Beta-lactam/beta-lactamase inhibitor combinations", ("brand-generic", "augmentin", "top-250"),
    ),
    BattleQuestion(
        "id-012", "mechanism", "Cell wall synthesis",
        "Which antimicrobial is classified as a glycopeptide in the cell-wall synthesis section?",
        (
            Choice("a", "Vancomycin", "Correct: vancomycin is listed as a glycopeptide that inhibits cell-wall synthesis."),
            Choice("b", "Daptomycin", "Daptomycin is a lipopeptide that acts at the cell membrane."),
            Choice("c", "Polymyxin B", "Polymyxin B is a polypeptide that acts at the cell membrane."),
            Choice("d", "Gentamicin", "Gentamicin is an aminoglycoside that acts at the 30S ribosomal subunit."),
        ), "a",
        "Vancomycin is the glycopeptide listed under cell-wall synthesis in the course table.",
        "VAN builds a wall: vancomycin = glycopeptide cell-wall inhibitor.",
        AGENTS_SOURCE, "Cell wall synthesis - glycopeptides", ("glycopeptide", "vancomycin", "cell-wall", "top-250"),
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
        "id-019", "identify", "Integrated identification",
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
        "id-020", "mechanism", "Integrated classification",
        "Which drug, ribosomal target, and antimicrobial class are correctly matched?",
        (
            Choice("a", "Gentamicin - 30S - aminoglycoside", "Correct: all three features match the table."),
            Choice("b", "Linezolid - 30S - tetracycline", "Linezolid is a 50S oxazolidinone."),
            Choice("c", "Daptomycin - cell wall - glycopeptide", "Daptomycin is a lipopeptide that acts at the cell membrane."),
            Choice("d", "Rifampin - folate synthesis - sulfonamide", "Rifampin is a rifamycin listed under RNA synthesis."),
        ), "a",
        "Gentamicin is listed as an aminoglycoside acting at the 30S ribosomal subunit.",
        "Gentamicin: aminoglycoside at thirty-S.",
        AGENTS_SOURCE, "Protein synthesis - 30S ribosomal subunit - aminoglycosides", ("gentamicin", "30s", "checkpoint", "top-250"),
    ),
    BattleQuestion(
        "id-021", "brand", "Brand and generic",
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
        "id-022", "cover", "Coverage distinction",
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
        "id-023", "cover", "Enterococcus faecalis",
        "The enemy is Enterococcus faecalis causing a urinary tract infection. Which medication is listed as an agent of choice?",
        (
            Choice("a", "Ampicillin", "Correct: ampicillin and amoxicillin are listed as agents of choice for this infection."),
            Choice("b", "Azithromycin", "Azithromycin is not listed as an agent of choice for this infection."),
            Choice("c", "Cefazolin", "Cefazolin is not listed as an agent of choice for this infection."),
            Choice("d", "Metronidazole", "Metronidazole is not listed as an agent of choice for this infection."),
        ), "a",
        "For an Enterococcus faecalis urinary tract infection, the course sheet lists ampicillin or amoxicillin as agents of choice.",
        "E. faecalis UTI: AMP up with ampicillin or amoxicillin.",
        ACTIVITY_SOURCE, "Enterococcus faecalis - urinary tract infections", ("enterococcus", "ampicillin", "amoxicillin", "agent-of-choice", "checkpoint"),
    ),
    BattleQuestion(
        "id-024", "mechanism", "Mechanism",
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


def _brand_text(brands: tuple[str, ...]) -> str:
    return ", ".join(brands)


def _build_brand_questions() -> tuple[BattleQuestion, ...]:
    """Build one grounded recall question for each testable, non-duplicate pair."""
    testable = [pair for pair in STARRED_BRAND_PAIRS if pair[1]]
    already_tested = {"Amoxicillin/clavulanate", "Piperacillin/tazobactam"}
    generated: list[BattleQuestion] = []
    for index, (generic, brands) in enumerate(testable):
        if generic in already_tested:
            continue
        distractors = [testable[(index + offset) % len(testable)] for offset in (1, 2, 3)]
        brand_names = _brand_text(brands)
        if index % 2 == 0:
            prompt = f"Which brand name or brand-name group matches {generic}?"
            correct_text = brand_names
            wrong_texts = [_brand_text(item_brands) for _, item_brands in distractors]
        else:
            prompt = f"Which generic entry matches the brand name(s) {brand_names}?"
            correct_text = generic
            wrong_texts = [item_generic for item_generic, _ in distractors]
        choices = (
            Choice("a", correct_text, f"Correct: {generic} is paired with {brand_names} on the starred Top 250 list."),
            Choice("b", wrong_texts[0], f"This does not match {generic}; the listed brand pairing is {brand_names}."),
            Choice("c", wrong_texts[1], f"This does not match {generic}; the listed brand pairing is {brand_names}."),
            Choice("d", wrong_texts[2], f"This does not match {generic}; the listed brand pairing is {brand_names}."),
        )
        generated.append(BattleQuestion(
            f"brand-{index + 1:03d}", "brand", "Brand and generic", prompt, choices, "a",
            f"The starred Top 250 list pairs {generic} with {brand_names}.",
            f"{generic} ↔ {brand_names}", TOP250_SOURCE, "Starred Top 250 entries",
            ("brand-generic", "top-250", "starred"),
        ))
    return tuple(generated)


SUPPLEMENTAL_FACTS = (
    # Classification
    ("class-001", "classify", "Penicillins", "Which class contains Penicillin VK?", "Beta-lactam penicillin", ("Macrolide", "Aminoglycoside", "Fluoroquinolone"), "Penicillin VK is a beta-lactam penicillin.", "Penicillin names its own beta-lactam family.", AGENTS_SOURCE, "Cell wall synthesis - beta-lactams - penicillins"),
    ("class-002", "classify", "Combination agents", "How is piperacillin/tazobactam classified?", "Beta-lactam/beta-lactamase inhibitor combination", ("Glycopeptide", "Lipopeptide", "Oxazolidinone"), "Piperacillin/tazobactam combines a beta-lactam with a beta-lactamase inhibitor.", "PIP/TAZO = beta-lactam plus protector.", AGENTS_SOURCE, "Beta-lactam/beta-lactamase inhibitor combinations"),
    ("class-003", "classify", "Glycopeptides", "Which class contains vancomycin?", "Glycopeptide", ("Lipopeptide", "Polypeptide", "Macrolide"), "Vancomycin is classified as a glycopeptide.", "VAN carries the glycopeptide shield.", AGENTS_SOURCE, "Cell wall synthesis - glycopeptides"),
    ("class-004", "classify", "Lipopeptides", "Which class contains daptomycin?", "Lipopeptide", ("Glycopeptide", "Tetracycline", "Rifamycin"), "Daptomycin is classified as a lipopeptide.", "DAPTO = lipopeptide.", AGENTS_SOURCE, "Cell membrane - lipopeptides"),
    ("class-005", "classify", "Aminoglycosides", "Which class contains gentamicin?", "Aminoglycoside", ("Macrolide", "Lincosamide", "Oxazolidinone"), "Gentamicin is classified as an aminoglycoside.", "Gentamicin joins the amino-glycosides.", AGENTS_SOURCE, "Protein synthesis - 30S - aminoglycosides"),
    ("class-006", "classify", "Tetracyclines", "Which class contains doxycycline?", "Tetracycline", ("Macrolide", "Fluoroquinolone", "Glycopeptide"), "Doxycycline is classified as a tetracycline.", "DOXY cycles with the tetracyclines.", AGENTS_SOURCE, "Protein synthesis - 30S - tetracyclines"),
    ("class-007", "classify", "Macrolides", "Which class contains azithromycin?", "Macrolide", ("Aminoglycoside", "Lincosamide", "Rifamycin"), "Azithromycin is classified as a macrolide.", "The -thromycin trio belongs to macrolides.", AGENTS_SOURCE, "Protein synthesis - 50S - macrolides"),
    ("class-008", "classify", "Lincosamides", "Which class contains clindamycin?", "Lincosamide", ("Oxazolidinone", "Tetracycline", "Fluoroquinolone"), "Clindamycin is classified as a lincosamide.", "CLINDA links to lincosamide.", AGENTS_SOURCE, "Protein synthesis - 50S - lincosamides"),
    ("class-009", "classify", "Oxazolidinones", "Which class contains linezolid?", "Oxazolidinone", ("Macrolide", "Aminoglycoside", "Glycopeptide"), "Linezolid is classified as an oxazolidinone.", "LINEZOLID lines up with oxazolidinones.", AGENTS_SOURCE, "Protein synthesis - 50S - oxazolidinones"),
    ("class-010", "classify", "Fluoroquinolones", "Which class contains ciprofloxacin?", "Fluoroquinolone", ("Rifamycin", "Nitroimidazole", "Sulfonamide"), "Ciprofloxacin is classified as a fluoroquinolone.", "The -floxacin ending signals fluoroquinolone.", AGENTS_SOURCE, "DNA synthesis - fluoroquinolones"),
    # Mechanism and target
    ("mech-001", "mechanism", "Cell wall", "What is the primary target category of penicillins?", "Cell wall synthesis", ("Cell membrane", "DNA synthesis", "Folate synthesis"), "Penicillins inhibit bacterial cell wall synthesis.", "Penicillins break the wall.", AGENTS_SOURCE, "Cell wall synthesis - penicillins"),
    ("mech-002", "mechanism", "Cell wall", "What is the primary target category of carbapenems?", "Cell wall synthesis", ("RNA synthesis", "30S protein synthesis", "Cell membrane"), "Carbapenems are beta-lactams that inhibit cell wall synthesis.", "Carbapenems crack the wall.", AGENTS_SOURCE, "Cell wall synthesis - carbapenems"),
    ("mech-003", "mechanism", "Cell membrane", "What is the primary target category of daptomycin?", "Cell membrane", ("Cell wall synthesis", "DNA synthesis", "Folate synthesis"), "Daptomycin acts at the bacterial cell membrane.", "DAPTO disrupts the membrane.", AGENTS_SOURCE, "Cell membrane - lipopeptides"),
    ("mech-004", "mechanism", "30S", "Which ribosomal subunit is targeted by gentamicin?", "30S", ("50S", "DNA gyrase", "RNA polymerase"), "Gentamicin is an aminoglycoside that acts at the 30S subunit.", "Aminoglycosides aim at thirty-S.", AGENTS_SOURCE, "Protein synthesis - 30S - aminoglycosides"),
    ("mech-005", "mechanism", "50S", "Which ribosomal subunit is targeted by azithromycin?", "50S", ("30S", "Cell membrane", "Folate pathway"), "Azithromycin is a macrolide that acts at the 50S subunit.", "Macrolides march to fifty-S.", AGENTS_SOURCE, "Protein synthesis - 50S - macrolides"),
    ("mech-006", "mechanism", "DNA synthesis", "Which target category is associated with ciprofloxacin?", "DNA synthesis", ("RNA synthesis", "Cell wall synthesis", "50S protein synthesis"), "Ciprofloxacin is listed among DNA-synthesis inhibitors.", "CIPRO clips DNA replication.", AGENTS_SOURCE, "DNA synthesis - fluoroquinolones"),
    ("mech-007", "mechanism", "RNA synthesis", "Which target category is associated with rifampin?", "RNA synthesis", ("DNA synthesis", "Folate synthesis", "Cell membrane"), "Rifampin is a rifamycin that inhibits RNA synthesis.", "RIF writes on RNA.", AGENTS_SOURCE, "RNA synthesis - rifamycins"),
    # Identification
    ("identify-001", "identify", "Group B Streptococcus", "Which organism is Group B and beta-hemolytic?", "Streptococcus agalactiae", ("Streptococcus pyogenes", "Streptococcus pneumoniae", "Enterococcus faecalis"), "S. agalactiae is the Group B beta-hemolytic streptococcus.", "Agalactiae = Group B.", BACTERIA_SOURCE, "Gram-positive pairs/chains - beta-hemolytic"),
    ("identify-002", "identify", "Gram-positive bacilli", "Which organism is an aerobic Gram-positive bacillus?", "Listeria monocytogenes", ("Neisseria species", "Bacteroides species", "Mycoplasma species"), "Listeria monocytogenes is placed among aerobic Gram-positive bacilli.", "Listeria = positive aerobic rod.", BACTERIA_SOURCE, "Gram-positive bacteria - aerobic bacilli"),
    ("identify-003", "identify", "Enteric bacilli", "Which organism is Gram-negative, lactose-fermenting, and oxidase-negative?", "Escherichia coli", ("Pseudomonas aeruginosa", "Neisseria species", "Bacteroides species"), "E. coli is in the lactose-fermenting, oxidase-negative Gram-negative bacillus branch.", "E. coli ferments lactose but stays oxidase negative.", BACTERIA_SOURCE, "Gram-negative bacilli - lactose fermenting"),
    ("identify-004", "identify", "Enteric bacilli", "Where does Enterobacter species belong on the course identification map?", "Gram-negative lactose-fermenting oxidase-negative bacilli", ("Gram-positive aerobic bacilli", "Gram-negative oxidase-positive nonfermenters", "Aerobic atypical bacteria"), "Enterobacter is mapped as Gram-negative, lactose-fermenting, oxidase-negative bacilli.", "Enterobacter enters the lactose-positive, oxidase-negative branch.", BACTERIA_SOURCE, "Gram-negative bacilli - lactose fermenting"),
    ("identify-005", "identify", "Diplococci", "Which organism is classified as an aerobic Gram-negative diplococcus?", "Neisseria species", ("Listeria monocytogenes", "Staphylococcus aureus", "Mycoplasma species"), "Neisseria is placed among aerobic Gram-negative diplococci.", "Neisseria = negative diplococci.", BACTERIA_SOURCE, "Gram-negative bacteria - aerobic diplococci"),
    # Reverse coverage recall
    ("cover-001", "cover", "MSSA", "First-generation cephalosporins are course-listed agents of choice for which enemy?", "MSSA", ("Serious MRSA infection", "Pseudomonas aeruginosa", "Atypical pneumonia"), "First-generation cephalosporins are listed as agents of choice for MSSA.", "First-generation cephalosporin → MSSA.", ACTIVITY_SOURCE, "Gram-positive cocci - MSSA"),
    ("cover-002", "cover", "MRSA", "Vancomycin is course-listed as an agent of choice for which serious infection?", "Serious MRSA infection", ("Penicillin-susceptible S. pneumoniae", "Atypical pneumonia", "Uncomplicated cystitis only"), "Vancomycin is listed as an agent of choice for serious MRSA infection.", "Serious MRSA raises the vancomycin shield.", ACTIVITY_SOURCE, "Gram-positive cocci - MRSA - serious infections"),
    ("cover-003", "cover", "Listeria", "Ampicillin is course-listed as an agent of choice for which organism?", "Listeria monocytogenes", ("Pseudomonas aeruginosa", "MRSA", "Mycoplasma pneumoniae"), "Ampicillin is listed as an agent of choice for Listeria monocytogenes.", "Listeria likes ampicillin.", ACTIVITY_SOURCE, "Gram-positive bacilli - Listeria monocytogenes"),
    ("cover-004", "cover", "Pseudomonas", "Cefepime is course-listed as an agent of choice for which Gram-negative enemy?", "Pseudomonas aeruginosa", ("Bacteroides species", "Chlamydia pneumoniae", "Enterococcus faecalis"), "Cefepime is included among agents of choice for Pseudomonas aeruginosa.", "Pseudomonas → cefepime in the primary lineup.", ACTIVITY_SOURCE, "Gram-negative bacilli - Pseudomonas aeruginosa"),
)


def _build_supplemental_questions() -> tuple[BattleQuestion, ...]:
    return tuple(BattleQuestion(
        question_id, stage, topic, prompt,
        (Choice("a", correct, f"Correct: {explanation}"),
         Choice("b", distractors[0], f"This does not fit. {explanation}"),
         Choice("c", distractors[1], f"This does not fit. {explanation}"),
         Choice("d", distractors[2], f"This does not fit. {explanation}")),
        "a", explanation, hook, source, section, (stage, "id-fundamentals")
    ) for question_id, stage, topic, prompt, correct, distractors, explanation, hook, source, section in SUPPLEMENTAL_FACTS)


ID_QUIZ_01 = CORE_QUESTIONS + _build_supplemental_questions() + _build_brand_questions()


QUESTIONS_BY_ID = {question.id: question for question in ID_QUIZ_01}


def questions_for_stage(stage: BattleStage) -> tuple[BattleQuestion, ...]:
    return tuple(question for question in ID_QUIZ_01 if question.stage == stage)


def display_questions(attempt_seed: int = 0) -> tuple[BattleQuestion, ...]:
    """Shuffle questions within each learning stage for one quiz attempt."""
    ordered_questions: list[BattleQuestion] = []
    for stage in LEARNING_SEQUENCE:
        ordered_questions.extend(sorted(
            questions_for_stage(stage.id),
            key=lambda question: hashlib.sha256(
                f"{attempt_seed}:{stage.id}:{question.id}".encode()
            ).digest(),
        ))
    return tuple(ordered_questions)


def simulation_questions(attempt_seed: int = 0, per_stage: int = 12) -> tuple[BattleQuestion, ...]:
    """Draw a balanced, fully shuffled ID Fundamentals quiz simulation."""
    selected: list[BattleQuestion] = []
    for stage in LEARNING_SEQUENCE:
        candidates = [question for question in display_questions(attempt_seed) if question.stage == stage.id]
        if len(candidates) < per_stage:
            raise ValueError(f"Not enough {stage.id} questions for a balanced simulation")
        selected.extend(candidates[:per_stage])
    return tuple(sorted(
        selected,
        key=lambda question: hashlib.sha256(
            f"simulation:{attempt_seed}:{question.id}".encode()
        ).digest(),
    ))


def display_choices(question: BattleQuestion, attempt_seed: int = 0) -> tuple[Choice, Choice, Choice, Choice]:
    """Return a shuffled order that stays stable for one quiz attempt."""
    return tuple(sorted(
        question.choices,
        key=lambda choice: hashlib.sha256(
            f"{attempt_seed}:{question.id}:{choice.id}".encode()
        ).digest(),
    ))
