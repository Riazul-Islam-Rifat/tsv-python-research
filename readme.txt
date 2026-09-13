# TSVD Python Research

This project reproduces real, confirmed thread-safety violation (TSV) bugs in Python projects.
Then tests whether existing tools (threadcheck) can detect them or not. 
Finally a detector prototype (basic_tsvd) is implemented for #wavefront_sdk-issue inspired by the TSVD4J approach.

## Setup

1. Clone the repo and enter it.

2. Create and activate a virtual environment

3. Install dependencies


## poc1 — wavefront-sdk-python#87

- Reproduce the raw crash (using the real, unmodified pre-fix library code)

- Confirm threadcheck misses it (using threadcheck command)

- Run the basic-tsvd detector


## Running poc2 — psf/requests#6366 --> similar approach of poc1
