# Research Brief: Next.js (React Web Framework, Vercel)

**Status:** Approved by researchValidator on revision pass 1 of 2 (one trivial correction applied below per validator note: CVE fix version corrected from 16.2.5 to 16.2.6).

## researchedAt

- **Research conducted:** 2026-07-13 (revision 1)
- **Source recency:** Sources current as of June–July 2026.
- **Current version, precisely stated:** Next.js **16.2.10** is the current stable/latest release and the correct target for a beginner curriculum. Next.js **16.3 exists only as a preview release** (`npm install next@preview`; three-part blog series June 25/26/29, 2026; stable release "expected in the coming weeks" but not shipped as of this research date). Do not pin or recommend 16.3 anywhere — mention it only as a forward-looking note.

## topicMap

1. **What Next.js is & when to reach for it** — A React meta-framework (Vercel) adding routing, rendering (SSR/SSG/streaming), bundling, and server infrastructure on top of React. Reach for it over a plain React SPA when you need SEO/first-load performance, a full-stack app, or Vercel-native deployment.
2. **Project setup & conventions** — `create-next-app`, TypeScript-by-default scaffolding, `app/` directory convention, `next.config.ts`, ESLint/Turbopack config.
3. **Routing (App Router)** — File-system routing under `app/`: `page.tsx`, `layout.tsx`, dynamic segments, catch-alls, route groups, parallel/intercepting routes. Also where `loading.tsx`/`error.tsx`/`not-found.tsx` are introduced as file-convention mechanics (behavioral depth covered later in 14).
4. **Server vs Client Components** — React Server Components (RSC) are the default; `"use client"` opts into client rendering. The single biggest conceptual shift from plain React.
5. **Metadata API / SEO** — `generateMetadata()` (async, server-only) and static `metadata` export; file-based conventions (`opengraph-image.tsx`, `sitemap.ts`, `robots.ts`); title-template merging down the layout tree. Depends on Routing (3) + Server/Client Components (4) since it's server-only and route-segment-scoped. Nextjs.org calls this "the cornerstone of SEO in App Router sites" — placed early because nearly every real project needs it from week one, not as late-stage polish.
6. **Data fetching & caching model** — `fetch()`, the `"use cache"` directive, `cacheLife()`/`cacheTag()`, Partial Prerendering (PPR, stable via `cacheComponents: true`), streaming with `<Suspense>`. Supersedes old Pages Router APIs.
7. **Mutations: Server Actions** — `"use server"` functions, `useActionState`, `revalidatePath` vs `revalidateTag`, optimistic UI.
8. **Route Handlers (API routes)** — `app/api/.../route.ts`, HTTP-verb exports; the App Router replacement for `pages/api`.
9. **Proxy (formerly Middleware)** — `proxy.ts` (renamed from `middleware.ts` in v16); rewrites/redirects/header manipulation, explicitly **not** an auth boundary (see pitfalls). Only hard-depends on Routing (3) — its placement here (after 4–8) is a pedagogical judgment call, not a strict prerequisite; a lighter path could teach it right after Routing.
10. **Styling, assets, optimization primitives** — CSS Modules, Tailwind, `next/image`, `next/font`, `next/script`. (OG images live in Metadata/5, not here.)
11. **Build & performance tooling** — Turbopack (default bundler for dev+build in v16), React Compiler (stable but opt-in, not default), Hydration Diff Indicator (16.2). 16.3-preview's "Instant Navigations"/AI tooling/Turbopack persistent cache work is a forward-looking mention only.
12. **Auth & authorization patterns** — No built-in auth; DAL (Data Access Layer) pattern; `cookies()`/`headers()` are fully async; NextAuth/Auth.js, Clerk as common libraries.
13. **Deployment** — Vercel (zero-config), self-hosting via `output: 'standalone'`, the new Deployment Adapter API (16.2) for third-party hosts.
14. **Error handling, loading states, testing** — Revisits `loading.tsx`/`error.tsx`/`not-found.tsx` from (3) for behavioral depth (reset patterns, `global-error.tsx` vs segment-level, imperative `notFound()`); Vitest/Jest/Playwright as community-standard, not bundled.
15. **Pages Router (legacy/context)** — Pre-13 paradigm, maintenance mode. Recognize, don't build in it.

## dependencies

