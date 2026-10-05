# Concrete Tailwind patterns

These patterns target Tailwind v4. Use the application's installed version and current official framework guide. Do not mix v3 configuration or `@tailwind` directives into a v4 setup. These examples provide styling; wire their behavior to the application contracts.

## Build integration

Run installation commands from the application source directory using its existing package manager. The npm commands below are examples.

For Vite:

```sh
npm install -D tailwindcss @tailwindcss/vite
```

Add the plugin alongside the project's existing plugins:

```ts
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [tailwindcss()], // Retain existing framework plugins here.
});
```

For a PostCSS-based framework such as Next.js:

```sh
npm install -D tailwindcss @tailwindcss/postcss postcss
```

Merge the plugin into the existing PostCSS configuration:

```js
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

Import Tailwind once in the application's global stylesheet:

```css
@import "tailwindcss";
```

Import that stylesheet from the framework's entry point or root layout. Confirm the framework's supported Node version and source-detection paths. Build CSS through the framework integration; the browser Play CDN is for development demonstrations.

Official guides: [Vite](https://tailwindcss.com/docs/installation/using-vite), [PostCSS](https://tailwindcss.com/docs/installation/using-postcss), [Play CDN](https://tailwindcss.com/docs/installation/play-cdn).

## Semantic theme

Adapt [uiTheme.css](../assets/uiTheme.css) into the application's global stylesheet. Its `@theme inline` mappings produce utilities such as `bg-canvas`, `bg-surface`, `text-ink`, `text-muted`, `border-line`, and `focus-visible:ring-accent`.

The eight colors cover backgrounds, text, actions, boundaries, and errors. Keep values consistent across components. Light/dark values follow the OS until an explicit `data-theme="light"` or `data-theme="dark"` attribute is set on the root `<html>` element. If a manual theme control is included in scope, frontend implements its state and persistence separately.

These semantic utilities already respond to the theme variables; they do not require `dark:` duplicates. Use the application's existing dark-mode configuration when extending an existing design.

See [theme variables](https://tailwindcss.com/docs/theme) and [dark mode](https://tailwindcss.com/docs/dark-mode).

## Layout and controls

The markup below illustrates an error state. Adapt content, IDs, class strings, and state logic to the actual feature. In JSX, use `className`, `htmlFor`, and the framework's event handlers.

```html
<main class="min-h-screen bg-canvas text-ink">
  <div class="mx-auto flex max-w-6xl flex-col gap-8 px-4 py-8 sm:px-6 lg:px-8">
    <header class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div class="flex flex-col gap-2">
        <h1 class="text-3xl font-semibold tracking-tight">Tasks</h1>
        <p class="max-w-prose text-base leading-7 text-muted">Plan your next action.</p>
      </div>
      <a href="#task-title" class="inline-flex min-h-11 items-center justify-center rounded-md bg-accent px-4 py-2 text-sm font-semibold text-on-accent hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-canvas">
        Add a task
      </a>
    </header>

    <div class="grid grid-cols-1 items-start gap-6 lg:grid-cols-2">
      <section aria-labelledby="create-heading" class="flex min-w-0 flex-col gap-4 rounded-lg border border-line bg-surface p-5 sm:p-6">
        <h2 id="create-heading" class="text-xl font-semibold">New task</h2>
        <form class="flex flex-col gap-4">
          <div class="flex flex-col gap-2">
            <label for="task-title" class="text-sm font-medium">Title</label>
            <input id="task-title" name="title" type="text" required maxlength="120" aria-invalid="true" aria-describedby="title-help title-error" class="min-h-11 w-full rounded-md border border-line bg-surface px-3 py-2 text-base text-ink placeholder:text-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent aria-invalid:border-danger" />
            <p id="title-help" class="text-sm text-muted">Use 1–120 characters.</p>
            <p id="title-error" class="text-sm text-danger">Enter a title.</p>
          </div>
          <button type="submit" class="inline-flex min-h-11 items-center justify-center rounded-md bg-accent px-4 py-2 text-sm font-semibold text-on-accent hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-surface disabled:cursor-not-allowed disabled:opacity-50">
            Create task
          </button>
          <p role="status" class="text-sm text-muted"></p>
        </form>
      </section>

      <section aria-labelledby="list-heading" class="flex min-w-0 flex-col gap-4 rounded-lg border border-line bg-surface p-5 sm:p-6">
        <h2 id="list-heading" class="text-xl font-semibold">Your tasks</h2>
        <div class="rounded-md border border-dashed border-line p-6 text-center text-muted">
          No tasks yet. Create your first task to get started.
        </div>
      </section>
    </div>
  </div>
</main>
```

State behavior belongs to the contract:

| State | Concrete presentation | Required behavior |
|---|---|---|
| Pending | `disabled`, `aria-busy="true"`, label “Creating…” | Prevent repeat submission and announce progress through the status region. |
| Invalid | `aria-invalid="true"`, `aria-describedby`, `text-danger` | Show the associated error; retain entered values. Remove invalid attributes and error content when resolved. |
| Success | Updated list and status message | Display the returned record and clear the form only after contracted success. |
| Empty | Bordered message with a useful next action | Distinguish no records from a failed request. |
| Failed request | Error text with a retry action when supported | Preserve user input and follow the contract's retry behavior. |

For wide tables, use an `overflow-x-auto` wrapper and a semantic `<table>`; ensure the scroll region is keyboard-accessible and labelled when necessary. Keep the rest of the page within the viewport. Use `motion-reduce:transition-none` if adding nonessential transitions.

## Class generation

Use full class strings in source. In a JavaScript component:

```js
const statusClasses = {
  open: "border-line bg-surface text-ink",
  completed: "border-accent bg-accent/10 text-ink",
};
```

Avoid fragments such as `bg-${color}-500`; Tailwind detects class names as text rather than evaluating expressions. Register external/shared source locations when automatic detection does not include them. See [source detection](https://tailwindcss.com/docs/detecting-classes-in-source-files).

## Verification

- Run the actual application build and confirm custom semantic utilities are generated and the stylesheet is loaded.
- Check the affected screen at a narrow mobile width and a wide desktop width, including long labels and content. Verify overflow and breakpoint behavior.
- Navigate by keyboard; check focus visibility, labels, error associations, and status announcements. Test actual interactions rather than only reviewing class strings.
- Check the required states and text/control contrast in both themes. If manual theme selection exists, verify it overrides the OS preference.
- Link evidence to the current increment and acceptance/contract IDs. Mark unavailable browser checks unverified; compilation alone does not prove usability.
