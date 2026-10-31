#!/usr/bin/env bash
set -euo pipefail
npm run build
npm run assets
npm run check
npm test
npx --yes wrangler@4.151.1 pages deploy public --project-name readytoprod --branch main --commit-dirty=true
