import mlx.core as mx
from ..recursive_mas import SFDLink


class ConsensusEngine:
    def __init__(self, sfd_link: SFDLink):
        self.sfd_link = sfd_link

    def compute_similarity_matrix(self, responses: dict) -> dict:
        """
        Extract hidden state for each response, compute NxN cosine similarity.
        Returns nested dict {name: {name: float}} with diagonal = 1.0.
        """
        names = list(responses.keys())
        embeds = {
            name: self.sfd_link.extract_hidden(resp)
            for name, resp in responses.items()
        }

        def cosine_sim(a, b):
            return float(
                mx.sum(a * b) / (mx.sqrt(mx.sum(a * a)) * mx.sqrt(mx.sum(b * b)))
            )

        return {
            ni: {
                nj: 1.0 if ni == nj else cosine_sim(embeds[ni], embeds[nj])
                for nj in names
            }
            for ni in names
        }

    def find_convergent_groups(
        self, similarity_matrix: dict, threshold: float = 0.85
    ) -> list:
        """
        Build graph where edge(i,j) exists if sim(i,j) > threshold.
        Return connected components as list of groups (sorted by size desc).

        Handles all cases with no presupposition:
          - unanimity   → one group of 7
          - majority    → one large + smaller groups/singletons
          - multi-split → several equal-sized groups
          - divergence  → all singletons
        """
        names = list(similarity_matrix.keys())
        parent = {n: n for n in names}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            parent[find(x)] = find(y)

        for ni in names:
            for nj in names:
                if ni != nj and similarity_matrix[ni][nj] > threshold:
                    union(ni, nj)

        groups_by_root = {}
        for name in names:
            groups_by_root.setdefault(find(name), []).append(name)

        groups = list(groups_by_root.values())
        groups.sort(key=len, reverse=True)
        return groups

    def generate_synthesis(
        self,
        responses: dict,
        group_names: list,
        similarity_matrix: dict,
        mi: str,
    ) -> str:
        """
        Find the latent centroid of the group: the agent with highest average
        cosine similarity to all other group members. Uses the pre-computed
        similarity matrix — no keyword matching, no re-embedding.
        Returns the centroid agent's response as the group synthesis.
        """
        if len(group_names) == 1:
            return responses[group_names[0]]

        centrality = {
            name: sum(
                similarity_matrix[name][other]
                for other in group_names
                if other != name
            ) / (len(group_names) - 1)
            for name in group_names
        }
        centroid = max(centrality, key=centrality.get)
        return responses[centroid]

    def build_output(
        self,
        phase1_responses: dict,
        phase2_responses: dict,
        mi: str,
    ) -> dict:
        """
        Full consensus pipeline:
        1. Compute NxN similarity matrix from Phase 2 hidden states
        2. Find emergent groups via connected components
        3. Generate synthesis per group from latent centroid
        4. Assemble structured output

        Result is fully dynamic — no hardcoded vote target.
        """
        names = list(phase2_responses.keys())
        n = len(names)

        sim_matrix = self.compute_similarity_matrix(phase2_responses)
        groups = self.find_convergent_groups(sim_matrix)

        # Global avg similarity (off-diagonal only)
        all_sims = [
            sim_matrix[ni][nj]
            for ni in names
            for nj in names
            if ni != nj
        ]
        avg_global = sum(all_sims) / len(all_sims)

        gruppi = []
        for group in groups:
            if len(group) > 1:
                grp_sims = [
                    sim_matrix[ni][nj]
                    for ni in group
                    for nj in group
                    if ni != nj
                ]
                avg_sim = sum(grp_sims) / len(grp_sims)
            else:
                avg_sim = 1.0

            sintesi = self.generate_synthesis(phase2_responses, group, sim_matrix, mi)

            gruppi.append({
                "ai": group,
                "similarity_media": round(avg_sim, 4),
                "sintesi": sintesi,
            })

        largest = max(groups, key=len)
        unanimita = len(groups) == 1 and len(groups[0]) == n

        return {
            "mi": mi,
            "voto": f"{len(largest)}/{n}",
            "gruppi": gruppi,
            "unanimita": unanimita,
            "avg_similarity_globale": round(avg_global, 4),
            "similarity_matrix": {
                ni: {nj: round(v, 4) for nj, v in row.items()}
                for ni, row in sim_matrix.items()
            },
            "phase1_responses": phase1_responses,
            "phase2_responses": phase2_responses,
        }
