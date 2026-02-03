import React from 'react';

interface ErrorAlertProps {
  message: string;
  onClose?: () => void;
  isVisible?: boolean;
}

const ErrorAlert: React.FC<ErrorAlertProps> = ({
  message,
  onClose,
  isVisible = true
}) => {
  if (!isVisible || !message) {
    return null;
  }

  return (
    <div
      className={`
        bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4
        transform transition-all duration-300 ease-in-out
        animate-fadeIn
      `}
      role="alert"
    >
      <div className="flex items-start">
        <svg
          className="fill-current h-6 w-6 text-red-500 mr-3 flex-shrink-0"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
            clipRule="evenodd"
          />
        </svg>
        <div>
          <p className="font-bold">Error</p>
          <p>{message}</p>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="ml-auto text-red-700 hover:text-red-900 focus:outline-none"
            aria-label="Close"
          >
            <svg
              className="h-6 w-6"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorAlert;