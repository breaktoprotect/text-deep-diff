from InstructorEmbedding import INSTRUCTOR
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = INSTRUCTOR("hkunlp/instructor-large")

control_objectives = [
    "Limit access to sensitive systems using identity-based controls",
    "Harden system configurations to reduce attack surface",
    "Log and audit user activity on critical infrastructure",
]

control_procedures = [
    "Restrict shell access on Linux servers to specific users",
    "Log all sudo commands executed by users on production hosts",
]

instruction = "Classify the control procedure under the best matching control objective"

# Instructor mode
co_instr = [[instruction, co] for co in control_objectives]
cp_instr = [[instruction, cp] for cp in control_procedures]
co_emb_instr = model.encode(co_instr)
cp_emb_instr = model.encode(cp_instr)
sim_instr = cosine_similarity(cp_emb_instr, co_emb_instr)

# Raw SBERT mode
co_emb_raw = model.encode(control_objectives)
cp_emb_raw = model.encode(control_procedures)
sim_raw = cosine_similarity(cp_emb_raw, co_emb_raw)

# Output
for i, cp in enumerate(control_procedures):
    best_instr = np.argmax(sim_instr[i])
    best_raw = np.argmax(sim_raw[i])
    print(f"CP: {cp}")
    print(
        f"  [INSTRUCTOR] → {control_objectives[best_instr]} (Score: {sim_instr[i][best_instr]:.4f})"
    )
    print(
        f"  [RAW SBERT]  → {control_objectives[best_raw]} (Score: {sim_raw[i][best_raw]:.4f})\n"
    )
