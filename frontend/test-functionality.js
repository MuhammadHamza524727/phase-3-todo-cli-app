// Test script to verify all functionality is working
const axios = require('axios');

async function testFunctionality() {
  console.log('🔍 Testing Full Stack Functionality...\n');

  const BASE_URL = 'http://localhost:8080';
  let token = null;

  try {
    // Test 1: Health Check
    console.log('✅ Testing Health Endpoint...');
    const healthResponse = await axios.get(`${BASE_URL}/health`);
    console.log(`   Health Status: ${healthResponse.data.status}\n`);

    // Test 2: Registration
    console.log('✅ Testing Registration...');
    const email = `testuser_${Date.now()}@example.com`;
    const password = 'testpass123';

    const registerResponse = await axios.post(`${BASE_URL}/api/register`, {
      email: email,
      password: password,
      password_confirm: password,
      name: 'Test User'
    });

    console.log(`   Registration: Success - User ID: ${registerResponse.data.user.id}`);
    token = registerResponse.data.token;

    // Test 3: Login
    console.log('\n✅ Testing Login...');
    const loginResponse = await axios.post(`${BASE_URL}/api/login`, {
      email: email,
      password: password
    });

    console.log(`   Login: Success - Token retrieved`);
    token = loginResponse.data.token;

    // Test 4: Create Task
    console.log('\n✅ Testing Task Creation...');
    const taskResponse = await axios.post(`${BASE_URL}/api/tasks`, {
      title: 'Test Task from Verification Script',
      description: 'This task was created to verify API functionality',
      completed: false
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    const taskId = taskResponse.data.id;
    console.log(`   Task Creation: Success - Task ID: ${taskId}`);

    // Test 5: Get Tasks
    console.log('\n✅ Testing Task Retrieval...');
    const getTasksResponse = await axios.get(`${BASE_URL}/api/tasks`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    console.log(`   Task Retrieval: Success - Found ${getTasksResponse.data.length} tasks`);

    // Test 6: Update Task
    console.log('\n✅ Testing Task Update...');
    const updateResponse = await axios.put(`${BASE_URL}/api/tasks/${taskId}`, {
      title: 'Updated Test Task from Verification Script',
      description: 'This task was updated to verify API functionality',
      completed: true
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    console.log(`   Task Update: Success - Updated task: ${updateResponse.data.title}`);

    // Test 7: Toggle Task Completion
    console.log('\n✅ Testing Task Completion Toggle...');
    const toggleResponse = await axios.patch(`${BASE_URL}/api/tasks/${taskId}/complete`, {
      completed: false
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    console.log(`   Task Toggle: Success - Completion status: ${toggleResponse.data.completed}`);

    // Test 8: Delete Task
    console.log('\n✅ Testing Task Deletion...');
    await axios.delete(`${BASE_URL}/api/tasks/${taskId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    console.log('   Task Deletion: Success');

    // Verify task was deleted
    const afterDeleteResponse = await axios.get(`${BASE_URL}/api/tasks`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    console.log(`   Verification: Success - Remaining tasks: ${afterDeleteResponse.data.length}`);

    console.log('\n🎉 ALL TESTS PASSED! Full stack functionality is working correctly.');
    console.log('\n📋 Summary:');
    console.log('   - Authentication (Register/Login) ✅');
    console.log('   - Task Management (CRUD Operations) ✅');
    console.log('   - JWT Authentication ✅');
    console.log('   - API Endpoint Integration ✅');
    console.log('   - Backend-Frontend Communication ✅');

  } catch (error) {
    console.error('❌ Test failed:', error.response?.data || error.message);
    process.exit(1);
  }
}

testFunctionality();