```
1 → 2 → 3 ──┬─────────────────────────────┐
            ▼                             ▼
            4 (Server/Client Components)  9 (Proxy — only hard-depends on 3;
            │                                placement after 4-8 is a judgment
            ▼                                call, not a strict requirement)
            5 (Metadata — depends on 3+4)
            │
            ├──────────┬───────────┐
            ▼          ▼           ▼
            6 (data)   7 (actions) 8 (route handlers)
            │          │           │
            └────┬─────┴───────────┘
                 ▼
                10 (styling) → 11 (build/perf) → 12 (auth) → 13 (deployment) → 14 (error handling, behavioral depth)

15 (Pages Router legacy) — no hard dependency, insertable any time after 4.
```

Notes:
- (4) Server vs Client Components is a hard gate — nothing about Metadata, data fetching, Server Actions, or Route Handlers makes sense without it.
- (5) Metadata is placed immediately after (3)+(4), not deferred to styling/polish, because it's server-only and route-scoped, and because a practical/build-oriented learner needs correct titles/social previews from their first real page.
- (9) Proxy's position is a judgment call, explicitly flagged — curriculumPlanner may move it earlier (right after Routing) for a lighter path without violating any dependency.
- (12) Auth depends on both (4) and (7) — idiomatic auth reads session state in Server Components and mutates it via Server Actions.
- (14) explicitly revisits, not duplicates, the file conventions from (3) — see coverage-split note above.

## keyConcepts

**1. What Next.js is / when to use it** — Next.js = React + routing + rendering strategies + bundler + server runtime. Decision criteria vs. plain React SPA (SEO, first paint, server data access) and vs. alternatives (Remix, TanStack Start, Astro). Current stable major version is 16 (16.2.10); App Router is the default paradigm.

**2. Project setup** — `npx create-next-app@latest` scaffolds TypeScript + `app/` by default. Reserved file names (`page`, `layout`, `loading`, `error`, `route`, `template`, `default`) are special to the framework. Turbopack is the default bundler for both `next dev` and `next build` in v16.

**3. Routing** — Folders = route segments; `page.tsx` makes a segment reachable. `layout.tsx` wraps children and **persists across navigations** (no re-render). Dynamic segments `[param]`, catch-all `[...param]`, optional catch-all `[[...param]]`, route groups `(name)`. Parallel/intercepting routes are advanced/optional for beginners. `params`/`searchParams` are **async** — must be awaited (hard breaking-change point vs. older tutorials).

**4. Server vs Client Components** — Everything in `app/` is a Server Component by default (zero JS shipped). `"use client"` opts a module (and its imports) into client rendering for hooks/events/browser APIs. Client Components still SSR once, then hydrate. Server→Client props must be serializable (no functions/class instances, except Server Actions). React Context must be provided from a Client Component — doesn't reach across the boundary otherwise. `"use server"` marks a **Server Action**, not a rendering mode — frequent point of confusion.

**5. Metadata API / SEO** — Static `metadata` export vs. async `generateMetadata()` (lets you fetch data before computing title/description). **Server-only** — cannot export from a `"use client"` file (a common, sometimes-silent failure mode). Merges down the layout tree: root `title.template` + `default`, children supply the `%s` piece. File-based conventions: `favicon.ico`, `icon.png`/`apple-icon.png`, `opengraph-image.tsx`/`twitter-image.tsx` (static or dynamic via `ImageResponse`), `robots.ts`, `sitemap.ts`. Contrasts with the deprecated Pages Router `next/head` pattern.

**6. Data fetching & caching** — Native `fetch()` in Server Components is primary; no `useEffect`+`useState` needed for initial data. Caching is now largely **explicit/opt-in** (`"use cache"`, `cacheLife()`, `cacheTag()`, or Cache Components) rather than cached-by-default. Partial Prerendering (PPR) graduated to **stable** via `cacheComponents: true` (replacing the old `experimental.ppr` flag) — Vercel positions it as the intended default rendering strategy going forward. `<Suspense>` streaming keeps slow data from blocking the rest of the page. Legacy `export const revalidate = 60` still works if `cacheComponents` is off, but is deprecated under the new model.

**7. Server Actions** — `"use server"` defines a callable mutation, usable from a form's `action` prop or a Client Component handler. `useActionState` (React 19+) exposes pending/result state. POST-only by design + Origin/Host checks mitigate CSRF, but that's not a substitute for real authorization inside the action. `revalidatePath` vs `revalidateTag` is described as "the decision most often gotten wrong" — use `revalidateTag` when the acting user needs to see their own write immediately. Server Actions execute **one at a time per client** (not parallel) and aren't meant for large file uploads.

