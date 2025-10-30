# 🧭 Project Overview

**Title:** Quantum Key Distribution using the BB84 Protocol

**Goal:** Implement, simulate, and analyze the BB84 quantum key distribution algorithm to understand quantum cryptographic security, eavesdropping detection (via QBER), and key reconciliation.

**Outcome:** A working BB84 simulation (in Python or Qiskit), a brief report, and a presentation explaining your results and findings.

# 📅 5-Week Project Structure
## Week 1: Background & Setup

### Objective: Understand the theory and prepare the environment.

### Topics:

- Review quantum bits (qubits), superposition, and measurement.

- Study BB84 protocol steps: encoding, transmission, measurement, and key sifting.

- Learn about Quantum Key Distribution (QKD) and why it’s secure.

- Review eavesdropping and QBER (Quantum Bit Error Rate).

### Deliverables:

- A short summary (1–2 pages) explaining BB84.

- Project environment ready.

### Tools to Set Up:

- Python 3.x

- Jupyter Notebook or VS Code

### Libraries:
- numpy, matplotlib, pandas, hashlib, qiskit (optional, for quantum simulation)

### Optional: GitHub repo for version control.

## Week 2: Basic BB84 Simulation

### Objective: Implement a simple classical simulation of BB84.

### Tasks:

### Write code to:

- Generate random bits and bases for Alice.

- Randomly choose Bob’s bases.

- Compare bases to get a “raw key”.

- ompute QBER when no eavesdropper is present.

### Deliverables:

- Working simulation script (bb84_sim.py or notebook).

- Visualization: raw vs sifted key length, sample bases.

### Tools:

- Python + NumPy for random generation and array logic.

- Matplotlib for plots.

## Week 3: Eavesdropping Simulation

### Objective: Add an intercept-resend attack model and measure QBER.

### Tasks:

- Simulate Eve intercepting with a certain probability.

- Plot QBER vs. Eve’s intercept probability.

- Add optional channel noise.

### Deliverables:

- A notebook or report section showing QBER increase with Eve’s activity.

- Visual plot like this:
QBER (%) vs. Eavesdrop Probability.

### Tools:

- Continue using Python/NumPy/Matplotlib.

- Use pandas to log and analyze simulation results.

## Week 4: Key Sifting & Privacy Amplification

### Objective: Demonstrate realistic post-processing of the key.

### Tasks:

- Implement basis reconciliation (keep matching bases).

- Implement sampling to estimate QBER.

- Apply a simple privacy amplification step (e.g., hash function).

- Optionally, explore error correction (e.g., parity bits).

### Deliverables:

- A refined BB84 simulation that outputs a final key (e.g., hashed or shortened).

- Documentation of steps and security reasoning.

### Tools:

- hashlib (for SHA-256 demo).

### Optional: Qiskit’s Aer simulator to simulate qubits more physically.

## Week 5: Evaluation & Presentation

### Objective: Analyze results and present findings.

### Tasks:

- Run simulations under multiple conditions:

- Different n_qubits

- Different Eve intercept probabilities

- Different channel noise

- Record QBER and final key length.

- Summarize insights: when can Eve be detected?

- Prepare a report and slide deck.

### Deliverables:

- Final notebook/report (with code, results, plots, and conclusions).

- Short 5–10 minute presentation.

### Optional Enhancements:

- Compare your classical simulation to a Qiskit-based quantum version.

- Add a simple GUI or web visualization for key distribution steps.

- Explore Decoy-State BB84 or E91 Protocol (advanced extension).

# 🧰 Recommended Tools Summary
| Purpose                       | Tool                          | Description                               |
| ----------------------------- | ----------------------------- | ----------------------------------------- |
| Simulation & Coding           | **Python + Jupyter Notebook** | Easy to visualize and document results    |
| Quantum simulation (optional) | **Qiskit (IBM Quantum)**      | For quantum circuit simulation            |
| Visualization                 | **Matplotlib, Seaborn**       | For QBER and key distribution analysis    |
| Data logging                  | **Pandas**                    | For storing and analyzing simulation runs |
| Hashing                       | **hashlib (SHA-256)**         | For privacy amplification demonstration   |
| Version control               | **Git + GitHub**              | For tracking progress and collaboration   |

# 🧪 Possible Experiments to Include

- Effect of eavesdropping: Plot QBER vs. Eve’s intercept rate.

- Effect of noise: Plot QBER vs. channel noise.

- Key length statistics: Compare raw, sifted, and final key lengths.

- Security threshold: Find the QBER level (≈11%) where secure key exchange fails.

# 📄 Expected Final Deliverables

- Jupyter Notebook: fully working BB84 simulation.

- Graphs: showing QBER trends and key statistics.

- Report (3–5 pages):

- Introduction to QKD and BB84

- Simulation methodology

- Experimental results and plots

- Conclusion on security and limitations

- Slide Deck (optional presentation): 5–10 minutes summary.