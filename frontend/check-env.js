// Script to check environment variables
console.log('Environment Variables Check:');
console.log('NODE_ENV:', process.env.NODE_ENV);
console.log('NEXT_PUBLIC_API_BASE_URL:', process.env.NEXT_PUBLIC_API_BASE_URL);
console.log('FRONTEND_URL:', process.env.FRONTEND_URL);
console.log('BACKEND_URL:', process.env.BACKEND_URL);

// Verify that required environment variables are present
const requiredVars = ['NEXT_PUBLIC_API_BASE_URL'];
const missingVars = requiredVars.filter(varName => !process.env[varName]);

if (missingVars.length > 0) {
  console.error('❌ Missing required environment variables:', missingVars);
  process.exit(1);
} else {
  console.log('✅ All required environment variables are set');
}

// Check if API_BASE_URL has a valid format
const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
if (apiUrl && (apiUrl.startsWith('http://localhost') || apiUrl.includes('.local') || apiUrl.includes('undefined'))) {
  console.warn('⚠️  Warning: API URL might not be set for production');
} else if (apiUrl) {
  console.log(`✅ API Base URL is set to: ${apiUrl}`);
}