**8. Route Handlers** — `app/api/.../route.ts` exports named per-verb functions (`GET`/`POST`/etc.), replacing the Pages Router's default-export `pages/api` pattern. Use for webhooks, external/non-Next clients, large/streaming payloads; use Server Actions for your own UI's form-driven mutations.

**9. Proxy (formerly Middleware)** — Renamed `middleware.ts` → `proxy.ts` in v16 (function `middleware` → `proxy`; codemod available via `npx @next/codemod`). Vercel's rationale: the old name invited Express-style-middleware assumptions and encouraged misuse as an auth boundary. **This is backed by two confirmed 2026 CVEs** (see pitfalls) — not just a style preference.

**10. Styling/assets/optimization** — `next/image` (auto resize/format/lazy load, needs width/height or `fill`), `next/font` (self-hosted, no layout shift), `next/script` (load-strategy control). CSS Modules built in; Tailwind is the common addition. OG/social images live under Metadata (5), not here.

**11. Build & performance tooling** — Turbopack default for dev+build in v16 (Vercel claims ~87% faster cold dev start, ~2.5x faster prod builds vs. Webpack; 16.2 adds ~400% faster dev startup). React Compiler is stable-as-a-config-option but **off by default** — opt in via `reactCompiler: true` + `babel-plugin-react-compiler`; auto-memoizes, replacing manual `useMemo`/`useCallback`/`React.memo`, at the cost of build/dev compile time. New in 16.2: Server Function Logging, redesigned 500 page, Hydration Diff Indicator. 16.3 (preview-only) is reportedly focused on Instant Navigations, deeper AI/agent tooling, and Turbopack persistent-cache work — mention only, not taught.

**12. Auth & authorization** — No built-in auth; standard pattern is cookie/session-based, read via `cookies()`/`headers()` (both fully async in v16, sync access removed). Recommended: a server-only Data Access Layer (DAL) centralizing checks and returning minimal DTOs, rather than scattering role checks. Common libraries: Auth.js/NextAuth, Clerk, Lucia-style custom sessions.

**13. Deployment** — Vercel: zero-config, tightest integration (ISR/PPR/Image Optimization/Edge all work out of the box). Self-hosting: `output: 'standalone'` for a minimal Node bundle (Docker/Kubernetes), full control but more ops overhead. Deployment Adapter API (new 16.2): a stable, versioned contract for third-party platforms (Cloudflare, Netlify, AWS) to build proper adapters, reducing "works on Vercel, breaks elsewhere" bugs — though adapter maturity varies by platform.

