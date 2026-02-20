// Global type declarations for Better Auth to handle dynamic properties
declare module 'better-auth' {
  interface Auth<Config> {
    GET: any;
    POST: any;
    $get: any;
    $post: any;
  }
}