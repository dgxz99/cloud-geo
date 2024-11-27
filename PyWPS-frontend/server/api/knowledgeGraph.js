// server/api/knowledgeGraph.js
const express = require("express");
const router = express.Router();
const driver = require("../config/neo4jConfig");

router.get("/knowledge-graph", async (req, res) => {
    const session = driver.session();
    const { limit = 100, skip = 0 } = req.query;
    const query = `MATCH (n)-[r]->(m) RETURN n, r, m, labels(n) AS labelsN, labels(m) AS labelsM SKIP ${skip} LIMIT ${limit}`;

    try {
        const result = await session.run(query);
        const nodes = [];
        const edges = [];

        result.records.forEach((record) => {
            const nodeA = record.get("n");
            const nodeB = record.get("m");
            const relation = record.get("r");
            const labelsA = record.get("labelsN");
            const labelsB = record.get("labelsM");
            const labelA = Array.isArray(labelsA) && labelsA.length > 0 ? labelsA[0] : 'Unknown';
            const labelB = Array.isArray(labelsB) && labelsB.length > 0 ? labelsB[0] : 'Unknown';

            nodes.push({
                data: {
                    id: nodeA.identity.toString(),
                    label: nodeA.properties.name || nodeA.properties.Title || 'Unknown',
                    labels: labelA
                }
            });
            nodes.push({
                data: {
                    id: nodeB.identity.toString(),
                    label: nodeB.properties.name || nodeB.properties.Title || 'Unknown',
                    labels: labelB
                }
            });

            edges.push({
                data: {
                    source: nodeA.identity.toString(),
                    target: nodeB.identity.toString(),
                    label: relation.type,
                },
            });
        });

        res.json({ nodes, edges });
    } catch (error) {
        console.error("Error fetching knowledge graph:", error);
        res.status(500).send("Error");
    } finally {
        await session.close();
    }
});

module.exports = router;
