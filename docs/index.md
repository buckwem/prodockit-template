---
hide:
    - navigation
    - toc
    - title
---

<!-- 
# Copyright (c) 2025-2026 Mark Buckwell and contributors
# SPDX-License-Identifier: MIT
-->

<!-- The "Source" button links to source_bundle.pdf, built by running
     `prodockit source-bundle` alongside `prodockit pdf` (see
     CONTRIBUTING.md and the CI workflow files) - remove this button if
     your project stops running that command, since the link would
     otherwise 404. -->
<div style="float: right; display: flex; gap: 15px; margin-left: 15px;" class="web-only" markdown="1">
[:material-archive: Source](source_bundle.pdf){ .md-button target="_blank" }
[:material-file-pdf-box: PDF](site_documentation.pdf){ .md-button target="_blank" }
</div>

<!-- Hide heading 1 on the page as hide: title does not seem to work -->
<style> .md-typeset h1 { display: none; } </style>
<!-- We still need a title set for the next/previous page navigation
     to work, so we set it here but hide it from the page.
-->
# Cover Page {.unnumbered .unlisted .hidden}

<!--
/*================== TITLE PAGE SURREY GITLAB ==================*/ 
-->
{% if is_surrey %}

<br>
<br>
<br>
![](assets/cover-centre-logo-black.png#only-light){ width="40%" style="display: block; margin: 0 auto;" }
![](assets/cover-centre-logo-white.png#only-dark){ width="40%" style="display: block; margin: 0 auto;" }

<!-- the different title line use styles defined in the extras.css file -->
<p class="title-ctr-b4">
Faculty of Engineering and Physical Sciences<br>
School of Computer Science and Electronic Engineering
</p>

<p class="title-ctr-4"> MSc programmes in Computer Science</p>


<p class="title-ctr-b4">module_id - module_name</p>

<!--
/*================== TITLE PAGE GITHUB OR OTHER GITLAB ==================*/
-->
{% else %}

<br>
<br>
<br>
![Illustration of abstract flowing concentric lines, representing professional documentation](assets/cover-hero-light.svg#only-light){ width="37.5%" style="display: block; margin: 0 auto;" }
![Illustration of abstract flowing concentric lines, representing professional documentation](assets/cover-hero-dark.svg#only-dark){ width="37.5%" style="display: block; margin: 0 auto;" }

<!-- the different title line use styles defined in the extras.css file -->
<p class="title-ctr-b4">
Crested Eagle Labs</p>

<p class="title-ctr-b4">
University of the World</p>

<p class="title-ctr-4">
Research programmes in Cyber Security</p>

{% endif %}

<!-- Outside the institution conditional so both cover variants use the same
     configured title. Zensical renders it for the website and ProDockit's
     cover preprocessing renders the same expression for the PDF. -->
<p class="title-ctr-b4">{{ config.site_name }}</p>

<br>
<br>
<br>
<br>


<!--
  In using this style, it's been applied to multiple lines using the line break
  Fill in your own name and the date the document is released.
-->
<p class="title-left-5">
Author: Insert Name Here
<br>
Date: Submission Date
</p>

<!-- Automated body-content word count, calculated by ProDockit's shared
     Zensical macro so the website and PDF display the same value. Delete
     this line if you don't want a word count shown on the cover page. -->
<p>Word count: {{ word_count }}</p>

<!-- ProDockit supplies the release of the template applied to this project.
     Keep it with the generated cover metadata so both cover variants show the
     same release on the website and in the PDF. -->
{% if applied_release %}
<p>Template release: {{ applied_release }}</p>
{% endif %}

<!-- ProDockit derives the repository URL from this checkout's origin remote,
     converting SSH syntax to a browser link and removing CI credentials. -->
{% if repo_url %}
<p>Repo: <a href="{{ repo_url }}">{{ repo_url }}</a></p>
{% endif %}
