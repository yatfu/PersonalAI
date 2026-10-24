# Interview study guide

An anonymized résumé companion with 55 study topics and 109 practice questions across ten sections. Names, contact information, profile links, employer/client names, school name, and personal dates are removed.

Open `dist/index.html` directly in a browser. No installation or build is required. To serve locally, run `python -m http.server 8765 --directory outputs/interviewGuide/dist` from the repository root.

The static page uses `guideData.js` for résumé content and questions, `app.js` for search, expandable panels and browser-local progress, and `styles.css` for responsive and print layouts. Practice progress stays in the current browser.

Validation: `node --check outputs/interviewGuide/dist/app.js` and `node --check outputs/interviewGuide/dist/guideData.js`. There is no automated test suite. Manually check search, expand/collapse, checkmark persistence, and printing after changes.

Local hosting configuration and deployment archives are excluded from Git.
