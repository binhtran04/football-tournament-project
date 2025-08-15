export interface Team {
  id: number
  team_id: string
  name: string
  created_at?: string
}

export interface Tournament {
  id: number
  tournament_id: string
  name: string
  created_at?: string
  teams?: TournamentTeam[]
}

export interface TournamentTeam {
  id: number
  team_id: string
  team_name: string
  created_at?: string
}