---
name: database-skill
description: Design PostgreSQL schemas, create tables, define relationships/indexes, and manage migrations safely. Use for building scalable, performant database structures in TypeScript/Node.js apps (Neon serverless PostgreSQL preferred).
---
# Database Skill – Create Tables, Migrations, Schema Design
## Instructions
1. **Schema design principles**
   - Normalize to 3NF by default (reduce redundancy, ensure integrity)
   - Use appropriate data types (e.g., uuid/timestamptz/jsonb/text/varchar)
   - Define primary keys (prefer uuid or serial/bigserial)
   - Add foreign keys with ON DELETE/UPDATE CASCADE/RESTRICT as needed
   - Create strategic indexes (B-tree for equality, GIN for jsonb/full-text, partial/functional where useful)

2. **Table creation & relationships**
   - Use declarative schema in code (Drizzle schema.ts or Prisma schema.prisma)
   - Colocate timestamps (created_at/updated_at with defaults/triggers)
   - Support soft deletes (deleted_at column + unique constraints)
   - Handle enums via CHECK constraints or native ENUM types
   - Design for Neon: favor small/frequent migrations, test on branches

3. **Migrations management**
   - Prefer Drizzle Kit (generate SQL from TS schema, manual edits possible)
   - Or Prisma Migrate (declarative schema → auto SQL diff)
   - Make migrations idempotent/small/focused (one change per file)
   - Use transactions; test in isolation (Neon branches ideal)
   - Version control migrations alongside code
   - Handle data migrations (backfills, renames) safely

## Best Practices
- Prefer Drizzle ORM for SQL-close control + type safety in 2026 projects
- Use Prisma for rapid prototyping or when declarative schema is preferred
- Always add indexes for frequent WHERE/JOIN/ORDER BY columns
- Avoid over-normalization (denormalize for read-heavy queries if needed)
- Use jsonb for flexible/semi-structured data
- Include constraints (NOT NULL, UNIQUE, CHECK) for data integrity
- Design with performance in mind: right column types, avoid wide tables if possible
- Test schema changes on Neon branch before main
- Document schema decisions & migration rationale

## Example Structure – Drizzle ORM (recommended modern approach 2026)

```ts
// schema.ts – Drizzle schema definition
import { pgTable, uuid, text, timestamp, boolean, serial, index, foreignKey, pgEnum } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

// Enums example
export const roleEnum = pgEnum("role", ["user", "admin", "moderator"]);

// Users table
export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  email: text("email").notNull().unique(),
  passwordHash: text("password_hash").notNull(),
  name: text("name"),
  role: roleEnum("role").notNull().default("user"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow().$onUpdate(() => new Date()),
  deletedAt: timestamp("deleted_at", { withTimezone: true }),
}, (table) => ({
  emailIdx: index("users_email_idx").on(table.email),
}));

// Posts table (example relation)
export const posts = pgTable("posts", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  content: text("content").notNull(),
  authorId: uuid("author_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  published: boolean("published").notNull().default(false),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
}, (table) => ({
  authorIdx: index("posts_author_idx").on(table.authorId),
}));

// Relations (for queries)
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));