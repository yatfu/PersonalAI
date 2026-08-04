# Curriculum: Next.js (App Router, v16.2.10)

Source: `outputs/topicTrainer/nextjs/research.md` (approved). Dependency graph has no cycles/gaps — sequencing below follows it exactly, with one explicit deviation noted at Module 3.

## Placement call: Proxy (subtopic 9)

Proxy only hard-depends on Routing (3). Default position in the brief is after 4–8; the brief explicitly invites moving it earlier.

**Decision: placed as Module 3, immediately after Routing and before Server vs Client Components.** Reasons:
- It doesn't need RSC/client-boundary understanding at all — it's request-level rewriting/redirecting that happens before rendering.
- Teaching it right after Routing gives an early, satisfying win (redirects/rewrites work visibly) while the file-convention mental model is still fresh.
- Most importantly: it front-loads the "Proxy is NOT an auth boundary" warning (pitfall 6, backed by two 2026 CVEs) as early as possible, before the learner has any chance to reach for it as a security mechanism. The full justification ("real checks belong in Server Components/Server Actions/DAL") is necessarily a forward reference at this point — flagged explicitly in the module and revisited in full once Module 4 and Module 10 land.

This doesn't violate the graph: nothing after Module 3 depends on Proxy, and Proxy's own only dependency (Routing) is already satisfied.

---

## Modules

**1. Foundations & Setup** — weight 2/5 (light)
Objective: Know what Next.js adds over plain React and stand up a correctly-configured project.
Subtopics: 1 (What Next.js is & when to reach for it), 2 (Project setup & conventions)
Covers: meta-framework value prop vs. plain React SPA / alternatives; `create-next-app`, TS-by-default, `app/` convention, reserved file names, Turbopack-as-default.

**2. Routing (App Router)** — weight 4/5 (heavy)
Objective: Build a multi-page app using file-system routing, including dynamic and grouped routes.
Subtopics: 3 (Routing)
Covers: `page.tsx`/`layout.tsx` (layout persistence across nav), dynamic segments `[param]`, catch-all/optional catch-all, route groups, parallel/intercepting routes (flagged advanced/optional), async `params`/`searchParams`, and the file-convention *existence* of `loading.tsx`/`error.tsx`/`not-found.tsx` (behavioral depth deferred to Module 12).

**3. Proxy: Rewrites & Redirects** — weight 1/5 (light)
Objective: Use `proxy.ts` for rewrites/redirects/header manipulation, and know its one hard boundary: it is not where auth lives.
Subtopics: 9 (Proxy)
Covers: `middleware.ts` → `proxy.ts` rename rationale, rewrites/redirects/header manipulation, the CVE-backed "not an auth boundary" pitfall (flagged for full resolution in Module 10).
*Moved earlier than the brief's default position — see placement call above.*

**4. Server vs Client Components** — weight 5/5 (heaviest)
Objective: Correctly decide, for any piece of UI, whether it's a Server or Client Component, and understand the consequences of that boundary.
Subtopics: 4 (Server vs Client Components)
Covers: Server Components as default (zero JS), `"use client"` boundary and import-infection, SSR-once-then-hydrate for Client Components, serializable-props-only rule, Context must originate from a Client Component, `"use server"` ≠ rendering mode.

> **MILESTONE A — after Module 4:** You can build a multi-page routed app with deliberate, correct Server/Client Component boundaries (not "use client everywhere"), and you can explain why Proxy is unsuitable for auth even though you haven't built auth yet.

**5. Metadata & SEO** — weight 3/5 (medium)
Objective: Ship correct, per-route titles/descriptions/social previews from day one, not as later polish.
Subtopics: 5 (Metadata API / SEO)
Covers: static `metadata` export vs. async `generateMetadata()`, server-only constraint (pitfall: exporting from a `"use client"` file), title-template merging down the layout tree, file-based conventions (`opengraph-image.tsx`, `sitemap.ts`, `robots.ts`), contrast with deprecated `next/head`.
Depends on 3 (Routing, Module 2) + 4 (Server/Client, Module 4) — both satisfied.

**6. Data Fetching & Caching** — weight 5/5 (heaviest, tied with Module 4)
Objective: Fetch data idiomatically in Server Components under the new explicit-caching model, and use streaming to avoid blocking the page on slow data.
Subtopics: 6 (Data fetching & caching model)
Covers: native `fetch()` in Server Components, `"use cache"`/`cacheLife()`/`cacheTag()`, Partial Prerendering (stable via `cacheComponents: true`), `<Suspense>` streaming, why "cached by default" tutorials are now wrong, legacy `revalidate` export as deprecated-but-working fallback.

**7. Mutations: Server Actions & Route Handlers** — weight 4/5 (heavy)
Objective: Write data back to the server the right way for the right consumer — a form/UI mutation vs. an external/webhook endpoint.
Subtopics: 7 (Server Actions), 8 (Route Handlers)
Covers: `"use server"` functions, `useActionState`, `revalidatePath` vs. `revalidateTag` (flagged as the most commonly-gotten-wrong decision), one-at-a-time execution per client, "don't use Server Actions for large uploads"; `app/api/.../route.ts` per-verb exports as the Route Handler replacement for `pages/api`; explicit compare/contrast of when to use which.
Grouped together because the brief itself teaches subtopic 8 by contrasting it against subtopic 7 — splitting them would duplicate the comparison.

