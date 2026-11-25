# Vitruvius Memory

Independent authenticated Graphiti/Neo4j service. All inference, embeddings and reranking use OpenRouter. No OpenAI key or silent direct-provider fallback. Memory is accepted only with explicit approval; namespace validation and hashing isolate personal, project, board and expert groups.

Runtime: `/etc/vitruvius-memory/runtime.env`, root-owned mode 0600, based on `.env.example`. Generated internal bearer token is shared privately with the main service; generated Neo4j password never leaves runtime configuration.

`docker compose --env-file /etc/vitruvius-memory/runtime.env up -d --build`

Neo4j publishes **no ports**. API publishes **only 10.116.0.5:8001** and requires Bearer authentication for every endpoint, including health. Apply the Docker-aware firewall from the main repository to admit only main droplet 10.116.0.4. Do not expose Neo4j HTTP or Bolt to the Internet.

Endpoints: GET `/healthz`; POST `/episodes` with group_id/name/text/approved=true; POST `/search` with group_id/query/limit. Groups are `vitruvius:personal:owner` or `vitruvius:project|board|expert:<id>`. The API converts validated groups into collision-resistant Graphiti-compatible IDs. Unknown/unconfigured dependencies return 503; no fake memories.

Python 3.12: `uv sync --frozen`; `uv run pytest -q`. Constructor tests verify OpenRouter is the endpoint for both LLM and embedder. Live episode ingestion/search and durable restart checks are tracked in the deployment report.

Operations: back up the Neo4j volume consistently and verify restore; no backup is implied by this source. Original session history and approved artifacts remain authoritative in managed PostgreSQL. Temporary attachments are never automatically sent to Graphiti. Provider retention is separate from local deletion. Audio/video ingestion is a future extension, not an implemented feature.
