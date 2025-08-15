import { http, HttpResponse } from 'msw'
import { Team, Tournament } from '../types'

// Mock data
const mockTeams: Team[] = [
  {
    id: 1,
    team_id: 'team-001',
    name: 'Helsinki FC',
    created_at: '2024-01-01T10:00:00Z'
  },
  {
    id: 2,
    team_id: 'team-002', 
    name: 'Oulu United',
    created_at: '2024-01-01T11:00:00Z'
  }
]

const mockTournaments: Tournament[] = [
  {
    id: 1,
    tournament_id: 'tournament-001',
    name: 'Spring Cup',
    created_at: '2024-01-01T09:00:00Z',
    teams: []
  }
]

export const handlers = [
  // Team endpoints
  http.get('*/teams', () => {
    return HttpResponse.json(mockTeams)
  }),

  http.post('*/teams', async ({ request }) => {
    const { name } = await request.json() as { name: string }
    const newTeam: Team = {
      id: mockTeams.length + 1,
      team_id: `team-00${mockTeams.length + 1}`,
      name,
      created_at: new Date().toISOString()
    }
    mockTeams.push(newTeam)
    return HttpResponse.json(newTeam)
  }),

  // Tournament endpoints
  http.get('*/tournaments', () => {
    return HttpResponse.json(mockTournaments)
  }),

  http.post('*/tournaments', async ({ request }) => {
    const { name } = await request.json() as { name: string }
    const newTournament: Tournament = {
      id: mockTournaments.length + 1,
      tournament_id: `tournament-00${mockTournaments.length + 1}`,
      name,
      created_at: new Date().toISOString(),
      teams: []
    }
    mockTournaments.push(newTournament)
    return HttpResponse.json(newTournament)
  }),
]