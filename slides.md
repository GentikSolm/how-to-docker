---
author: Josh Brown
---
# Notes on projects
## Folder Structure

- Nested base project folders should have purpose.
- If your project has separate services (for example, an api that is separate from the UI), then each service should live in a subfolder labeled appropriately. 
- If your project is one service, no need to nest the project recursively. 
- Ex. ~/github/myproject vs ~/github/myproject/myproject

## .gitignore
- Look up .gitignore templates for your project
- Anything that changes during build / runtime generally should be ignored
- Anything that can be installed during setup should be ignored

- Common examples
    - `node_modules`
    - `__pycache__`
    - `.env`
    - `build/`
    - `dist/`

*Note: these will generally also apply to .dockerignore*

---
# Notes on projects
## Branches
- Decide on a branching strategy
- I personally recommend the `github` flow for most teams
- A branch is not your branch
- Establishing naming patterns for your team can help a lot
- Writing down issues on gh can also help with this
    - Ex. for brunus projects, we use the convention `[type]/[issue #]-[desc]`

## Comment on CRA

**Stop using Create React App, And get off of it, if you can**

### Why?
- Very slow, compared to newer alternatives
- Massive footprint
- Outdated and insecure
- Does not play well with plugins (TS, Tailwind, etc.)

### Alternatives

Are you making a SPA?
- Vite
- Nx

Want SSR / non SPA?
- Next.js
- Remix.js
- Astro (can be non-react too)


---
# What is docker?

---
# Before Docker

---
# Container era

---
# Problems Docker Solves

---
# The Dockerfile

---
# Docker CLI

---
# Docker Compose
