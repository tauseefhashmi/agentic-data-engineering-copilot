# Schema mismatch
When a transformation fails because a column is missing, first inspect the upstream schema and the latest successful run. If the upstream change is intentional, update the model contract and tests. If the change is unexpected, stop downstream publication and open an incident ticket.

# Freshness breach
If a source is late, validate the upstream job status and last successful ingestion timestamp before rerunning downstream jobs.

# Duplicate records
Compare business keys against the last successful partition. Do not blindly delete data before identifying the duplicate-generation source.
