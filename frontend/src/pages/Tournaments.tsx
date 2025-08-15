import { useState, useEffect } from "react";
import TournamentForm from "../components/TournamentForm";
import { tournamentApi } from "../api";
import { Tournament } from "../types";

export default function Tournaments() {
  const [tournaments, setTournaments] = useState<Tournament[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  const loadTournaments = async () => {
    try {
      const data = await tournamentApi.getTournaments();
      setTournaments(data);
      setError("");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to load tournaments"
      );
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadTournaments();
  }, []);

  const handleTournamentCreated = () => {
    loadTournaments();
  };

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="text-lg">Loading tournaments...</div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="mb-6 text-3xl font-bold text-gray-900">Tournaments</h1>

        <div className="rounded-lg bg-white p-6 shadow">
          <h2 className="mb-4 text-xl font-semibold text-gray-800">
            Create New Tournament
          </h2>
          <TournamentForm onTournamentCreated={handleTournamentCreated} />
        </div>
      </div>

      <div className="rounded-lg bg-white p-6 shadow">
        <h2 className="mb-4 text-xl font-semibold text-gray-800">
          All Tournaments
        </h2>

        {error && (
          <div className="mb-4 rounded border border-red-200 bg-red-50 px-4 py-3 text-red-700">
            {error}
          </div>
        )}

        {tournaments.length === 0 ? (
          <div className="py-8 text-center text-gray-500">
            No tournaments found. Create your first tournament above!
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {tournaments.map((tournament) => (
              <div
                key={tournament.id}
                className="rounded-lg border border-gray-200 p-4 transition-shadow hover:shadow-md"
              >
                <h3 className="text-lg font-semibold text-gray-900">
                  {tournament.name}
                </h3>
                <p className="mt-1 text-sm text-gray-600">
                  ID: {tournament.tournament_id}
                </p>
                {tournament.created_at && (
                  <p className="mt-2 text-xs text-gray-500">
                    Created:{" "}
                    {new Date(tournament.created_at).toLocaleDateString()}
                  </p>
                )}
                {tournament.teams && tournament.teams.length > 0 && (
                  <div className="mt-3">
                    <p className="text-xs font-medium text-gray-700">
                      Teams: {tournament.teams.length}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
