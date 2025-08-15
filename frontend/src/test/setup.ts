import '@testing-library/jest-dom'
import { beforeAll, afterEach, afterAll } from 'vitest'
import { setupServer } from 'msw/node'
import { handlers } from './handlers'

// This configures a request mocking server with the given request handlers.
export const server = setupServer(...handlers)

// Establish API mocking before all tests.
beforeAll(() => server.listen())

// Reset any request handlers that are added during tests.
afterEach(() => server.resetHandlers())

// Cleanup after tests are finished.
afterAll(() => server.close())