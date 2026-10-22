# Sources and maintenance notes

Policy/method sources reviewed on 2026-10-15; workflow revised and browser recovery spot-checked on 2026-10-16. Recheck applicable marketplace requirements during actual projects; links and feature availability can change. A cached/search-readable document and a successful authenticated current-page review are not the same thing.

Version 1.2.0 finalized on 2026-10-17 adds staged inspection, per-ASIN checkpoints and an offline consistency checker. Additional browser spot checks on 2026-10-16 covered a nine-image gallery inventory (two large images inspected) and an A+ native four-column step module. These checks do not refresh policy verification or establish full competitor coverage.

Version 1.3.0 on 2026-10-19 adds localized residential scene/occasion expansion and visual direction for lifestyle/A+ layouts, palette, typography and motivated light/shadows. The user-supplied finished set and local plant library were inspected within the scope documented in [local reference study](reference-study.md); external directories are provenance, not runtime dependencies or product/policy evidence. This revision does not refresh the official-policy checks above.

Version 1.4.0 adds explicit scale/projection/framing checks, a bounded outside-inspiration search workflow, supporting-prop hierarchy, protection from text/blur effects and optional expressive display type. The user's 2026-10-19 instruction establishes **1600×1600 secondary** and **1464×600 desktop A+** production defaults; this supersedes inherited 2000/970 test suggestions for new work, not the real requirements of every account slot. The public Amazon A+ overview was reopened as text; no authenticated account or universal 1464×600 module acceptance was verified.

## Public scene-inspiration spot check — 2026-10-19

Searches used category/home-styling and seasonal-placement queries, narrowed to primary home-brand pages. The following pages were opened/read as text; their image links/alt text were not treated as actual visual inspection. This checks source discovery, not a new full competitor study or cross-category image campaign.

|Source|Useful candidate information|Boundary|
|---|---|---|
|[IKEA indoor plant decor](https://www.ikea.com/au/en/rooms/living-room/how-to/style-your-home-with-indoor-plant-decor-pub832cc460/)|Floor/shelf placement and books as contextual staging suggest different scale/placement tasks|Do not adopt added plants, larger container or general wellness/care claims as our SKU facts; no copied scene composition|
|[IKEA artificial plants and flowers](https://www.ikea.com/gb/en/ideas/how-to-style-and-maintain-artificial-plants-and-flowers-pubf9703de1/)|Bouquet/table/storage-area tasks widen candidates beyond wall-hung decor|Do not trim/rebuild our SKU, add stems, transfer another product's suitability or make a live item artificial|
|[Pottery Barn holiday mantel](https://www.potterybarn.com/tips-and-ideas/how-to-decorate-your-mantle-for-the-holidays/)|Mantel, small seasonal objects and flameless lighting provide occasion/context alternatives|Not a mandate to add every prop or to put an unsupported product near fire; does not prove weather/fire performance or conversion|

These sites are examples of useful public discovery, not mandatory runtime dependencies, preferred affiliate sources or fixed templates. Future searches must use the actual product/category/market. Store external inspiration as SRC-INSP, separate from competitor V and product P evidence.


## Authoritative starting points

- [Amazon product image guide](https://sellercentral.amazon.com/help/hub/reference/external/G1881?locale=en_us): marketplace image requirements. During authoring, indexed text was accessible; a direct open returned a login/JavaScript shell. Record that limitation rather than claiming account/category-level verification.
- [Amazon A+ design guide](https://sell.amazon.com/blog/a-plus-content-design-guide): accessible official overview of content types, native modules, and content restrictions. Exact account fields and sizes still require the seller's actual Content Manager.
- [Amazon A+ content guidelines entry](https://sellercentral.amazon.com/help/hub/reference/external/G202102930): direct access returned a login/JavaScript shell during authoring. Do not treat this link alone as a read policy.
- [Amazon SP-API models](https://github.com/amzn/selling-partner-api-models): official API schemas if API work is separately requested. This planning skill neither implements SP-API nor infers all UI capabilities from the schemas.
- [Official OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills): skill discovery, SKILL.md, supporting resources, and local skill locations. This repository's `skills/` folder is a source/distribution layout, not proof that the current Codex session has installed it.

## User-supplied methodological references

These were inspected as background, not installed or copied as dependencies. Their tool/model recommendations and commercial links are not adopted.

| Reference | Relevant idea | Boundary |
| --- | --- | --- |
| [nexscope-ai/Amazon-Skills](https://github.com/nexscope-ai/Amazon-Skills) | Separate keyword, review, listing and image tasks | No assumption that its tools or paid datasets exist here |
| [ecommerce-image-skills A+ skill](https://github.com/xianyu110/ecommerce-image-skills/blob/main/skills/amazon-a-plus/SKILL.md) | Repeat product identity constraints across prompts | No adoption of model names, third-party generation endpoints, or fixed A+ dimensions |
| [SERP-Clustering](https://github.com/MarcoGiordano96/SERP-Clustering) | Cluster terms by shared search-result URLs when raw data exists | Semantic grouping remains valid when SERP data is absent; no fabricated overlap |
| [onlineshop-image-optimizer](https://github.com/ptmrio/onlineshop-image-optimizer) | Possible downstream export processing | Out of scope: this skill produces no image exports |
| [Sentiment-Analysis-of-Amazon-Reviews](https://github.com/sks006/Sentiment-Analysis-of-Amazon-Reviews) | Optional aid for text exploration | Theme evidence and sample denominators take precedence over sentiment scores |

## Deliberate corrections to the initial reference workflow

- Claim eligibility depends on evidence scope, not a letter grade alone. An unsupported claim cannot be rescued by putting it in FAQ or prefixing it with “designed to”.
- Search demand, keyword ranking, tool estimates and measured organic traffic are distinct observations.
- The user's 2026-10-16 revision supersedes the original count: DIM01, DETAIL01, SCENE01–04 and APLUS01–05, exactly 11 image assets with no MAIN by default.
- A+ module count and image count differ; allocate actual modules within the five-image budget. Native text fields stay separate; additional required derivatives need an explicit scope change.
- Reviews inform buying objections; customer-review graphics are not a default image asset. Guarantees are not a default A+ closing module.
- Preserve genuine product markings while excluding added MAIN overlays. A sparse plant must not be artificially densified to meet frame coverage.
- Fixed title lengths, preview sizes, observation periods and suggested listing resolution are working conventions, not universal platform rules.

No source grants permission to use competitor photos as this product's identity references. Use only supplied/authorized assets for production.
