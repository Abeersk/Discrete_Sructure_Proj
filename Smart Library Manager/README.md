# 🔐 Advanced Password Security Analyzer

**Outcome:** A GUI Streamlit app that goes beyond basic “length-only” meters by combining entropy, attack-time estimation, blacklist checks, pattern detection, and visual benchmarking.

## Why this is better than a normal password strength meter
Typical meters only count length and a few character types. This analyzer adds:
1. **Entropy-based strength** using the character pool and length.
2. **Attack-time estimation** based on entropy (billion guesses/second model).
3. **Common-password blacklist** penalties for known weak choices.
4. **Pattern detection** (e.g., repeated characters).
5. **Actionable suggestions** with clear improvement guidance.
6. **History tracking** for recent passwords (local session only).
7. **Benchmark chart** to visualize length, complexity, and entropy side-by-side.

## Discrete Structures coverage (from your topic list)
**Used topics:** **10 / 14**  
The table below shows which of your required topics are actively used in the current implementation.

| Topic | Used? | Where it appears in the app |
|---|---|---|
| 1. Discrete Structures and Their Applications | Yes | Overall design of rule-based security evaluation |
| 2. Introduction to Propositional Logic | Yes | Rules like “length ≥ 12” and “has digit” |
| 3. Logical Connectives and Truth Tables | Yes | AND/OR combinations of rules (score from multiple conditions) |
| 4. Logical Equivalence and the Laws of Logic | No | Not explicitly modeled |
| 5. Applications of Propositional Logic | Yes | Security scoring and feedback logic |
| 6. Introduction to Sets and Notations | Yes | Character sets (lower/upper/digit/punct) |
| 7. Set Types | Yes | Subsets of the overall character pool |
| 8. Set Operations | Yes | Union of character sets to build the pool size |
| 9. Set Properties | Yes | Cardinality (pool size) used in entropy |
| 10. Venn Diagrams | No | Not visualized in the UI |
| 11. Applications of Sets | Yes | Keyspace/entropy modeling |
| 12. Cartesian Product | Yes | Keyspace = pool ^ length (implicit product) |
| 13. Relations | Yes | Relation between password features and score output |
| 14. Relation Types (Reflexive, Symmetric, Transitive) | No | Not explicitly modeled |

## Optional topics (not implemented yet)
These are **not** in the current code, but can be added if you want full coverage:
- Functions and its types
- Sequence and series (and differentiation between them)
- Permutations and combinations (and differentiation between them)
- Graphs
- Everyday-life and CS applications for each optional topic

## How to run
1. Install dependencies:
   ```powershell
   pip install streamlit pandas
   ```
2. Start the app:
   ```powershell
   streamlit run advanced_psw_analyzer\main.py
   ```

## Project structure
```
group_proj\
  advanced_psw_analyzer\
    main.py
  README.md
```
