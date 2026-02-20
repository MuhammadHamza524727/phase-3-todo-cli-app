// This file is not used - authentication is handled by the backend API
// The better-auth library is not needed for this project

// import betterAuth from 'better-auth';
// 
// export const auth = betterAuth({
//   emailAndPassword: {
//     enabled: true,
//     requireEmailVerification: false,
//   },
//   socialProviders: {},
//   database: {
//     provider: 'sqlite',
//     url: process.env.DATABASE_URL || './db.sqlite',
//   },
// });
// 
// // Export handlers for Next.js API routes
// export const GET = auth.handler;
// export const POST = auth.handler;