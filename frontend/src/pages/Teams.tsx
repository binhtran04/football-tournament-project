import { useState, useEffect } from "react";
import TeamForm from "../components/TeamForm";
import { teamApi } from "../api";
import { Team } from "../types";

export default function Teams() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const loadTeams = async () => {
    try {
      const data = await teamApi.getTeams();
      setTeams(data);
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load teams");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadTeams();
  }, []);

  const handleTeamCreated = () => {
    loadTeams();
  };

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="text-lg">Loading teams...</div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="mb-6 text-3xl font-bold text-gray-900">Teams</h1>

        <div className="rounded-lg bg-white p-6 shadow">
          <h2 className="mb-4 text-xl font-semibold text-gray-800">
            Create New Team
          </h2>
          <TeamForm onTeamCreated={handleTeamCreated} />
        </div>
      </div>

      <div className="rounded-lg bg-white p-6 shadow">
        <h2 className="mb-4 text-xl font-semibold text-gray-800">All Teams</h2>

        {error && (
          <div className="mb-4 rounded border border-red-200 bg-red-50 px-4 py-3 text-red-700">
            {error}
          </div>
        )}

        {teams.length === 0 ? (
          <div className="py-8 text-center text-gray-500">
            No teams found. Create your first team above!
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {teams.map((team) => (
              <div
                key={team.id}
                className="rounded-lg border border-gray-200 p-4 transition-shadow hover:shadow-md"
              >
                <h3 className="text-lg font-semibold text-gray-900">
                  {team.name}
                </h3>
                <p className="mt-1 text-sm text-gray-600">ID: {team.team_id}</p>
                {team.created_at && (
                  <p className="mt-2 text-xs text-gray-500">
                    Created: {new Date(team.created_at).toLocaleDateString()}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
