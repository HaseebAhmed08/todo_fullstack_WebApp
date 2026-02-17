import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const formData = await request.json();
    
    // Forward the login request to Better Auth
    const authResponse = await fetch(`${process.env.BETTER_AUTH_BASE_URL || 'http://localhost:8000/api/auth'}/sign-in/email`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: formData.email,
        password: formData.password,
      }),
    });

    const data = await authResponse.json();

    return NextResponse.json(data, {
      status: authResponse.status,
    });
  } catch (error) {
    console.error('Login proxy error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}