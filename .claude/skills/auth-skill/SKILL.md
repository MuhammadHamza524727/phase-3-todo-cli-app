---
name: auth-skill
description: Implement secure user authentication flows: signup, signin, password hashing, sessions/JWT tokens, and full Better Auth integration. Use for building modern, type-safe auth systems in TypeScript apps (Next.js, Hono, Express, etc.).
---
# Auth Skill – Signup, Signin, Password Hashing, JWT Tokens & Better Auth
## Instructions
1. **Core flows to implement**
   - User signup (email/password, optional fields like name, image)
   - User signin (email/password credentials)
   - Secure password hashing & verification (argon2id default in Better Auth)
   - Session management (cookie-based, httpOnly, secure, sameSite)
   - JWT token support (stateless bearer tokens via JWT plugin)
   - Token refresh/revocation when using JWT strategy

2. **Better Auth integration (strongly preferred modern approach)**
   - Install: npm install better-auth
   - Create central auth instance: betterAuth({ ... })
   - Enable emailAndPassword plugin (built-in hashing, rate limiting, verification)
   - Add plugins as needed: jwt(), bearer(), magicLink(), passkey(), twoFactor(), organization()
   - Mount handler for framework (Next.js App Router: auth.handlers; Hono/Express: toHandler(auth))
   - Use client SDK: createAuthClient() for signUp.email(), signIn.email(), useSession(), signOut()
   - Leverage type inference ($InferAuth, inferAdditionalFields for custom session/user fields)

3. **Security & best practices**
   - Never store plain passwords — Better Auth uses argon2id by default
   - Use secure cookies (httpOnly, secure, sameSite: 'strict'/'lax')
   - Enable rate limiting & brute-force protection (built-in or via plugin)
   - Validate inputs strictly (email format, password strength ≥8 chars default)
   - Support email verification, 2FA (TOTP), magic links, passkeys when relevant
   - Use strong secret (BETTER_AUTH_SECRET ≥32 chars, rotate periodically)
   - For APIs: prefer JWT + bearer plugin with JWKS endpoint for verification
   - Minimize session data exposure (only id, email, role, etc.)

## Best Practices
- Prefer Better Auth over manual implementations (less boilerplate, better security defaults, plugins for advanced flows)
- Use Server Components / edge runtime where possible (Better Auth supports it well)
- Auto-signin after signup unless verification is required
- For custom fields (e.g. role): use inferAdditionalFields on client to keep types safe
- Always handle errors gracefully (Better Auth returns typed errors)
- Log auth events only — never passwords or tokens
- Mobile-first & accessible forms (labels, password toggle, ARIA)
- Prefer database-backed sessions by default; use JWT plugin for stateless API auth

## Example Structure – Better Auth (recommended 2026 approach)

```ts
// lib/auth.ts – Central auth config (server-side)
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";           // for JWT support
// import { bearer } from "better-auth/plugins";    // optional bearer strategy
// import { twoFactor } from "better-auth/plugins"; // etc.

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
  emailAndPassword: {
    enabled: true,
    autoSignIn: true,
    minPasswordLength: 8,
    // rateLimit: { ... }, requireEmailVerification: true, etc.
  },
  plugins: [
    jwt(),                    // exposes /token & JWKS endpoints
    // bearer(),
    // magicLink(), passkey(), twoFactor(), organization(), etc.
  ],
  // database: your adapter (drizzle, prisma, kysely, etc.)
});

// Next.js App Router example: app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth";
export const { GET, POST } = auth.handlers;