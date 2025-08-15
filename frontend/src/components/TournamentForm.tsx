import React, { useState } from 'react'
import { tournamentApi } from '../api'

interface TournamentFormProps {
  onTournamentCreated: () => void
}

export default function TournamentForm({ onTournamentCreated }: TournamentFormProps) {
  const [name, setName] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!name.trim()) {
      setError('Tournament name is required')
      return
    }

    setIsLoading(true)
    setError('')

    try {
      await tournamentApi.createTournament(name.trim())
      setName('')
      onTournamentCreated()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create tournament')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="tournamentName" className="mb-1 block text-sm font-medium text-gray-700">
          Tournament Name
        </label>
        <input
          id="tournamentName"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          disabled={isLoading}
          className="w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-green-500 focus:outline-none focus:ring-green-500 disabled:bg-gray-100"
          placeholder="Enter tournament name"
        />
      </div>
      
      {error && (
        <div className="text-sm text-red-600">{error}</div>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className="w-full rounded-md bg-green-600 px-4 py-2 text-white transition-colors hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:bg-green-400"
      >
        {isLoading ? 'Creating...' : 'Create Tournament'}
      </button>
    </form>
  )
}