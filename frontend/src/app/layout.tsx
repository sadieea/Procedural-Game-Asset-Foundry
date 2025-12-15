import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Procedural Game Asset Foundry',
  description: 'JSON-Native, Studio-Grade Visual Asset Generator for Game Developers',
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body className="overflow-hidden">
        <div className="h-screen w-screen bg-studio-dark">
          {children}
        </div>
      </body>
    </html>
  )
}