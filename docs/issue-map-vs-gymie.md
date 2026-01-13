Title: Feature Gap Analysis vs Gymie (Club Management)

Summary
- Compare our current Activities API against Gymie’s feature set to identify gaps and propose additions suitable for extracurricular/club management.

Background
- Our repo provides a simple FastAPI app for viewing activities and signing up/unregistering students:
  - Endpoints:
    - GET `/activities`
    - POST `/activities/{activity_name}/signup?email=…`
    - DELETE `/activities/{activity_name}/unregister?email=…`
  - In-memory data model; no auth, roles, billing, or comms.
- Gymie (https://github.com/lubusIN/laravel-gymie, https://gymie.in/) implements a full club/gym management suite including members, enquiries/follow-ups, plans/services, subscriptions, invoices/payments, expenses, SMS/email, ACL, settings, reports, API, and cron-driven automations.

Goals
- Map Gymie modules to an extracurricular program context and highlight deltas vs our app.
- Produce a prioritized list of new features to implement incrementally in our stack.

Out of Scope
- Full Laravel/Gymie adoption or port.
- Building a payments pipeline in this issue (can be split out).

Deliverables
- A short report (markdown) listing:
  1) Features we already cover
  2) Features missing (gaps) grouped by modules
  3) A proposed MVP+phased roadmap with API endpoints and data model changes
- Optional: Wireframe sketches or sequence diagrams for 1–2 critical flows (e.g., membership renewal reminders).

Acceptance Criteria
- The report clearly maps Gymie modules to our domain (student clubs/extracurriculars).
- A ranked backlog exists with at least: Members, Plans, Subscriptions, Notifications, and Roles.
- Each backlog item includes: brief description, proposed endpoints, data schema notes, and effort sizing (S/M/L).
- Team signs off on the next two milestones.

Initial Feature Mapping (reference)
- Already in our app:
  - Activities catalog (name, description, schedule, capacity)
  - Signup/unregister and participant counts
- New vs Gymie (gaps):
  - Members directory and profiles
  - Enquiries + follow-ups (prospective students → members)
  - Plans & services (tiers, passes)
  - Subscriptions lifecycle (create/change/renew/cancel; expiring/expired views)
  - Invoices & payments (states: paid/unpaid/partial/overpaid; discounts)
  - Expenses & categories (club budgets)
  - Notifications: SMS/email triggers/events (renewals, reminders, birthdays)
  - Roles & permissions (officers/advisors/admins)
  - Settings (org, templates), Reports/analytics, API auth (JWT), scheduler jobs

Suggested Next Steps
1) Define “Member” model + auth (email-based, simple JWT) and connect signups to member IDs (M)
2) Add Plans + basic Subscriptions with capacity rules and expiring/expired queries (M)
3) Notification hooks (email first) for signup confirmation and upcoming expiry (S)
4) Basic role model (admin vs viewer) gating write endpoints (S)
5) Stretch: Expenses tracking and invoices/payments stub (L; separate issue)

Labels
- enhancement, analysis, planning

References
- Gymie routes snapshot (members/enquiries/followups/plans/services/subscriptions/invoices/payments/expenses/sms/settings/acl/api)
- Our code: `src/app.py`, `src/static/`