**14. Error handling, loading states, testing** — `loading.tsx` auto-wraps a segment in `<Suspense>` (mechanics in 3; here: designing good skeletons, nested loading boundaries). `error.tsx` is a Client Component boundary per segment; `global-error.tsx` for root-layout errors (here: reset patterns, what's safe to show vs. log server-side). `not-found.tsx` + imperative `notFound()` (here: when to call it vs. letting a route simply not match). Next.js doesn't bundle a test runner — Vitest/Jest + Playwright are community-standard; scope down for a beginner curriculum unless testing is an explicit goal.

**15. Pages Router (legacy)** — `pages/` directory, `getStaticProps`/`getServerSideProps`/`getStaticPaths`, default-export API routes, Client-Components-only mental model. Maintenance mode — don't build new projects here, but recognize it for older material/existing codebases.

## pitfalls

1. **Overusing `"use client"`** — drags large subtrees into the client bundle. Default to Server Components; push `"use client"` to the smallest leaf that needs it.
2. **Confusing `"use server"` with "this makes a Server Component"** — it marks a Server Action, not a rendering mode.
3. **Using React Context across the Server→Client boundary directly** — Providers must be Client Components; pass server-read state down as props/resolved data instead.
4. **Assuming `fetch()` is cached by default** — caching is now largely explicit; code from older tutorials may behave differently under 16.
5. **Following outdated PPR/`experimental.ppr` advice** — replaced by `cacheComponents: true`; mixing old/new caching config causes confusing behavior.
6. **Treating Proxy as an auth boundary — a confirmed real-world failure, not just a style concern.** Next.js's May 2026 security release fixed **CVE-2026-44573** (Pages Router + i18n: an unprefixed `/_next/data/<buildId>/<page>.json` request bypasses the middleware matcher because it requires a locale segment) and **CVE-2026-44574** (dynamic-route parameter injection via query params alters the effective route in a way middleware doesn't see, bypassing authorization checks). Both fixed as of **16.2.6** — the initial 16.2.5 patch was incomplete for Turbopack-enabled apps (tracked separately as CVE-2026-45109/GHSA-26hh-7cqf-hhc6); since this curriculum teaches Turbopack as the default bundler, 16.2.6+ is the version that actually closes the gap. Real auth checks belong in Server Components/Server Actions/Route Handlers, ideally behind a DAL — never solely in Proxy.
7. **Using `next/head` in the App Router** — a Pages Router habit; the App Router replaces it entirely with the Metadata API.
8. **Exporting `generateMetadata`/`metadata` from a `"use client"` file** — metadata exports are server-only; a common, sometimes-silent trip-up when a page/layout file was marked client for an unrelated reason. Fix: move the interactive part into a child Client Component.
9. **Forgetting `params`/`searchParams`/`cookies()`/`headers()` are async** — sync access was fully removed in v16.
10. **Leaking sensitive data through Server→Client props** — pass only what the client actually needs.
11. **Picking the wrong revalidation function** — `revalidatePath` vs `revalidateTag`; use `revalidateTag` when the acting user needs to see their own write immediately.
12. **Using Server Actions for large file uploads** — use a Route Handler with streaming instead.
13. **Assuming Server Actions run in parallel** — they're dispatched one at a time per client.
14. **Expecting layouts to re-fetch on navigation** — `layout.tsx` persists by design; state is preserved, no re-render.
15. **Learning from Pages-Router-era content without realizing it** — syntax/mental model differ enough from the App Router + v16 caching/proxy/metadata changes to cause real confusion.
16. **Expecting React Compiler on by default** — it's stable-as-an-option but off by default in 16.2/16.3.
17. **Installing/following `next@preview` (16.3) content as if it were stable** — teach against 16.2.10, not the preview channel.

## sources

