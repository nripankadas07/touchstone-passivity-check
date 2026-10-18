# Research —18 October2026

User: RF engineers reviewing a small exported network capture before model use.

Pain: Element magnitudes alone can hide coupled gain; reviewers need the worst sampled matrix and the exact tolerance convention.

Smallest useful capability: Check sampled one/two-port Touchstone S-matrix gain with an explicit singular-value report.

Acceptance: Recover coupled gain missed by per-column checks, lossless through and passive nonreciprocal networks; RI/MA/DB agreement; reject malformed options, row counts and frequency order.

Demand is inferred from workflow and adjacent public discussions, not verified product requests. Discovery: descriptive GitHub topics, runnable invented example and chronological portfolio index. No unsolicited outreach or activity manipulation.

## Alternatives and evidence

Live GitHub repository search sorted Most stars: `RF microwave; Qucs`. Highest-star relevant comparable found in the inspected scope: **ra3xdh/qucs_s**. Search and reference-follow coverage is limited, not an exhaustive global ranking. Unrelated keyword matches were excluded.

| Repository | Stars observed | Last push UTC | Archived | API license |
| --- | ---: | --- | --- | --- |
| [ra3xdh/qucs_s](https://github.com/ra3xdh/qucs_s) | 1409 | 2026-10-17T17:31:33Z | False | GPL-2.0 |
| [Qucs/qucs](https://github.com/Qucs/qucs) | 1329 | 2026-03-25T09:10:21Z | False | NOASSERTION |
| [scikit-rf/scikit-rf](https://github.com/scikit-rf/scikit-rf) | 949 | 2026-10-18T05:42:31Z | False | BSD-3-Clause |

Qucs-S and Qucs provide circuit simulation and Touchstone components. Scikit-rf already implements passivity/dissipation-matrix tests and much broader network analysis. Its per-port reference issues informed our explicit common-real-reference limit; they are not verified requests for this product. No missing competitor capability is claimed.

Current README, selected relevant source and up to five issue/PR records were read. [Provenance](RESEARCH_PROVENANCE.json) preserves exact URLs, observations and source identities. NOASSERTION is unclassified licensing, not permission to copy. No third-party implementation or fixtures are bundled.

Our narrow Python wheel has a clean-install example and failure contract. Established alternatives provide broader workflows, capabilities, documentation, examples and support communities. Competitor installs, time to first useful result, reliability, support response and technical performance were not measured. Our examples prove only our specified behavior. Stars inform discovery, not quality or performance. No feature-absence or superiority claim is made.

Portfolio distinction: All193 owned repositories were compared. No existing RF S-parameter matrix inspector was found. General numeric or evidence tools do not implement this physical-format contract.

Standard formats and algorithms are not inventions of this project; the implementation/report interface and invented fixtures are original. No branding or competitor prose is copied. No technical performance benchmark was conducted.
