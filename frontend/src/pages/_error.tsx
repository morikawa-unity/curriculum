import { NextPageContext } from 'next'

interface ErrorPageProps {
  statusCode?: number
  hasGetInitialProps?: boolean
  err?: Error
}

function ErrorPage({ statusCode }: ErrorPageProps) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-4">
        {statusCode ? statusCode : 'Client-side error occurred'}
      </h1>
      <p className="text-gray-600 mb-4">
        {statusCode === 404
          ? 'This page could not be found.'
          : 'An unexpected error has occurred.'}
      </p>
      <a
        href="/"
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Go back home
      </a>
    </div>
  )
}

ErrorPage.getInitialProps = ({ res, err }: NextPageContext) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404
  return { statusCode }
}

export default ErrorPage