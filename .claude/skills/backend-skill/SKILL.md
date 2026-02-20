---
name: backend-skill
description: Generate clean RESTful routes, handle requests/responses with validation, and connect to databases (PostgreSQL/Neon preferred) in TypeScript backends. Use for building performant, type-safe APIs with Hono (modern default), or alternatives like Fastify/NestJS.
---
# Backend Skill – Generate Routes, Handle Requests/Responses, Connect to DB
## Instructions
1. **Route generation & structure**
   - Use RESTful conventions (GET/POST/PUT/PATCH/DELETE)
   - Group routes by domain/feature (e.g., /users, /posts) via routers/groups
   - Support path params, query strings, JSON bodies
   - Prefer async handlers for DB I/O

2. **Request/response handling**
   - Validate inputs with Zod/Valibot (type inference for safety)
   - Return typed JSON responses (status codes, error shapes)
   - Handle errors centrally (custom error classes, 4xx/5xx responses)
   - Add middleware for logging, CORS, rate limiting, auth

3. **Database connection & usage**
   - Use dependency injection/context for DB clients (e.g., Drizzle db instance)
   - Prefer async/await with transactions where needed
   - Integrate with Neon/PostgreSQL via Drizzle ORM (type-safe queries)
   - Support connection pooling, prepared statements, migrations

## Best Practices
- Prefer Hono in 2026 for speed, tiny size, runtime flexibility (Node/Bun/Deno/Cloudflare), and clean TypeScript DX
- Use Zod for schema validation → auto-infer types for req/res
- Keep handlers small & focused (extract services/logic)
- Always type responses (success + error unions)
- Secure defaults: validate all inputs, use prepared queries to prevent SQL injection
- Add OpenAPI/Swagger via plugins when docs needed
- Test routes with type-safe clients (Eden for Elysia-like if using alternatives)
- For larger/enterprise apps: consider NestJS for modular structure (controllers/modules)
- Integrate seamlessly with Better Auth (handler mounting) and Drizzle (db queries)

## Example Structure – Hono (recommended modern approach 2026)

```ts
// src/index.ts – Main app entry
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'
import { db } from './db' // Drizzle instance
import { users } from './schema' // Drizzle schema
import { eq } from 'drizzle-orm'
import { auth } from './auth' // Better Auth instance

const app = new Hono<{ Variables: { user?: any } }>()

// Mount Better Auth handler (from your Auth Skill)
app.route('/api/auth', auth.handler)

// Middleware example: auth guard
const authMiddleware = async (c, next) => {
  const session = await auth.api.getSession({ headers: c.req.raw.headers })
  if (!session) return c.json({ error: 'Unauthorized' }, 401)
  c.set('user', session.user)
  await next()
}

// Example: GET /users/:id – Protected route
app.get('/users/:id', authMiddleware, zValidator('param', z.object({ id: z.string().uuid() })), async (c) => {
  const { id } = c.req.valid('param')
  const [user] = await db.select().from(users).where(eq(users.id, id)).limit(1)

  if (!user) return c.json({ error: 'User not found' }, 404)
  return c.json({ data: { id: user.id, email: user.email, name: user.name } })
})

// Example: POST /users – Signup-like (validation + DB insert)
const createUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(1).optional(),
})

app.post('/users', zValidator('json', createUserSchema), async (c) => {
  const data = c.req.valid('json')

  // In real app, use Better Auth signup here
  // For demo: direct DB insert (hash password!)
  const [newUser] = await db.insert(users).values({
    email: data.email,
    passwordHash: 'hashed_via_better_auth', // placeholder
    name: data.name,
  }).returning()

  return c.json({ data: { id: newUser.id, email: newUser.email } }, 201)
})

// Error handling middleware (global)
app.onError((err, c) => {
  console.error(err)
  return c.json({ error: 'Internal Server Error' }, 500)
})

export default app