Official: [Next.js Blog](https://nextjs.org/blog) (incl. [16](https://nextjs.org/blog/next-16), [16.2](https://nextjs.org/blog/next-16-2), [16.3 Instant Navigations](https://nextjs.org/blog/next-16-3-instant-navigations), [16.3 AI Improvements](https://nextjs.org/blog/next-16-3-ai-improvements), [16.3 Turbopack](https://nextjs.org/blog/next-16-3-turbopack)) · [Next.js Docs — Server/Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [Server Actions guide](https://nextjs.org/docs/app/guides/server-actions), [Forms guide](https://nextjs.org/docs/app/guides/forms), [Proxy file convention](https://nextjs.org/docs/app/api-reference/file-conventions/proxy), [Proxy getting started](https://nextjs.org/docs/app/getting-started/proxy), [Middleware→Proxy rename](https://nextjs.org/docs/messages/middleware-to-proxy), [Upgrading to v16](https://nextjs.org/docs/app/guides/upgrading/version-16), [PPR platform guide](https://nextjs.org/docs/app/guides/ppr-platform-guide), [reactCompiler config](https://nextjs.org/docs/app/api-reference/config/next-config-js/reactCompiler) · [Vercel — Next.js on Vercel](https://vercel.com/docs/frameworks/full-stack/nextjs), [Common App Router mistakes](https://vercel.com/blog/common-mistakes-with-the-next-js-app-router-and-how-to-fix-them), [May 2026 security release](https://vercel.com/changelog/next-js-may-2026-security-release) · [vercel/next.js GitHub Releases](https://github.com/vercel/next.js/releases), [Discussion #84842 — middleware rename](https://github.com/vercel/next.js/discussions/84842), [Discussion #95130 — 16.3 preview feedback](https://github.com/vercel/next.js/discussions/95130).

Security: [CVE-2026-44573 — GitLab Advisories](https://advisories.gitlab.com/npm/next/CVE-2026-44573/), [CVE-2026-44574 — GitLab Advisories](https://advisories.gitlab.com/npm/next/CVE-2026-44574/), [CVE-2026-44573 — Miggo](https://www.miggo.io/vulnerability-database/cve/CVE-2026-44573), [CVE-2026-44573 — NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-44573), [Next.js Security Meltdown — byteiota](https://byteiota.com/next-js-security-meltdown-13-cves-middleware-bypass-ssrf/), [16.2.6 fixes writeup — Essa Mamdani](https://essamamdani.com/blog/nextjs-16-2-6-critical-security-fixes-ai-devtools-mcp).

Third-party guides: [App Router in 2026 — DEV](https://dev.to/ottoaria/nextjs-app-router-in-2026-the-complete-guide-for-full-stack-developers-5bjl), [App Router vs Pages Router — Grapes Tech](https://www.grapestechsolutions.com/blog/next-js-routing-app-router-vs-page-router/), [App Router vs Pages Router for SaaS — BuildMVPFast](https://www.buildmvpfast.com/blog/nextjs-app-router-vs-pages-router-saas-2026), [Next.js 16 comprehensive guide — Nandann](https://www.nandann.com/blog/nextjs-16-release-comprehensive-guide), [Next.js 16.2 guide — Nandann](https://www.nandann.com/blog/nextjs-16-2-complete-guide), [16 migration guide — Pockit](https://pockit.tools/blog/nextjs-16-migration-guide-turbopack-proxy-cache-components/), [Turbopack/PPR/cache model — jsmanifest](https://jsmanifest.com/nextjs-16-turbopack-partial-prerendering-cache), [PPR in production — Sam Cheek](https://samcheek.com/blog/nextjs-partial-prerendering-production-2026), [Why Next.js is moving from Middleware — Build with Matija](https://www.buildwithmatija.com/blog/nextjs16-middleware-change), [Server Actions complete guide — MakerKit](https://makerkit.dev/blog/tutorials/nextjs-server-actions), [Server Actions in production — Digital Applied](https://www.digitalapplied.com/blog/nextjs-server-actions-production-patterns-2026-guide), [Server Actions vs Route Handlers — Medium](https://sayhitosumit.medium.com/stop-writing-api-routes-next-js-server-actions-for-mutations-31cfd55cb3fa), [Deploying Next.js apps in 2026 — DEV](https://dev.to/zahg_81752b307f5df5d56035/the-complete-guide-to-deploying-nextjs-apps-in-2026-vercel-self-hosted-and-everything-in-between-48ia), [Self-hosting Next.js — Flightcontrol](https://www.flightcontrol.dev/blog/secret-knowledge-to-self-host-nextjs), [Best Next.js hosting 2026 — MakerKit](https://makerkit.dev/blog/tutorials/best-hosting-nextjs), [29 beginner mistakes — DEV](https://dev.to/azeem_shafeeq/all-29-nextjs-mistakes-beginners-make-56nj), [React Compiler stable guide — Digital Applied](https://www.digitalapplied.com/blog/react-compiler-stable-nextjs-16-automatic-memoization), [React Compiler v1.0 — Econify](https://www.econify.com/news/the-loop-react-compiler-v1-0-automatic-memoization-goes-stable), [16.3 preview — Digital Applied](https://www.digitalapplied.com/blog/nextjs-16-3-agent-native-turbopack-persistent-cache-2026), [16.3 preview — Build with Matija](https://www.buildwithmatija.com/blog/nextjs-16-3-preview-instant-navigations-turbopack-ai), [16.3 preview — Nidhin's blog](https://blog.nidhin.dev/next-js-16-3-preview), [16.3 preview — Onix/Medium](https://medium.com/@onix_react/release-next-js-16-3-fdb243541db5) · [endoflife.date — Next.js](https://endoflife.date/nextjs), [eosl.date — Next.js](https://eosl.date/eol/product/nextjs/).

## openQuestions

1. **Pages Router removal timeline** — no firm deprecation date found; curriculum should give it only a short "here's what it was" note, not a full module.
2. **Deployment Adapter API maturity on non-Vercel platforms** — API is stable, but adapter completeness for Cloudflare/Netlify/AWS wasn't clearly benchmarked; worth a caveat about platform-specific rough edges.
3. **`revalidatePath` vs `revalidateTag` guidance** — may reflect one blog's opinion more than settled consensus; present as current best practice, not immutable law.
4. **Turbopack production build edge cases** — no hard data found on custom Webpack loader/plugin incompatibilities; unlikely to matter for a beginner curriculum.
5. **React Compiler default timeline** — unclear when/if it flips to default; phrase as "available, opt-in."
6. **16.3 stable timing** — expected "in the coming weeks" as of late June 2026; worth a quick re-check if curriculum/site production happens weeks after this research, though current signals suggest 16.3's changes are additive/perf-focused rather than a routing-model change.
