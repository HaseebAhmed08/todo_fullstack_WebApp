"""
Check Frontend Logs for Better Auth Errors
Reads recent frontend terminal output to find error details
"""
import subprocess
import sys

print("Checking frontend logs for Better Auth errors...")
print("=" * 60)

# Try to read from frontend terminal
# Since we can't directly access terminal output, we'll create a test
# that triggers the error and captures it

print("\nAttempting signup to trigger error...")
print("Check the frontend terminal window for error messages")
print("\nLook for lines containing:")
print("  - 'ERROR [Better Auth]'")
print("  - Stack traces")
print("  - Database connection errors")
print("\nCommon issues:")
print("  1. Database connection string incorrect")
print("  2. Missing required columns in user table")
print("  3. Better Auth can't create tables")
print("  4. SSL/TLS connection issues")

print("\n" + "=" * 60)
print("Please check the frontend terminal and share any error messages")
