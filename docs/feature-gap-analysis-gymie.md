# Feature Gap Analysis vs Gymie (Club Management)

## 1. Features Already Covered
- Activities catalog (name, description, schedule, capacity)
- Signup/unregister and participant counts

## 2. Features Missing (Gaps)
### Members Directory and Profiles
- Member management (students, teachers)
- Profiles with contact info, status

### Enquiries & Follow-ups
- Track prospective students
- Follow-up reminders

### Plans & Services
- Membership tiers, passes
- Activity/service bundles

### Subscriptions Lifecycle
- Create/change/renew/cancel subscriptions
- Expiring/expired views

### Invoices & Payments
- Track payments, discounts, states (paid/unpaid/partial/overpaid)

### Expenses & Categories
- Club budgets, expense tracking

### Notifications
- Email/SMS triggers for renewals, reminders, birthdays

### Roles & Permissions
- Admin, officer, advisor, student roles
- Access control for actions

### Settings, Reports, API Auth, Scheduler
- Organization settings, templates
- Analytics and reporting
- JWT-based API authentication
- Scheduled jobs (e.g., reminders)

## 3. Proposed MVP + Phased Roadmap
### MVP
- Member model + email-based auth (simple JWT)
- Connect signups to member IDs
- Basic plans and subscriptions (with capacity rules)
- Expiring/expired queries
- Email notification hooks (signup confirmation, expiry reminders)
- Basic role model (admin vs viewer)

### Phase 2
- Enquiries/follow-ups
- More advanced plans/services
- Invoices/payments stub
- Expense tracking
- SMS notifications
- Advanced roles/permissions
- Reports/analytics

## 4. API Endpoints & Data Model Changes (MVP)
- `POST /members` – create member
- `POST /auth/login` – login, returns JWT
- `GET /members/{id}` – get member profile
- `POST /plans` – create plan
- `POST /subscriptions` – create subscription
- `GET /subscriptions?status=expiring` – list expiring subscriptions
- `POST /notifications/email` – send notification
- `GET /activities` – (existing)
- `POST /activities/{activity_name}/signup` – (existing, now links to member)

## 5. Backlog Items (with Sizing)
| Feature                | Description                                 | Endpoints                | Data Schema Notes         | Effort |
|------------------------|---------------------------------------------|--------------------------|--------------------------|--------|
| Member model & auth    | Add member entity, JWT login                | /members, /auth/login    | Member, JWT              | M      |
| Plans & subscriptions  | Add plans, link to activities, expiry rules | /plans, /subscriptions   | Plan, Subscription       | M      |
| Notifications (email)  | Email on signup/expiry                      | /notifications/email     | EmailTemplate, Trigger   | S      |
| Roles/permissions      | Admin vs viewer, gate write endpoints       | (middleware)             | Role, Permission         | S      |
| Enquiries/follow-ups   | Track prospects, reminders                  | /enquiries               | Enquiry, FollowUp        | M      |
| Invoices/payments      | Track payments, stub only                   | /invoices, /payments     | Invoice, Payment         | L      |
| Expenses               | Track club expenses                         | /expenses                | Expense, Category        | L      |

## 6. Wireframe/Sequence (Optional)
- Membership renewal reminder flow (see issue for details)

---

*This report maps Gymie modules to the extracurricular domain, highlights gaps, and proposes a phased roadmap for implementation.*
