// Simple test API client without complex authentication
export async function testApiCall() {
  try {
    const response = await fetch('http://localhost:8000/health');
    const data = await response.json();
    console.log('Backend health check:', data);
    return data;
  } catch (error) {
    console.error('Backend connection failed:', error);
    return null;
  }
}