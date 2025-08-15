import { Team, Tournament } from "./types";

const TEAM_SERVICE_URL =
  (import.meta as any).env.VITE_TEAM_SERVICE_URL || "http://localhost:8001";
const TOURNAMENT_SERVICE_URL =
  (import.meta as any).env.VITE_TOURNAMENT_SERVICE_URL ||
  "http://localhost:8002";

// Team API
export const teamApi = {
  async createTeam(name: string): Promise<Team> {
    const response = await fetch(`${TEAM_SERVICE_URL}/teams`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name }),
    });

    if (!response.ok) {
      throw new Error("Failed to create team");
    }

    return response.json();
  },

  async getTeams(): Promise<Team[]> {
    const response = await fetch(`${TEAM_SERVICE_URL}/teams`);

    if (!response.ok) {
      throw new Error("Failed to fetch teams");
    }

    return response.json();
  },
};

// Tournament API
export const tournamentApi = {
  async createTournament(name: string): Promise<Tournament> {
    const response = await fetch(`${TOURNAMENT_SERVICE_URL}/tournaments`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name }),
    });

    if (!response.ok) {
      throw new Error("Failed to create tournament");
    }

    return response.json();
  },

  async getTournaments(): Promise<Tournament[]> {
    const response = await fetch(`${TOURNAMENT_SERVICE_URL}/tournaments`);

    if (!response.ok) {
      throw new Error("Failed to fetch tournaments");
    }

    return response.json();
  },
};