> **MILESTONE B — after Module 7:** You can build one complete CRUD feature end-to-end: read data with caching/streaming (Module 6), mutate it via a Server Action with the correct revalidation call, and expose the same data through a Route Handler for a non-Next client.

**8. Styling, Assets & Optimization** — weight 2/5 (light-medium)
Objective: Style a Next.js app and use its built-in asset primitives instead of hand-rolled equivalents.
Subtopics: 10 (Styling, assets, optimization primitives)
Covers: CSS Modules, Tailwind as the common addition, `next/image` (sizing requirements), `next/font` (no layout shift), `next/script` (load-strategy control). Note: OG/social images already covered under Metadata (Module 5), not repeated here.

**9. Build & Performance Tooling** — weight 2/5 (light-medium)
Objective: Understand what's making the dev/build loop fast by default and what's opt-in.
Subtopics: 11 (Build & performance tooling)
Covers: Turbopack as default bundler for dev+build, React Compiler (stable but off-by-default — opt in via config + babel plugin), Hydration Diff Indicator, Server Function Logging, 16.3-preview items mentioned as forward-looking only (not taught).

**10. Auth & Authorization** — weight 4/5 (heavy)
Objective: Add authenticated, authorized routes using a centralized server-side pattern — closing the loop opened by the Module 3 Proxy warning.
Subtopics: 12 (Auth & authorization patterns)
Covers: no built-in auth; cookie/session pattern via fully-async `cookies()`/`headers()`; DAL (Data Access Layer) centralizing checks and returning minimal DTOs; NextAuth/Auth.js, Clerk as common libraries; explicit callback to why this — not Proxy — is where real checks belong.
Depends on 4 (Module 4) and 7 (Module 7) — both satisfied; also sequenced after 11 per the graph's `10 → 11 → 12` chain.

> **MILESTONE C — after Module 10:** You can add a protected route that reads session state in a Server Component and mutates it via a Server Action, gated through a DAL — with zero reliance on Proxy for security decisions.

**11. Deployment** — weight 2/5 (medium)
Objective: Ship the app to production, on Vercel or elsewhere.
Subtopics: 13 (Deployment)
Covers: Vercel zero-config path (ISR/PPR/Image Opt/Edge all work out of the box), self-hosting via `output: 'standalone'`, the new Deployment Adapter API (16.2) for third-party hosts, caveat that adapter maturity varies by platform.

**12. Error Handling, Loading States & Testing** — weight 3/5 (medium)
Objective: Design good loading/error UX per route segment and know where testing fits (without building a full test suite here).
Subtopics: 14 (Error handling, loading states, testing)
Covers: `loading.tsx` skeleton design and nested boundaries, `error.tsx` as a Client Component boundary with reset patterns, `global-error.tsx` vs. segment-level, `notFound()` vs. a route simply not matching; Vitest/Jest/Playwright named as community-standard, scoped light per the brief's beginner-focus note.
Explicitly a *revisit* of the file-convention mechanics introduced in Module 2 — behavioral depth only, no duplication.

**13. Pages Router: Legacy Recognition** — weight 1/5 (lightest)
Objective: Recognize Pages Router code in older tutorials/codebases without building new work in it.
Subtopics: 15 (Pages Router legacy)
Covers: `pages/` directory, `getStaticProps`/`getServerSideProps`/`getStaticPaths`, default-export API routes, why older tutorial content can mislead (pitfall 15). Kept deliberately short per the brief's own note (openQuestion 1) — recognition only, not a full module's worth of depth despite occupying a module slot for structural clarity.
No hard dependency; placed last as a low-stakes capstone note rather than mid-stream, so it doesn't interrupt the practical build arc.

> **MILESTONE D (capstone) — after Module 13:** You can take an app from Module 7's CRUD feature through styling, performance awareness, auth, and deployment, and you can tell App Router code apart from Pages Router code on sight.

---

## Summary table

| # | Module | Subtopics | Weight |
|---|--------|-----------|--------|
| 1 | Foundations & Setup | 1, 2 | 2/5 |
| 2 | Routing (App Router) | 3 | 4/5 |
| 3 | Proxy: Rewrites & Redirects | 9 | 1/5 |
| 4 | Server vs Client Components | 4 | 5/5 |
| — | **Milestone A** | | |
| 5 | Metadata & SEO | 5 | 3/5 |
| 6 | Data Fetching & Caching | 6 | 5/5 |
| 7 | Mutations: Server Actions & Route Handlers | 7, 8 | 4/5 |
| — | **Milestone B** | | |
| 8 | Styling, Assets & Optimization | 10 | 2/5 |
| 9 | Build & Performance Tooling | 11 | 2/5 |
| 10 | Auth & Authorization | 12 | 4/5 |
| — | **Milestone C** | | |
| 11 | Deployment | 13 | 2/5 |
| 12 | Error Handling, Loading States & Testing | 14 | 3/5 |
| 13 | Pages Router: Legacy Recognition | 15 | 1/5 |
| — | **Milestone D (capstone)** | | |

13 modules, all 15 subtopics covered (7 and 8 combined in Module 7), 4 milestones spaced every 3–4 modules. Dependency graph fully respected; no contradictions found in the research brief.
