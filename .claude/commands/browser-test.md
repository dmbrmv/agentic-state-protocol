---
description: Test web application in Chrome browser
argument-hint: [url-or-action]
---

# /browser-test - Chrome Browser Testing

## Pre-computed Context

Package.json scripts:
!`cat package.json 2>/dev/null | grep -A 20 '"scripts"' | head -25 || echo "No package.json"`

Framework detection:
!`cat package.json 2>/dev/null | grep -E '"(react|vue|angular|svelte|next|nuxt)"' | head -5 || echo "Unknown framework"`

Current dev server:
!`lsof -i :3000,:5173,:8080,:4200 2>/dev/null | grep LISTEN | head -3 || echo "No dev server detected"`

## Task

Test web application in Chrome browser.

**Action/URL**: $ARGUMENTS

### Prerequisites

1. **Chrome Browser**: Must be installed
2. **Claude Chrome Extension**: Required for `--chrome` flag
3. **Dev Server**: Application should be running locally

### Common Dev Server URLs

| Framework | Command | URL |
|-----------|---------|-----|
| React (CRA) | `npm start` | http://localhost:3000 |
| React (Vite) | `npm run dev` | http://localhost:5173 |
| Next.js | `npm run dev` | http://localhost:3000 |
| Vue (Vite) | `npm run dev` | http://localhost:5173 |
| Vue (CLI) | `npm run serve` | http://localhost:8080 |
| Angular | `ng serve` | http://localhost:4200 |
| Svelte | `npm run dev` | http://localhost:5173 |

### Testing Actions

#### If URL provided:
Navigate to the URL and verify:
- Page loads without errors
- Console is clean (no errors)
- UI renders correctly
- Core functionality works

#### Common Test Actions:

**"test login flow"**
1. Navigate to login page
2. Enter test credentials
3. Submit form
4. Verify redirect to dashboard
5. Check for errors

**"check console errors"**
1. Open application
2. Navigate through main pages
3. Open DevTools Console
4. Report any errors or warnings

**"verify UI"**
1. Load the application
2. Check visual rendering
3. Test responsive breakpoints
4. Verify no layout issues

**"test form submission"**
1. Navigate to form
2. Fill in test data
3. Submit
4. Verify success/error handling

**"check performance"**
1. Open DevTools Performance
2. Record page load
3. Report metrics (LCP, FID, CLS)

### Output Format

```
## Browser Test Results

### Environment
- URL: [url tested]
- Browser: Chrome
- Dev Server: [running/not running]

### Console Check
- Errors: [count]
- Warnings: [count]
- Details: [list significant issues]

### Visual Check
- Layout: OK/Issues
- Responsive: OK/Issues
- Assets: OK/Missing

### Functionality Check
- [Feature]: PASS/FAIL
- [Feature]: PASS/FAIL

### Performance (if checked)
- LCP: [value]
- FID: [value]
- CLS: [value]

### Screenshots
[Describe any captured evidence]

### Verdict
[SHIP IT | FIX REQUIRED | INVESTIGATE]
```

### Without Chrome Extension

If Chrome extension not available:
1. Start the dev server manually
2. Open the URL in browser
3. Follow the test steps manually
4. Report findings back

```bash
# Start dev server
npm run dev

# Open in browser
open http://localhost:5173  # macOS
xdg-open http://localhost:5173  # Linux
```
