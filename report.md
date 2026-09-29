# Project 1 Report: Intelligent Search Visualizer

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Selected Region:**`, `**Live Deployment URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information 
- **Name:** Christopher Moreno
- **UID (netID):** cmore50
- **UIN:** 660533792

---

## Section 1: Selected City Region
- **Selected Region:** Boston

---

## Section 2: Map Graph Configuration
- **Total Cities Configured:** 22
- **Total Connection Edges:** 37
- **Graph Fully Connected:** Yes

---

## Section 3: Local Verification & Search Algorithms
*Check the algorithms you successfully ran and verified on your local development server by placing an `x` in the brackets (e.g., `[x]`):*
- [x] Breadth-First Search (BFS)
- [x] Depth-First Search (DFS)
- [x] Uniform Cost Search (UCS)
- [x] Iterative Deepening Search (IDS)
- [x] Greedy Best-First Search (Greedy)
- [x] A* Search (A*)

---

## Section 4: Deployed and Presentation Information
- **Deployment Platform:** Render
- **Live Deployment URL:** https://boston-search-visualizer-1.onrender.com/
- **Video Presentation Link:** [Provide an accessible link to your 5–7 minute video presentation]

---

## Section 5: Discussion
- **Which search algorithm is best for this route finding problem?** 
    I believe A* is the best algorithm for this route finding problem. Route finding on a physical road network requires both cost-optimality and computational efficiency. A* always returns the exact same minimal-cost driving route as Uniform-Cost search does in this problem while also able to better avoid non-viable branches.
- **Search Efficiency (Nodes expanded/time taken comparison):** Greedy Best-First search consistently is able to expand the fewest nodes and finishes with the shortest runtime because it evaluates strictly on h(n). A* is the best balance of both efficiency and finding the shortest path. Uniform-Cost search gurantees the optimal path but lacks in time taken/nodes expanded. Both Breadth-First Search and Iterative Deepening Search expand a large number of nodes layer by layer while usually finding slower routes. Depth First Search gives the worst performance giving terrible high mileage paths while expanding an extreme number of paths.
- **Link the idea of search algorithm to today Generative AI.** 
    LLMs, although mainly generating text, still use a massive search tree. Advanced reasoning systems generate and evaluate multiple candidate reasoning paths before answering. Same as the search algorithms I generated, it may go through multiple paths before deciding on the best one.  