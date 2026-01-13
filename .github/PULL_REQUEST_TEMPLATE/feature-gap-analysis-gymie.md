This pull request implements the MVP changes described in issue #8 (Feature Gap Analysis vs Gymie):

- Adds a `Member` model and JWT-based authentication (with admin/viewer roles)
- Updates activity signups to use member IDs (authenticated)
- Adds `Plan` and `Subscription` models and endpoints
- Adds endpoints for member registration, login, and profile
- Adds a stub endpoint for email notifications
- Adds a simple role model and gates write endpoints for admins
- Demo credentials: see `src/teachers.json`

Implements: #8

---

**Note:** This is an in-memory MVP for demonstration. No persistent storage or real email sending is included.
