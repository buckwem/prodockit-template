---
icon: lucide/book-open
---

<!-- 
# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT
-->

{{ heading_counter_reset(page) }}

# Section {: #section2 }

## SubSection {: #cross-reference-example }

Sections can be cross-referenced with `\ref{id}` - see \ref{section2-subsection-2} below, which stays correct even if you reorder or add pages.

Where the reader may be holding a printout, use `\autoref{id}` instead - see \autoref{section2-subsection-2}, which renders the same text and adds the target's page number in the PDF.

Both render the target's current number and name, so unlike a hand-typed "see Section 2.2 SubSection" they update themselves if the target moves - and `\autoref{id}` gives a printed reader somewhere to turn to, which a section number alone does not.

### SubSubSection {: #section2-subsubsection-1 }

### SubSubSection {: #section2-subsubsection-2 }

## SubSection {: #section2-subsection-2 }

### SubSubSection {: #section2-subsubsection-3 }

## SubSection {: #section2-subsection-3 }

### SubSubSection {: #section2-subsubsection-4 }