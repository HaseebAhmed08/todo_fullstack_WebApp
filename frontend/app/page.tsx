'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import Link from 'next/link';
import LoadingSpinner from '@/components/LoadingSpinner';
import { CheckCircle, Zap, Shield, Sparkles } from 'lucide-react';

export default function HomePage() {
  const router = useRouter();
  const { session, loading } = useAuth();

  // If user is already authenticated, redirect to dashboard
  useEffect(() => {
    if (!loading && session) {
      router.push('/dashboard');
    }
  }, [session, loading, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <LoadingSpinner size="lg" color="blue" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      {/* Navigation */}
      <nav className="fixed w-full z-50 bg-white/80 backdrop-blur-md border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center space-x-2">
              <div className="p-1.5 bg-yellow-500 rounded-lg">
                <CheckCircle className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-yellow-600 to-orange-600">
                Todo Evolution
              </span>
            </div>
            <div className="flex space-x-4">
              <Link href="/signin" className="px-4 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors">
                Sign In
              </Link>
              <Link href="/signup" className="px-4 py-2 text-sm font-medium text-white bg-yellow-500 hover:bg-yellow-600 rounded-lg shadow-sm shadow-yellow-200 transition-all hover:scale-105 active:scale-95">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 -z-10 bg-yellow-400/10 blur-[120px] rounded-full w-[600px] h-[600px]" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-yellow-100 text-yellow-700 text-sm font-medium mb-8 animate-fade-in">
            <Sparkles className="h-4 w-4 mr-2" />
            Phase II is here with Better Auth Cloud
          </div>

          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6">
            Organize your life <br />
            <span className="text-yellow-500">one task</span> at a time.
          </h1>

          <p className="max-w-2xl mx-auto text-xl text-slate-600 mb-10 leading-relaxed">
            The next evolution of task management. Simple, secure, and soon-to-be AI-powered.
            Built with Next.js 15, FastAPI, and Better Auth.
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link href="/signup" className="px-8 py-4 bg-yellow-500 text-white rounded-xl text-lg font-bold shadow-lg shadow-yellow-200 hover:bg-yellow-600 transition-all hover:-translate-y-1">
              Start for Free
            </Link>
            <Link href="/signin" className="px-8 py-4 bg-white text-slate-700 border border-slate-200 rounded-xl text-lg font-bold hover:bg-slate-50 transition-all">
              Login to Dashboard
            </Link>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="p-8 rounded-2xl bg-slate-50 border border-slate-100 group hover:border-yellow-200 hover:shadow-xl transition-all">
              <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center text-yellow-600 mb-6 group-hover:scale-110 transition-transform">
                <Zap />
              </div>
              <h3 className="text-xl font-bold mb-3">Lightning Fast</h3>
              <p className="text-slate-600">Built on a distributed architecture using FastAPI and Neon Serverless for sub-100ms response times.</p>
            </div>

            <div className="p-8 rounded-2xl bg-slate-50 border border-slate-100 group hover:border-yellow-200 hover:shadow-xl transition-all">
              <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center text-yellow-600 mb-6 group-hover:scale-110 transition-transform">
                <Shield />
              </div>
              <h3 className="text-xl font-bold mb-3">Military-Grade Auth</h3>
              <p className="text-slate-600">Powered by Better Auth with session management and cross-origin JWT verification.</p>
            </div>

            <div className="p-8 rounded-2xl bg-slate-50 border border-slate-100 group hover:border-yellow-200 hover:shadow-xl transition-all">
              <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center text-yellow-600 mb-6 group-hover:scale-110 transition-transform">
                <Sparkles />
              </div>
              <h3 className="text-xl font-bold mb-3">AI Ready</h3>
              <p className="text-slate-600">Future-proof architecture ready for Phase III chatbot integration in the coming weeks.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 border-t border-slate-100">
        <div className="max-w-7xl mx-auto px-4 text-center text-slate-500 text-sm">
          &copy; 2026 Todo Evolution Project. Built for Hackathon II.
        </div>
      </footer>
    </div>
  );
}
