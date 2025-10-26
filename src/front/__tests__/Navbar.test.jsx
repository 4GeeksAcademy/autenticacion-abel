import React from 'react'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { Navbar } from '../components/Navbar'

test('shows email when token present', () => {
  const payload = { email: 'test@example.com' }
  const token = ['header', btoa(JSON.stringify(payload)), 'signature'].join('.')
  sessionStorage.setItem('token', token)
  render(
    <MemoryRouter>
      <Navbar />
    </MemoryRouter>
  )
  expect(screen.getByText(/test@example.com/)).toBeInTheDocument()
  sessionStorage.removeItem('token')
})
